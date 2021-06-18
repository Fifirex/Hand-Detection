#! /usr/bin/python3
import cv2
import mediapipe as mp
import rospy
from std_msgs.msg import Int16MultiArray

def talker():
  mp_drawing = mp.solutions.drawing_utils
  mp_hands = mp.solutions.hands

  # Master counter
  i = 1

  # Passing Array
  arr = [[0,0],[0,0]]

  # GLOBALS
  CONFIG_CYCLE = 50 #def = 50
  STRENGTH = 2	    #def = 2

  # tools
  dist = 0
  ctr = 0
  low = 0
  high = 0
  low2 = 0
  mid2 = 0
  high2 = 0
  orient = 2
  switch = 0
  claw = 0
  flag = 0

  # ROS_init
  pub = rospy.Publisher('TopicArr', Int16MultiArray, queue_size=10)
  rate = rospy.Rate(10)

  # For webcam input:
  cap = cv2.VideoCapture(0)

  with mp_hands.Hands(
    min_detection_confidence = 0.5,
    max_num_hands = 1,
    min_tracking_confidence = 0.5) as hands:

    while cap.isOpened():
      success, image = cap.read()

      # init for size of the frame
      h, w, r = image.shape

      # DEBUG BLOCK
      print (arr)

      if rospy.is_shutdown():
        exit()

      print("Loop Running")
      Md = Int16MultiArray()
      x = [arr[0][0], arr[1][0], arr[0][1], arr[1][1]]
      Md.data = x
      pub.publish(Md)
      rate.sleep()

      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # Flip the image horizontally for a later selfie-view display
      # and convert the BGR image to RGB.
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      results = hands.process(image)

      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          for id, lms in enumerate(hand_landmarks.landmark):
              
            # MAIN_SWITCH
            if ((ctr >= CONFIG_CYCLE) and (arr[0][0] == 0) and (arr[0][1] == 0) and (arr[1][0] == 0) and (arr[1][1] == 0)):
              ctr+= 1
              if ((ctr >= STRENGTH*CONFIG_CYCLE) and (switch == 0)):
                arr[1][1] = 1
                switch = 1

            #HANDS_BACK
            if (switch == 1):
              arr[1][1] = 1

            # TRANSLATION
            if ((id == 9) and (lms.x*w < 3*w//5) and (lms.x*w > 2*w//5) and (arr[0][0] != 0)):
              arr[0][0] = 0
            elif ((orient == 0) or (orient == 1)):
              if ((id == 2) and (lms.x*w > 3*w//5) and (arr[0][0] != 1)):
                arr[0][0] = 1
              elif ((id == 20) and (lms.x*w < 2*w//5) and (arr[0][0] != -1)):
                arr[0][0] = -1
            elif (orient == -1):
              if ((id == 20) and (lms.x*w > 3*w//5) and (arr[0][0] != 1)):
                arr[0][0] = 1
              elif ((id == 2) and (lms.x*w < 2*w//5) and (arr[0][0] != -1)):
                arr[0][0] = -1

            # ROTATION
            if (id == 4):
              low2 = lms.x*w
            elif (id == 5):
              mid2 = lms.x*w
            elif (id == 9):
              high2 = lms.x*w          
            # hand orientation config
            if (high2!=0 and low2!=0 and mid2!=0):
              if (mid2 < high2):
                if (low2 < mid2):
                  orient = 1
                else:
                  orient = 0
              else:
                if (low2 > mid2):
                  orient = -1
                else:
                  orient = 0
              high2 = 0
              low2 = 0
              mid2 = 0
            # info_transmission
            if (arr[0][0]!=0):
              arr[1][0] = 0
            else:
              arr[1][0] = orient

            # CLAWING 
            if (id == 12):
              low = lms.y*h
            elif (id == 0):
              high = lms.y*h
            # config_cycle
            if ((ctr < CONFIG_CYCLE) and (low != 0) and (high !=0)):
              if (dist == 0): 
                dist = (high - low)/3
              else:
                dist = (dist + (high - low)/3)/2 
              ctr += 1
            # claw_check
            elif (ctr >= CONFIG_CYCLE):
              if (((high - low) < dist) and (claw == 0)):
                claw = 1
              if (((high - low) > dist) and (claw == 1)):
                claw = 0
            # info_transmission
            if (claw == 0):
              flag = 1
            elif (flag == 1):
              if (arr[0][1] == 1):
                arr[0][1] = 0
                flag = 0
              else:
                arr[0][1] = 1
                flag = 0

          mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        i += 1

      # HANDS AWAY
      else: 
        arr[0][0] = 0
        arr[1][0] = 0
        arr[0][1] = 0
        arr[1][1] = 0
        ctr = 0     # resets config_cycle

      #cv2.putText(image, fps, (20, 120), font, 3, (10, 155, 0), 3, cv2.LINE_AA)    ## FPS counter
      cv2.line(image, (2 * w // 5, 0), (2 * w // 5, h), (0,0,0), 5)
      cv2.line(image, (3 * w // 5, 0), (3 * w // 5, h), (0,0,0), 5)
      cv2.imshow('Hands', image)

      if cv2.waitKey(2) & 0xFF == 27:
        break

  cap.release()
  rospy.spin()  

if __name__ == '__main__':
  rospy.init_node('talker',anonymous=True)
  talker()