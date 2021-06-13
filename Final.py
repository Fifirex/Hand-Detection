import cv2
import mediapipe as mp
import time
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands   

# Execuation time counter 
starttime = time.time()

# FPS counter
last_frame_time, current_frame_time = 0, 0

# Master counter
i = 1      

# Main np array layout ([lateral_state, NULL], [closed_check, NULL])
# Lateral_state: right (1), centre (0), left (-1)
arr = np.array([[0, 0], [0, 0]]) 

# Config Distance
CONFIG_CYCLE = 50
dist = 0
ctr = 0
low = 0
high = 0

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence = 0.5,
    max_num_hands = 1,
    min_tracking_confidence = 0.6) as hands:
  
  while cap.isOpened():
    success, image = cap.read()

    # init for size of the frame
    h, w, r = image.shape

    # DEBUG
    print (arr)
    print("POSITION : ")
    if ( arr[0,0] == 1 ):
      print("RIGHT")
    elif ( arr[0,0]== -1 ):
      print("LEFT")
    elif ( arr[0,0] == 0 ):
      print("CENTRE")
    print("CLAWED : ")
    if ( ctr >= CONFIG_CYCLE ):
      if ( arr[0,1] == 1):
        print("YES")
      else:
        print("NO")
    else:
      print("IN CONFIG")
    # print (3*w//5)
    # print (ctr)
    # print (dist)

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    ##FPS counter
    current_frame_time = time.time()
    fps = 1/(current_frame_time - last_frame_time)
    last_frame_time = current_frame_time
    fps = str(int(fps))
    font = cv2.FONT_HERSHEY_COMPLEX

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

          # LATERAL MOVEMENT
          # right
          if ((id == 4) and (lms.x*w > 3*w//5) and (arr[0, 0] != 1)):
            arr[0, 0] = 1
          #left
          elif ((id == 20) and (lms.x*w < 2*w//5) and (arr[0, 0] != -1)):
            arr[0, 0] = -1
          #centre
          elif ((id == 9) and (lms.x*w < 3*w//5) and (lms.x*w > 2*w//5) and (arr[0, 0] != 0)):
            arr[0, 0] = 0

          # CLAWING UP
          if ((id == 12)):
            low = lms.y*h
          elif ((id == 0)):
            high = lms.y*h
          # config_cycle
          if ((ctr < CONFIG_CYCLE) and (low != 0) and (high !=0)):
            if (dist == 0): 
              dist = (high - low)/2
            else:
              dist = (dist + (high - low)/2)/2 
            ctr += 1
          # claw check
          elif (ctr >= CONFIG_CYCLE):
            if (((high - low) < dist) and (arr[0, 1] == 0)):
              arr[0, 1] = 1
            if (((high - low) > dist) and (arr[0, 1] == 1)):
              arr[0, 1] = 0

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      i += 1
            
    cv2.putText(image, fps, (20, 120), font, 3, (10, 155, 0), 3, cv2.LINE_AA)    ## FPS counter
    cv2.line(image, (2 * w // 5, 0), (2 * w // 5, h), (0,0,0), 5)
    cv2.line(image, (3 * w // 5, 0), (3 * w // 5, h), (0,0,0), 5)
    cv2.imshow('Hands', image)
    
    endtime = time.time()     ## runtime counter ##
    # print(endtime-starttime)

    if cv2.waitKey(2) & 0xFF == 27:
      break

cap.release()

# Jointly created by a Bangladeshi Immigrant and his kid.