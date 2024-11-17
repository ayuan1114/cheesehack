import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from model import process_vid, process_frame

# function to extract frames from professional video
def extract_frames(video_path, frame_rate=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # make sure interal is always 1, even if fps is lower than frame_rate
    if fps < frame_rate:
        print("Warning: Video FPS is lower than the desired frame rate. Using FPS as the frame rate.")
        interval = 1  # Capture all frames if FPS is lower than the requested frame rate
    else:
        interval = fps // frame_rate

    success, frame = cap.read()
    count = 0
    
    while success:
        if count % interval == 0:
            # Convert frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
            # Log the frame shape
            #print(f"Processed frame {count}, shape: {frame.shape}, converted to RGB")
        success, frame = cap.read()
        count += 1
    
    cap.release()
    frames = np.array(frames)
    print(frames)    
    return frames
    
# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# normalize data so you can use any camera
def normalize_pose_data(pose_data):
    normalized_data = []
    
    # iterate through each frame in pose_data
    for frame in pose_data:
        # case where no pose was detected
        if frame is None:  
            normalized_data.append(None)
            continue
        
        # Calculate the center of all landmarks (average of all x, y, z coordinates)
        center_x = np.mean([landmark.x for landmark in frame.landmark])
        center_y = np.mean([landmark.y for landmark in frame.landmark])
        center_z = np.mean([landmark.z for landmark in frame.landmark])

        # Normalize each landmark's coordinates relative to the center of the landmarks
        normalized_frame = [
            (landmark.x - center_x, landmark.y - center_y, landmark.z - center_z) 
            for landmark in frame.landmark
        ]
        
        # get frame dimensensions 
        frame_height, frame_width, _ = frame.shape

        # make landmark center also the frame center
        normalized_frame = [
            (landmark[0] - (frame_width / 2) + center_x,  # Adjust x
             landmark[1] - (frame_height / 2) + center_y, # Adjust y
             landmark[2])  # No adjustment for z (depth remains the same)
            for landmark in normalized_frame
        ]

        normalized_data.append(normalized_frame)
    
    return np.array(normalized_data, dtype=object)

# save frame as a csv
def save_data(data, output_file):

    # itialize data frame
    df = pd.DataFrame({
        'frame': np.repeat(range(data.shape[0]), data.shape[1]),
        'landmark': np.tile(range(data.shape[1]), data.shape[0]),
        'x': data[:,:,0].flatten(),
        'y': data[:,:,1].flatten(),
        'z': data[:,:,2].flatten()
    })
    df.to_csv(output_file, index=False)

video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/backend/golf_videos/72.mp4"
frames = extract_frames(video_path)
_,pose_data = process_vid(frames)
normalized_data = normalize_pose_data(pose_data)
save_data(pose_data, 'pro_swing_rubric.csv')