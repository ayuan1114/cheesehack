# Takes pro golfer swing and uses that as rubric for input
# Input: a pro swing video
# Output: csv containing pose data

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from model import process_vid
from camera import save_vid
import os
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark, NormalizedLandmarkList

output_folder = "videos"

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def convert_to_landmark(poses):
    landmarks_array = []
    for pose in poses:
        landmarks_array.append(NormalizedLandmarkList(landmark=[
            NormalizedLandmark(x=landmark[0], y=landmark[1], z=landmark[2]) for landmark in pose
        ]))
    return landmarks_array

def landmarks_to_numpy(pose_array):
    landmarks = [[
        [landmark.x, landmark.y, landmark.z] for landmark in landmark_list.landmark
    ] for landmark_list in pose_array]
    return np.array(landmarks)

def get_pose_box(pose_data):
    np_pose = landmarks_to_numpy(pose_data)
    np_pose = np_pose.reshape(-1, 3)
    np_x = np_pose[:, 0]
    np_y = np_pose[:, 1]
    max_x = np.max(np_x[(np_x > 0) & (np_y > 0)])
    max_y = np.max(np_y[(np_x > 0) & (np_y > 0)])
    min_x = np.min(np_x[(np_x > 0) & (np_y > 0)])
    min_y = np.min(np_y[(np_x > 0) & (np_y > 0)])
    return min_x, min_y, max_x, max_y
    
def draw_pose_box(frames, pose_data, width, height):
    
    min_x, min_y, max_x, max_y = get_pose_box(pose_data)

    min_x = int(min_x * width)
    min_y = int(min_y * height)
    max_x = int(max_x * width)
    max_y = int(max_y * height)

    for frame in frames:
        cv2.line(frame, (min_x, min_y), (max_x, min_y), (255, 0, 0))
        cv2.line(frame, (max_x, min_y), (max_x, max_y), (255, 0, 0))
        cv2.line(frame, (max_x, max_y), (min_x, max_y), (255, 0, 0))
        cv2.line(frame, (min_x, max_y), (min_x, min_y), (255, 0, 0))

    return frames

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
