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

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Load the CSV into a pandas DataFrame
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
            # Extract the x, y for each landmark in the frame (only need 2D)
            landmark = frame_data[frame_data['landmark'] == landmark_id]
            if not landmark.empty:
                x, y = landmark['x'].values[0], landmark['y'].values[0]
                landmarks.append((x, y))  
            #else:
                #landmarks.append((0, 0))
        
        swing_data.append(landmarks)
    
    return swing_data

def overlay_swing_on_video(video_path, swing_data, output_video_path):
    # Open the video
    cap = cv2.VideoCapture(video_path)
    
    # Get the video dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    vid = []
    frame_idx = 0
    success, frame = cap.read()

    while success and frame_idx < len(swing_data):
        landmarks = swing_data[frame_idx]

        # Scale landmarks to actual frame dimensions
        scaled_landmarks = []
        for landmark in landmarks:
            if len(landmark) == 2:  
                x, y = landmark
            else:
                continue  # Skip invalid landmark data
            
            # Scale the coordinates based on frame size
            scaled_landmarks.append((x * frame_width, y * frame_height))

        # Create a landmark list for drawing
        landmarks_proto = convert_to_landmark_list(scaled_landmarks)

        # Draw landmarks and connections on the frame
        frame_copy = frame.copy()
        mp_drawing.draw_landmarks(
            frame_copy,
            landmarks_proto,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )

        vid.append(frame_copy)
        success, frame = cap.read()
        frame_idx += 1

    vid = np.array(vid)
    save_vid(vid, output_video_path, frame_width, frame_height)
    cap.release()

csv_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/pro_swing_rubric.csv"
loaded_sd = load_swing_data(csv_path)
sd = get_swing_data(loaded_sd)

#video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/fswing.mp4"
video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/backend/golf_videos/72.mp4"
output_video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/output_video.mp4"
overlay_swing_on_video(video_path, sd, output_video_path)