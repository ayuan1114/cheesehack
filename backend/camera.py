import cv2
from model import process_frame, process_vid
import os
import ffmpeg
import numpy as np

output_folder = "videos"

os.makedirs(output_folder, exist_ok=True)

# Open a connection to the webcam
camera = cv2.VideoCapture(0)
fps = 30
camera.set(cv2.CAP_PROP_FPS, fps)
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

def capture(show = False, save = True):
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
    return frames

def play_vid(video, cap = "Recording"):
    playing = True
    while playing:
        for frame in video:
            cv2.imshow(cap, frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                playing = False
                break

def save_vid(video, file_name):
    codec = 'libx264'

    (
        ffmpeg
        .input('pipe:0', framerate=30, format='rawvideo', pix_fmt='bgr24', s=f'{width}x{height}')
        .output(os.path.join(output_folder, file_name), vcodec=codec, pix_fmt='yuv420p')
        .overwrite_output()
        .run(input=video.tobytes())  # Pass the raw bytes of the frames
    )

test_vid = capture(True)
save_vid(test_vid, 'test_vid.mp4')
processed_vid, captured_pose = process_vid(test_vid)
save_vid(processed_vid, 'processed_vid.mp4')
play_vid(processed_vid, '')