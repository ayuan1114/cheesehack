from data_extract import capture, save_vid, play_vid, extract_frames, save_norm_swing, load_norm_swing
from model import process_vid, draw_pose_box, overlay_swing

pro_vid, width1, height1 = extract_frames("pro.mp4", get_dims=True)
save_norm_swing(pro_vid, "pro_pose.csv")
pro_pose = load_norm_swing("pro_pose.csv")
vid, width2, height2 = extract_frames("fswing.mp4", get_dims=True)
processed_vid, f_pose = process_vid(vid)
overlayed_frames = overlay_swing(vid, height2, width2, pro_pose, add_box=True, og_pose=True)
save_vid(overlayed_frames, "projected_vid.mp4", width2, height2)