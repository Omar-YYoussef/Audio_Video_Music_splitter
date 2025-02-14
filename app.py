# here, you should call the home.py 

import streamlit as st
import tempfile
import os
from pathlib import Path
from app.processors.video_processor import VideoProcessor
from app.processors.audio_processor import AudioProcessor
from app.processors.link_processor import LinkDownloader
# Initialize session state for tracking processing status
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "URL Processing 🔗"


# Utility functions
def save_uploaded_file(uploaded_file, temp_dir):
    file_path = Path(temp_dir) / uploaded_file.name
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    return file_path


def download_file_button(file_path, label, file_name, mime_type):
    with open(file_path, 'rb') as f:
        if st.download_button(
                label=label,
                data=f.read(),
                file_name=file_name,
                mime=mime_type
        ):
            # Reset the processing state after download
            st.session_state.processing_complete = False
            st.experimental_rerun()


def reset_processing_state():
    st.session_state.processing_complete = False


def process_audio(audio_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = save_uploaded_file(audio_file, temp_dir)
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir(exist_ok=True)

        with st.spinner("Processing audio..."):
            try:
                audio_proc = AudioProcessor(input_path, output_dir)
                if not audio_proc.run_demucs():
                    raise RuntimeError("Demucs processing failed.")

                vocals_path = audio_proc.get_vocals_path()
                no_vocals_path = audio_proc.get_no_vocals_path()

                if not vocals_path or not no_vocals_path:
                    raise FileNotFoundError("Processed files not found.")

                col1, col2 = st.columns(2)
                with col1:
                    download_file_button(
                        vocals_path,
                        "Download Vocals",
                        f"vocals_{audio_file.name.rsplit('.', 1)[0]}.wav",
                        "audio/wav"
                    )

                st.success("Audio processing completed!")
                st.session_state.processing_complete = True

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                reset_processing_state()


def process_video(video_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = save_uploaded_file(video_file, temp_dir)
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir(exist_ok=True)

        with st.spinner("Processing video..."):
            try:
                video_proc = VideoProcessor(input_path, output_dir)
                audio_path = video_proc.extract_audio()
                if not audio_path:
                    raise RuntimeError("Audio extraction from video failed.")

                audio_proc = AudioProcessor(audio_path, output_dir)
                if not audio_proc.run_demucs():
                    raise RuntimeError("Demucs processing failed.")

                vocals_path = audio_proc.get_vocals_path()
                no_vocals_path = audio_proc.get_no_vocals_path()
                if not vocals_path or not no_vocals_path:
                    raise FileNotFoundError("Processed audio files not found.")

                final_video_path = video_proc.combine_video_audio(vocals_path)

                col1, col2 = st.columns(2)
                if final_video_path:
                    with col1:
                        download_file_button(
                            final_video_path,
                            "Download Processed Video",
                            f"processed_{video_file.name}",
                            "video/mp4"
                        )
                with col2:
                    download_file_button(
                        vocals_path,
                        "Download Vocals",
                        f"vocals_{video_file.name.rsplit('.', 1)[0]}.wav",
                        "audio/wav"
                    )

                st.success("Video processing completed!")
                st.session_state.processing_complete = True

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                reset_processing_state()


def process_url(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            output_dir = Path(temp_dir) / "downloaded"
            output_dir.mkdir(exist_ok=True)

            with st.spinner("Downloading video..."):
                downloader = LinkDownloader(output_dir)
                video_path = downloader.download_from_url(url)

                if not video_path:
                    st.error("Video download failed")
                    return

                # Add extensive logging and checks
                #st.write(f"Downloaded video path: {video_path}")
                #st.write(f"Video file exists: {os.path.exists(video_path)}")

                try:
                    video_file_size = os.path.getsize(video_path)
                    #
                    #(f"Video file size: {video_file_size} bytes")

                    if video_file_size == 0:
                        st.error("Downloaded video file is empty")
                        return
                except Exception as size_error:
                    st.error(f"Error checking file size: {size_error}")
                    return

            # Rest of the processing remains the same...
            st.info("Processing video...")
            process_dir = Path(temp_dir) / "output"
            process_dir.mkdir(exist_ok=True)

            video_proc = VideoProcessor(video_path, process_dir)
            audio_path = video_proc.extract_audio()

            if not audio_path:
                st.error("Audio extraction failed")
                return

            st.info("Separating vocals...")
            audio_proc = AudioProcessor(audio_path, process_dir)
            if not audio_proc.run_demucs():
                st.error("Demucs processing failed")
                return

            vocals_path = audio_proc.get_vocals_path()
            no_vocals_path = audio_proc.get_no_vocals_path()

            if not vocals_path or not no_vocals_path:
                st.error("Processed audio files not found")
                return

            st.info("Creating final video...")
            final_video_path = video_proc.combine_video_audio(vocals_path)

            if not final_video_path:
                st.error("Final video creation failed")
                return

            col1, col2 = st.columns(2)
            if final_video_path:
                with col1:
                    download_file_button(
                        final_video_path,
                        "Download Processed Video",
                        "processed_video.mp4",
                        "video/mp4"
                    )

            if vocals_path:
                with col2:
                    download_file_button(
                        vocals_path,
                        "Download Vocals",
                        "vocals.wav",
                        "audio/wav"
                    )

            st.success("Video processing completed!")
            st.session_state.processing_complete = True

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            import traceback
            traceback.print_exc()  # This will print the full traceback


# Page config
st.set_page_config(
    page_title="🎵 Audio/Video Music Separator",
    page_icon="🎵",
    layout="wide"
)

# Main App Layout
st.title("🎵 Audio/Video Music Separator")

# Tabs for different processing types
tab1, tab2, tab3 = st.tabs(["URL Processing 🔗", "Audio Processing 🎧", "Video Processing 🎥"])

with tab1:
    st.header("Process Video from URL")
    with st.expander("Instructions", expanded=True):
        st.markdown("""
        1. Paste a video URL from Facebook, or other supported platforms
        2. Click the **Process URL** button
        3. Download the processed video or vocals
        """)

    if not st.session_state.processing_complete:
        url = st.text_input("Enter video URL")
        if url and st.button("Process URL"):
            process_url(url)

with tab2:
    st.header("Process Your Audio File")
    with st.expander("Instructions", expanded=True):
        st.markdown("""
        1. Upload an audio file in MP3, WAV, or OGG format
        2. Click the **Process Audio** button
        3. Download the separated vocals
        """)

    if not st.session_state.processing_complete:
        audio_file = st.file_uploader("Upload your audio file", type=['mp3', 'wav', 'ogg'])
        if audio_file and st.button("Process Audio"):
            process_audio(audio_file)

with tab3:
    st.header("Process Your Video File")
    with st.expander("Instructions", expanded=True):
        st.markdown("""
        1. Upload a video file in MP4, MKV, or AVI format
        2. Click the **Process Video** button
        3. Download the processed video or vocals
        """)

    if not st.session_state.processing_complete:
        video_file = st.file_uploader("Upload your video file", type=['mp4', 'mkv', 'avi'])
        if video_file and st.button("Process Video"):
            process_video(video_file)

# Add a reset button when processing is complete
if st.session_state.processing_complete:
    if st.button("Process Another File"):
        reset_processing_state()
        st.experimental_rerun()


# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This app helps you separate vocals from music in your audio and video files.

    ### Features:
    - Process videos from URLs
    - Upload and process audio files
    - Upload and process video files
    - Extract vocals
    - Download processed files
    - Click process another file
    """)

# Footer
st.markdown("""
---
Made with ❤️ using [Streamlit](https://streamlit.io)
""")