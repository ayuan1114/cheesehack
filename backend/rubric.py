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
    
    min_x, min_y, max_x, max_y = get_pose_box(pose_data)

    box_w = max_x - min_x
    box_h = max_y - min_y

    # iterate through each frame in pose_data
    for frame in pose_data:
        # case where no pose was detected
        if frame is None:  
            normalized_data.append(None)
            continue

        # Normalize each landmark's coordinates relative to the center of the landmarks
        normalized_frame = [
            ((landmark.x - min_x) / box_w, (landmark.y - min_y) / box_h, landmark.z) 
            for landmark in frame.landmark
        ]

        normalized_data.append(normalized_frame)
    return np.array(normalized_data, dtype=object)

def project_pose(norm_pose_data, cur_pose_data):
    projected_data = []

    min_x, min_y, max_x, max_y = get_pose_box(cur_pose_data)

    box_w = max_x - min_x
    box_h = max_y - min_y

    for pose in norm_pose_data:
        # case where no pose was detected
        if pose is None:  
            projected_data.append(None)
            continue

        # Normalize each landmark's coordinates relative to the center of the landmarks
        projected_frame = [
            [point[0] * box_w + min_x, point[1] * box_h + min_y, point[2]] 
            for point in pose
        ]

        projected_data.append(projected_frame)
    projected_data = np.array(projected_data)
    return projected_data

#save frame as a csv
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

# save frame as a csv (not normalized)
def save_data(data, output_file):
    # Ensure the input data is structured correctly
    frames = []
    for frame_idx, frame in enumerate(data):
        if frame is not None:  # Skip frames where no pose was detected
            for landmark_idx, landmark in enumerate(frame.landmark):
                frames.append({
                    'frame': frame_idx,
                    'landmark': landmark_idx,
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
    df = pd.DataFrame(frames)
    df.to_csv(os.path.join(output_folder, output_file), index=False)

def overlay_swing_on_video(video_path, swing_data, output_video_path):
    vid, width, height = extract_frames(video_path, get_dims=True)
    _, captured_pose = process_vid(vid)
    
    norm_swing_data = normalize_pose_data(swing_data)
    projected_pose = project_pose(norm_swing_data, captured_pose)
    projected_landmarks = convert_to_landmark(projected_pose)

    projected_frames = []
    pose_idx = 0
    for frame in vid:
        if pose_idx < len(projected_landmarks):
            if projected_landmarks[pose_idx]:
                mp_drawing.draw_landmarks(
                    frame,
                    projected_landmarks[pose_idx],
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                )
        projected_frames.append(frame)
        pose_idx+=1
    projected_frames = np.array(projected_frames)
    save_vid(projected_frames, output_video_path, width, height)