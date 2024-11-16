import cv2
import mediapipe as mp
from model import process_frame, process_vid

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Open a connection to the webcam
camera = cv2.VideoCapture(0)

frames = []

def capture():
    if not camera.isOpened():
        print("Error: Could not access the camera.")
    else:
        print("Camera feed started. Press 'q' to quit.")
        
        while True:
            # Read a frame from the camera
            ret, frame = camera.read()
            
            if not ret:
                print("Failed to grab a frame.")
                break
            frames.append(frame) # each frame is numpy array
            cv2.imshow("Recording...", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()
    return frames

def play_vid(video, cap):
    playing = True
    while playing:
        for frame in video:
            cv2.imshow(cap, frame)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                playing = False
                break
