# main FastAPI file

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import tempfile
from typing import List
import uuid
from pathlib import Path
import logging

# import your existing moduldes
from data_extract import extract_frames, save_norm_swing, load_norm_swing
from model import process_vid, overlay_swing

# configure logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# initialize fastAPI
app = FastAPI(
    title = "Golf Swing Comparison",
    description = "FastAPI to help comparing user golf swing with professional golf swing",
    version="1.0.0"
)

# add CORS middleware
# configure this during production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# directory set up
base_dir = Path(__file__).parent
input_dir = base_dir / "input_videos"
output_dir = base_dir / "output_videos"
pro_csv_dir = base_dir / "pro_csv"
pro_videos_dir = base_dir / "pro_videos"
temp_dir = base_dir / "temp"

# create directories if they don't exist

# store processing jobs
processing_jobs = {}

class ProcessingStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED  = "failed"

# root: check if running endpoint
@app.get("/")
async def root():
    return {"message": "Swing Comparison API is running"}

# status health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# get /pro_videos
@app.get("/pro-videos")
async def list_pro_videos():
    try:
        pro_videos = []
        for file in pro_videos_dir.glob("*.mp4"):
            pro_videos.append({
                "filename": file.name,
                "display_name": file.stem.replace("_", " ").title(),
                "path": str(file.relative_to(base_dir))
            })
        
        if not pro_videos:
            return {"pro_videos": [], "message": "No professional videos found"}
        
        # return a dictionary, script will convert to JSON 
        return {"pro_videos": pro_videos} # keep it like this, testing script expects this.
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing out pro videos: {str(e)}")
    
@app.post("/process-comparison")
async def process_comparison(
    user_video: UploadFile = File(...),
    pro_video_name: str = Form(...)
):
    """
    Process user video with selected pro video for pose comparison
    """
    if not user_video.filename.lower().endswith('.mp4'):
        raise HTTPException(status_code=400, detail="Only MP4 files are supported")
    
    # Generate unique identifier for this processing session
    session_id = str(uuid.uuid4())
    
    try:
        # Save uploaded user video temporarily
        user_video_path = temp_dir / f"{session_id}_user_video.mp4"
        with open(user_video_path, "wb") as buffer:
            content = await user_video.read()
            buffer.write(content)
        
        # Verify pro video exists
        pro_video_path = pro_videos_dir / pro_video_name
        if not pro_video_path.exists():
            raise HTTPException(status_code=404, detail=f"Pro video '{pro_video_name}' not found")
        
        # Check if corresponding CSV exists, if not create it
        pro_csv_name = pro_video_path.stem + ".csv"
        pro_csv_path = pro_csv_dir / pro_csv_name
        
        if not pro_csv_path.exists():
            print(f"Creating CSV for pro video: {pro_video_name}")
            # Extract frames from pro video and save normalized pose
            pro_frames, _, _ = extract_frames(str(pro_video_path), get_dims=True)
            save_norm_swing(pro_frames, str(pro_csv_path))
        
        # Process user video
        print(f"Processing user video...")
        user_frames, width, height = extract_frames(str(user_video_path), get_dims=True)
        
        # Load pro pose data
        print(f"Loading pro pose data from: {pro_csv_path}")
        pro_pose = load_norm_swing(str(pro_csv_path))
        
        # Create overlay
        print(f"Creating pose overlay...")
        overlayed_frames = overlay_swing(
            user_frames, height, width, pro_pose, 
            add_box=True, og_pose=True
        )
        
        # Save output video
        output_filename = f"comparing_{user_video.filename.split('.')[0]}_vs_{pro_video_path.stem}_{session_id}.mp4"
        output_path = output_dir / output_filename
        
        # Import save_vid from your data_extract module
        from data_extract import save_vid
        save_vid(overlayed_frames, str(output_path), width, height)
        
        # Clean up temporary user video
        user_video_path.unlink(missing_ok=True)
        
        return {
            "success": True,
            "session_id": session_id,
            "output_filename": output_filename,
            "message": "Video processed successfully",
            "download_url": f"/download/{output_filename}"
        }
        
    except Exception as e:
        # Clean up on error
        if 'user_video_path' in locals():
            user_video_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/download/{filename}")
async def download_video(filename: str):
    """Download processed video"""
    file_path = output_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="video/mp4"
    )

@app.get("/status/{session_id}")
async def get_processing_status(session_id: str):
    """Check if processing is complete for a session"""
    # Look for output files with this session_id
    output_files = list(output_dir.glob(f"comparison_{session_id}_*.mp4"))
    
    if output_files:
        return {
            "status": "completed",
            "output_filename": output_files[0].name,
            "download_url": f"/download/{output_files[0].name}"
        }
    else:
        return {"status": "processing"}

@app.delete("/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    """Clean up files for a specific session"""
    try:
        # Remove temporary files
        temp_files = list(temp_dir.glob(f"{session_id}_*"))
        for file in temp_files:
            file.unlink(missing_ok=True)
        
        # Optionally remove output files (you might want to keep these)
        # output_files = list(OUTPUT_VIDEOS_DIR.glob(f"comparison_{session_id}_*"))
        # for file in output_files:
        #     file.unlink(missing_ok=True)
        
        return {"message": "Session cleaned up successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup error: {str(e)}")

@app.get("/storage-info")
async def get_storage_info():
    """Get information about stored files"""
    try:
        return {
            "pro_videos_count": len(list(pro_videos_dir.glob("*.mp4"))),
            "pro_csvs_count": len(list(pro_csv_dir.glob("*.csv"))),
            "output_videos_count": len(list(output_dir.glob("*.mp4"))),
            "temp_files_count": len(list(temp_dir.glob("*")))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting storage info: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)