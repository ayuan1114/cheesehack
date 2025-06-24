import os
from data_extract import extract_frames, save_norm_swing

# define file paths
pro_video_dir = "pro_videos"
pro_csv_dir = "pro_csv"

# load first available pro video
pro_videos = [f for f in os.listdir(pro_video_dir) if f.endswith(".mp4")]
if not pro_videos:
    raise Exception("No videos found in pro_videos")
pro_video_name = pro_videos[0]
pro_video_path = os.path.join(pro_video_dir, pro_video_name)

# extract frames
pro_frames, width, height = extract_frames(pro_video_path, get_dims=True)

# save normalized pose to CSV
csv_name = os.path.splitext(pro_video_name)[0] + ".csv"
csv_path = os.path.join(pro_csv_dir, csv_name)
save_norm_swing(pro_frames, csv_path)

print(f"Pro pose CSV saved to: {csv_path}")
