# Extract the skeleton (pose landmarks) from a pro swing and normalize it
# Extract the skeleton from the user video
# Overlay the pro's swing onto the user's video for comparison
# Save this overlay as new video
import os

from data_extract import capture, save_vid, play_vid, extract_frames, save_norm_swing, load_norm_swing
from model import process_vid, draw_pose_box, overlay_swing

# File Paths
input_dir = "input_videos"
pro_csv_dir = "pro_csv"
output_dir = "output_videos"

# create output dir if it doesnt exist
os.makedirs(output_dir, exist_ok=True)

# Load User Video
input_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]
if not input_files:
    raise Exception("No input video found in folder")
 
input_video_name = input_files[0]
#input_video_path = input_files[0]
input_video_path = os.path.join(input_dir, input_files[0])

# load PRO CSV
csv_files = [f for f in os.listdir(pro_csv_dir) if f.endswith(".csv")]
if not csv_files:
    raise Exception("No CSV file found in folder")
pro_csv_name = csv_files[0]
pro_csv_path = os.path.join(pro_csv_dir, pro_csv_name)

# extract frames and dimensions from user's video
user_frames, width, height = extract_frames(input_video_path, get_dims=True)

# process user frames for pose estimation
processed_user_frames, user_pose = process_vid(user_frames)

# load pro pose from CSV
pro_pose = load_norm_swing(pro_csv_path)

# overlay pro pose onto user video
overlayed_frames = overlay_swing(user_frames, height, width, pro_pose, add_box=True, og_pose=True)

# save output video in folder
output_filename = f"compare_{os.path.splitext(input_video_name)[0]}_vs_{os.path.splitext(pro_csv_name)[0]}.mp4"
output_path = os.path.join(output_dir, output_filename)
save_vid(overlayed_frames, output_path, width, height)

print(f"Saved to: {output_path}")


###OLD below

# extract frames from pro video
#pro_vid, width1, height1 = extract_frames("pro.mp4", get_dims=True)
# pro_vid, width1, height1 = extract_frames("72.mp4", get_dims=True)

# # save the pro video pose landmarks
# save_norm_swing(pro_vid, "pro_pose.csv")
# # load back the saved pro pose landmarks
# pro_pose = load_norm_swing("pro_pose.csv")
# # extract frames from user's swing video
# vid, width2, height2 = extract_frames("fswing.mp4", get_dims=True)
# # process the user's swing video for pose detection
# processed_vid, f_pose = process_vid(vid)
# # overlay the pro swing over the user's swing
# overlayed_frames = overlay_swing(vid, height2, width2, pro_pose, add_box=True, og_pose=True)
# # save video
# save_vid(overlayed_frames, "projected_vid.mp4", width2, height2)