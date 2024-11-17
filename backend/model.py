import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# takes an rgb frame
def process_frame(frame):
    processed_frame = np.copy(frame)
    # Process the frame with MediaPipe Pose
    results = pose.process(processed_frame)
    
    # Draw pose landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            processed_frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )
    return processed_frame, results.pose_landmarks

def process_vid(video):
    processed_vid = []
    pose_array = []
    for frame in video:
        processed_frame, pose = process_frame(frame)
        processed_vid.append(processed_frame)
        pose_array.append(pose)
    processed_vid = np.array(processed_vid)
    pose_array = np.array(pose_array)
    return processed_vid, pose_array
            
