import requests
import time
import json
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent
API_BASE_URL = "http://localhost:8000"
TEST_VIDEO_PATH = BASE_DIR / "input_videos" / "fswing.mp4"  # Path to your test video

def test_api():
    """Test the FastAPI endpoints"""
    
    print("Starting API Tests...")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on port 8000")
        print("Run: uvicorn main:app --reload")
        return
    
    # Test 2: List pro videos
    print("\n2. Testing pro videos listing...")
    try:
        response = requests.get(f"{API_BASE_URL}/pro-videos")
        if response.status_code == 200:
            data = response.json()
            pro_videos = data.get("pro_videos", [])
            print(f"✅ Found {len(pro_videos)} pro videos")
            
            if pro_videos:
                print("Available pro videos:")
                for video in pro_videos:
                    print(f"  - {video['display_name']} ({video['filename']})")
                
                # Select first pro video for testing
                selected_pro = pro_videos[0]['filename']
                print(f"📹 Will use '{selected_pro}' for testing")
            else:
                print("⚠️  No pro videos found. Please add some .mp4 files to the pro_videos folder")
                return
        else:
            print(f"❌ Failed to list pro videos: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error listing pro videos: {e}")
        return
    
    # Test 3: Storage info
    print("\n3. Testing storage info...")
    try:
        response = requests.get(f"{API_BASE_URL}/storage-info")
        if response.status_code == 200:
            info = response.json()
            print("✅ Storage info retrieved:")
            print(f"  - Pro videos: {info['pro_videos_count']}")
            print(f"  - Pro CSVs: {info['pro_csvs_count']}")
            print(f"  - Output videos: {info['output_videos_count']}")
            print(f"  - Temp files: {info['temp_files_count']}")
        else:
            print(f"❌ Failed to get storage info: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting storage info: {e}")
    
    # Test 4: Video processing (only if test video exists)
    if Path(TEST_VIDEO_PATH).exists():
        print(f"\n4. Testing video processing with {TEST_VIDEO_PATH}...")
        try:
            # turn path to string bc we use BASE_DIR
            with open(str(TEST_VIDEO_PATH), 'rb') as video_file:
                files = {'user_video': (TEST_VIDEO_PATH.name, video_file, 'video/mp4')}
                data = {'pro_video_name': selected_pro}
                
                print("Uploading and processing video...")
                response = requests.post(
                    f"{API_BASE_URL}/process-comparison",
                    files=files,
                    data=data,
                    timeout=300  # 5 minute timeout for processing
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Video processing completed!")
                    print(f"  - Session ID: {result['session_id']}")
                    print(f"  - Output filename: {result['output_filename']}")
                    print(f"  - Download URL: {API_BASE_URL}{result['download_url']}")
                    
                    # Test download
                    print("\n5. Testing video download...")
                    download_response = requests.get(f"{API_BASE_URL}{result['download_url']}")
                    if download_response.status_code == 200:
                        print("✅ Video download successful!")
                        print(f"  - Downloaded {len(download_response.content)} bytes")
                        
                        # Save downloaded video to output_videos/ and replace the original
                        output_filename = result['output_filename']
                        output_dir = BASE_DIR / "output_videos"
                        final_output_path = output_dir / output_filename

                        # Overwrite the existing file
                        with open(final_output_path, 'wb') as f:
                            f.write(download_response.content)

                        print(f"✅ Downloaded and saved over: {final_output_path}")

                        # Delete duplicate in backend folder if it exists
                        downloaded_duplicate = BASE_DIR / f"downloaded_{output_filename}"
                        if downloaded_duplicate.exists():
                            downloaded_duplicate.unlink()
                            print(f"🗑️  Deleted duplicate: {downloaded_duplicate}")
                    else:
                        print(f"❌ Download failed: {download_response.status_code}")
                else:
                    print(f"❌ Video processing failed: {response.status_code}")
                    try:
                        error_detail = response.json()
                        print(f"Error details: {error_detail}")
                    except:
                        print(f"Response text: {response.text}")
        except Exception as e:
            print(f"❌ Error during video processing: {e}")
    else:
        print(f"\n4. ⚠️  Skipping video processing test - {TEST_VIDEO_PATH} not found")
        print("   Create a test video file to test video processing")
    
    print("\n🏁 API Tests completed!")

# def create_test_setup_instructions():
#     """Print setup instructions for testing"""
#     print("\n" + "="*60)
#     print("📋 TEST SETUP INSTRUCTIONS")
#     print("="*60)
#     print("""
# To fully test the API, you need:

# 1. 📁 Directory structure:
#    backend/
#    ├── main.py (the FastAPI app)
#    ├── model.py (your existing file)
#    ├── data_extract.py (your existing file)
#    ├── pro_videos/ (folder with .mp4 professional videos)
#    ├── pro_csv/ (will be auto-created)
#    ├── input_videos/ (not needed for API)
#    ├── output_videos/ (will be auto-created)
#    └── temp/ (will be auto-created)

# 2. 🎬 Add professional videos:
#    - Place at least one .mp4 file in the pro_videos/ folder
#    - These will be shown to users for selection

# 3. 🧪 For testing video processing:
#    - Place a test video file named 'test_user_video.mp4' in the same directory as this test script

# 4. 🚀 Start the API server:
#    cd backend
#    pip install fastapi uvicorn python-multipart
#    uvicorn api:app --reload

# 5. 🔍 Run this test:
#    python test_api.py
# """)

if __name__ == "__main__":
    #create_test_setup_instructions()
    
    # Ask user if they want to proceed with tests
    response = input("\nDo you want to run the API tests now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        test_api()
    else:
        print("Tests skipped. Run this script again when ready!")