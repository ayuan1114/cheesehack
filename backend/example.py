from camera import capture, save_vid, play_vid, extract_frames
from model import process_vid, draw_pose_box, overlay_swing_on_video

pro_vid, width1, height1 = extract_frames("pro.mp4", get_dims=True)
_, pro_pose = process_vid(pro_vid)
vid, width2, height2 = extract_frames("fswing.mp4", get_dims=True)
processed_vid, f_pose = process_vid(vid)
overlayed_frames = overlay_swing_on_video(vid, height2, width2, pro_pose, add_box=True, og_pose=True)
save_vid(overlayed_frames, "projected_vid.mp4", width2, height2)