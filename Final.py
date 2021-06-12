import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

sourcefile = open('Landmarks.txt', 'w')       #### Printing landmark locations to ext file ####

## Execuation time counter ##
starttime = time.time()

## FPS counter
last_frame_time, current_frame_time = 0, 0

i = 1       ## For indexing output ##

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5) as hands:
  
  while cap.isOpened():
    success, image = cap.read()
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
          if(id == 5 or id == 6 or id == 7 or id == 8):
            ##### Not printing out lover hand to reduce the clutter ############

            ######### Might split for each finger and then combine finally if too much cluttering ###########
            sourcefile.write(f"\n{i}:\n{id}:\n{lms}\n\n")

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      i += 1
            
    cv2.putText(image, fps, (20, 120), font, 3, (10, 155, 0), 3, cv2.LINE_AA)    ## FPS counter
    cv2.imshow('MediaPipe Hands', image)
    
    endtime = time.time()     ## runtime counter ##
    print(endtime-starttime)

    if cv2.waitKey(2) & 0xFF == 27:
      break

sourcefile.close()
cap.release()