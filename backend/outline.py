# Takes input (video file, either pro or input) and will draw pose landmarks and skeleton on the original video

import pandas as pd
import cv2
import numpy as np
from camera import save_vid
import mediapipe as mp
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark, NormalizedLandmarkList

# helper function to convert landmark list to normalizedlandmarklist
def convert_to_landmark_list(landmarks):
    return NormalizedLandmarkList(landmark=[
        NormalizedLandmark(x=x, y=y, z=0) for x, y in landmarks
    ])

# initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# load the CSV into a pandas DataFrame
def load_swing_data(csv_path):
    df = pd.read_csv(csv_path)

    return df

# return swing data
def get_swing_data(df):
    swing_data = []
    # get highest landmark
    max_landmark = df['landmark'].max()

    for frame in df['frame'].unique():
        frame_data = df[df['frame'] == frame]
        landmarks = []
        
        for landmark_id in range(max_landmark + 1):  
            # extract the x, y for each landmark in the frame (only need 2D)
            landmark = frame_data[frame_data['landmark'] == landmark_id]
            if not landmark.empty:
                x, y = landmark['x'].values[0], landmark['y'].values[0]
                landmarks.append((x, y))  
            
        swing_data.append(landmarks)
    
    return swing_data

def overlay_swing_on_video(video_path, swing_data, output_video_path):
    # open the video
    cap = cv2.VideoCapture(video_path)
    
    # get the video dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    vid = []
    frame_idx = 0
    success, frame = cap.read()

    while success and frame_idx < len(swing_data):
        landmarks = swing_data[frame_idx]

        # scale landmarks to actual frame dimensions
        scaled_landmarks = []
        for landmark in landmarks:
            if len(landmark) == 2:  
                x, y = landmark
                # scale the coordinates based on frame size
                scaled_x = int(x * frame_width)
                scaled_y = int(y * frame_height)
                print(f"Landmark {frame_idx}: Scaled ({x}, {y}) to ({scaled_x}, {scaled_y})") 
                scaled_landmarks.append((scaled_x, scaled_y))

        # draw landmarks
        for i, (x, y) in enumerate(scaled_landmarks):
        
            cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0), -1)  
    
            # connect lines between landmarks that follow human body
            for connection in mp_pose.POSE_CONNECTIONS:

                start_idx, end_idx = connection
    
                # get the coordinates of the start and end landmarks
                start_landmark = scaled_landmarks[start_idx]
                end_landmark = scaled_landmarks[end_idx]
    
                # draw a line between the start and end landmarks
                start_x, start_y = int(start_landmark[0]), int(start_landmark[1])
                end_x, end_y = int(end_landmark[0]), int(end_landmark[1])
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)

        # store the frame with masked landmarks
        vid.append(frame)
        success, frame = cap.read()
        frame_idx += 1

    vid = np.array(vid)
    save_vid(vid, output_video_path, frame_width, frame_height)
    cap.release()

csv_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/pro_swing_rubric.csv"
loaded_sd = load_swing_data(csv_path)
sd = get_swing_data(loaded_sd)

video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/fswing.mp4"
#video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/backend/golf_videos/72.mp4"
output_video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/output_video.mp4"
overlay_swing_on_video(video_path, sd, output_video_path)