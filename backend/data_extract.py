# Capture a video from webcam
# Extracts frames from existing video
# Save or play video, converts pose landmark data into a CSV (saves each frame's landmarks)
# Processes the input video to extract pose landmarks, normalize pose data, save it 
# Load a previosuly saved swing CSV

import cv2
from model import process_frame, process_vid, normalize_pose_data, convert_to_landmark
import os
import ffmpeg
import tempfile
import numpy as np
import pandas as pd

video_folder = "videos"
data_folder = "data"

os.makedirs(video_folder, exist_ok=True)
os.makedirs(data_folder, exist_ok=True)


def capture(show = False, save = True, get_dims=False):
    camera = cv2.VideoCapture(0)

    fps = 30
    camera.set(cv2.CAP_PROP_FPS, fps)
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames = []
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
            if save:
                frames.append(frame) # each frame is numpy array
            if show:
                processed_frame, _ = process_frame(frame)
                cv2.imshow("Processed", processed_frame)

            else:
                cv2.imshow("Recording...", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()
    frames = np.array(frames)
    if get_dims:
        return frames, width, height
    else:
        return frames

# function to extract frames from professional video
def extract_frames(video_path, frame_rate=30, get_dims=False):

    # rotate video before extracting
    rotated_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    (
        ffmpeg
        .input(video_path)
        .filter('transpose', 1)  # rotate 90° clockwise
        .output(rotated_path)
        .overwrite_output()
        .run()
    )

    cap = cv2.VideoCapture(os.path.join(video_folder, video_path))

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
            frames.append(frame)
            # Log the frame shape
        success, frame = cap.read()
        count += 1
    
    cap.release()
    os.remove(rotated_path) # clean rotated video after frames extracted

    frames = np.array(frames)
    if get_dims:
        return frames, width, height
    else:
        return frames

def play_vid(video, cap = "Recording"):
    playing = True
    while playing:
        for frame in video:
            cv2.imshow(cap, frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                playing = False
                break

def save_vid(video, file_name, width, height):
    codec = 'libx264'

    (
        ffmpeg
        .input('pipe:0', framerate=30, format='rawvideo', pix_fmt='bgr24', s=f'{width}x{height}')
        .output(os.path.join(video_folder, file_name), vcodec=codec, pix_fmt='yuv420p')
        .overwrite_output()
        .run(input=video.tobytes())  # Pass the raw bytes of the frames
    )

# save frame as a csv (not normalized)
def save_data(data, output_file):
    # Ensure the input data is structured correctly
    frames = []
    for frame_idx, pose in enumerate(data):
        if pose is not None:  # Skip frames where no pose was detected
            for landmark_idx, landmark in enumerate(pose):
                frames.append({
                    'frame': frame_idx,
                    'landmark': landmark_idx,
                    'x': landmark[0],
                    'y': landmark[1],
                    'z': landmark[2]
                })
    df = pd.DataFrame(frames)
    df.to_csv(os.path.join(data_folder, output_file), index=False)

#takes swing vid
def save_norm_swing(video, file_name):
    _, pose = process_vid(video)
    norm_pose = normalize_pose_data(pose)
    save_data(norm_pose, file_name)

# return swing data from csv as list of landmarks
def load_norm_swing(file_name):
    df = pd.read_csv(os.path.join(data_folder, file_name))

    swing_data = []

    for frame in df['frame'].unique():
        frame_data = df[df['frame'] == frame]
        swing_data.append(frame_data[['x', 'y', 'z']].to_numpy())
    swing_data = np.array(swing_data)
    convert_to_landmark(swing_data)
    return swing_data