# Extract the skeleton (pose landmarks) from a pro swing and normalize it
# Extract the skeleton from the user video
# Overlay the pro's swing onto the user's video for comparison
# Save this overlay as new video

from data_extract import capture, save_vid, play_vid, extract_frames, save_norm_swing, load_norm_swing
from model import process_vid, draw_pose_box, overlay_swing


# extract frames from pro video
#pro_vid, width1, height1 = extract_frames("pro.mp4", get_dims=True)
pro_vid, width1, height1 = extract_frames("72.mp4", get_dims=True)

# save the pro video pose landmarks
save_norm_swing(pro_vid, "pro_pose.csv")
# load back the saved pro pose landmarks
pro_pose = load_norm_swing("pro_pose.csv")
# extract frames from user's swing video
vid, width2, height2 = extract_frames("fswing.mp4", get_dims=True)
# process the user's swing video for pose detection
processed_vid, f_pose = process_vid(vid)
# overlay the pro swing over the user's swing
overlayed_frames = overlay_swing(vid, height2, width2, pro_pose, add_box=True, og_pose=True)
# save video
save_vid(overlayed_frames, "projected_vid.mp4", width2, height2)