import cv2
from model import process_frame
import os
import ffmpeg
import numpy as np
import pandas as pd

output_folder = "videos"

os.makedirs(output_folder, exist_ok=True)


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
    cap = cv2.VideoCapture(os.path.join(output_folder, video_path))

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
        .output(os.path.join(output_folder, file_name), vcodec=codec, pix_fmt='yuv420p')
        .overwrite_output()
        .run(input=video.tobytes())  # Pass the raw bytes of the frames
    )

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