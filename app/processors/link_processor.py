from pathlib import Path
import yt_dlp
import tempfile
import streamlit as st
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
import re
import os


class LinkDownloader:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_filename(self, title):
        """Sanitize filename by removing special characters and limiting length"""
        # Replace special characters with underscore
        clean_name = re.sub(r'[^a-zA-Z0-9.]', '_', title)
        # Limit length
        if len(clean_name) > 50:
            clean_name = clean_name[:50]
        return clean_name

    def download_from_url(self, url):
        """Download video from URL using yt-dlp"""
        try:
            # Create a temporary filename template
            temp_filename = 'downloaded_video.%(ext)s'
            temp_filepath = str(self.output_dir / temp_filename)

            # Configure yt-dlp options
            ydl_opts = {
                'format': 'best',
                'outtmpl': temp_filepath,
                'quiet': False,  # Enable output for debugging
                'no_warnings': False,
                'extract_audio': False,
            }

            st.info("Starting video download...")
            print(f"Download directory: {self.output_dir}")
            print(f"Download template: {temp_filepath}")

            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                # Get the actual extension
                ext = info.get('ext', 'mp4')

                # Download the video
                ydl.download([url])

                # Construct the actual file path
                actual_filepath = str(self.output_dir / f"downloaded_video.{ext}")
                print(f"Expected downloaded file: {actual_filepath}")

                # Verify file exists
                if not os.path.exists(actual_filepath):
                    print(f"Files in directory: {os.listdir(self.output_dir)}")
                    raise FileNotFoundError(f"Downloaded file not found at {actual_filepath}")

                print(f"File size: {os.path.getsize(actual_filepath)} bytes")
                return actual_filepath

        except Exception as e:
            st.error(f"Error during download: {str(e)}")
            print(f"Download error details: {str(e)}")
            return None