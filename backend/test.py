import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# function to extract frames from professional video
def extract_frames(video_path, frame_rate=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    return(fps)

video_path = "/Users/felixzhu/CS/cheesehacks/cheesehack/backend/golf_videos/27.mp4"

extract_frames(video_path)
fps = extract_frames(video_path)
print(f"FPS: {fps}")