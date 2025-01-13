from pathlib import Path
import subprocess
import os
import streamlit as st

class VideoProcessor:
    def __init__(self, input_video, output_dir):
        self.input_video = Path(input_video)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_audio = self.output_dir / "extracted_audio.wav"
        self.final_video = self.output_dir / "final_video.mp4"

    def extract_audio(self):
        """Extract audio from video file"""
        try:
            # First, verify the input video file exists and is readable
            if not self.input_video.exists():
                st.error(f"Input video file not found: {self.input_video}")
                return None

            # Print file size and check if it's not empty
            file_size = os.path.getsize(self.input_video)
            #st.info(f"Input video file size: {file_size} bytes")
            if file_size == 0:
                st.error("Input video file is empty")
                return None

            # Ensure output directory exists
            self.temp_audio.parent.mkdir(parents=True, exist_ok=True)

            # Construct FFmpeg command with detailed logging
            command = [
                "ffmpeg",
                "-v", "error",  # Change to error to reduce verbose output
                "-i", str(self.input_video),
                "-vn",  # No video
                "-acodec", "pcm_s16le",  # 16-bit PCM
                "-ar", "44100",  # 44.1kHz sample rate
                "-ac", "2",  # Stereo
                "-y",  # Overwrite output file if it exists
                str(self.temp_audio)
            ]

            # Run FFmpeg command and capture output
            try:
                # Use subprocess.run with timeout to prevent hanging
                process = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=60  # 60 seconds timeout
                )

                # Check for any errors
                if process.returncode != 0:
                    st.error(f"FFmpeg error: {process.stderr}")
                    st.error(f"FFmpeg command: {' '.join(command)}")
                    return None

            except subprocess.TimeoutExpired:
                st.error("Audio extraction timed out")
                return None
            except Exception as e:
                st.error(f"Unexpected error during FFmpeg execution: {str(e)}")
                return None

            # Verify the output audio file exists and is not empty
            if not self.temp_audio.exists():
                st.error("Audio extraction failed: Output file is missing")
                return None

            file_size = os.path.getsize(self.temp_audio)
            if file_size == 0:
                st.error("Audio extraction failed: Output file is empty")
                return None

            #st.success(f"Audio extracted successfully to {self.temp_audio}")
            return str(self.temp_audio)

        except Exception as e:
            st.error(f"Unexpected error during audio extraction: {str(e)}")
            return None

    def combine_video_audio(self, vocals_path):
        """Combine original video with vocals only"""
        try:
            # Verify input files exist
            if not self.input_video.exists():
                st.error(f"Original video not found: {self.input_video}")
                return None
            if not Path(vocals_path).exists():
                st.error(f"Vocals audio not found: {vocals_path}")
                return None

            # Construct FFmpeg command
            command = [
                "ffmpeg",
                "-v", "verbose",  # Enable verbose logging
                "-i", str(self.input_video),
                "-i", vocals_path,
                "-c:v", "copy",  # Copy video stream without re-encoding
                "-c:a", "aac",   # Use AAC codec for audio
                "-b:a", "192k",  # Set audio bitrate
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-y",  # Overwrite output file if it exists
                str(self.final_video)
            ]

            # Run FFmpeg command and capture output
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )

            # Print FFmpeg output for debugging
            print("FFmpeg stdout:", process.stdout)
            print("FFmpeg stderr:", process.stderr)

            # Check if the command was successful
            if process.returncode != 0:
                st.error(f"FFmpeg error during video combination: {process.stderr}")
                return None

            # Verify the output video file exists and is not empty
            if not self.final_video.exists() or os.path.getsize(self.final_video) == 0:
                st.error("Video combination failed: Output file is missing or empty")
                return None

            print(f"Video combined successfully: {self.final_video}")
            return str(self.final_video)

        except Exception as e:
            st.error(f"Error during video combination: {str(e)}")
            print(f"Exception details: {str(e)}")
            return None