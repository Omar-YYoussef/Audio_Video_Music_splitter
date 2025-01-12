# 🎵 Omar-YYoussef-Audio/Music Splitter 🎶

This Streamlit application allows you to separate vocals from music in audio and video files. It uses the Demucs model for source separation and FFmpeg for audio and video processing. 🎧🎬

![image](https://github.com/user-attachments/assets/d2095eb1-472f-4aa9-9d8b-466eb59deaeb)


## ✨ Features ✨

*   **URL Processing:** Downloads and processes audio from video URLs (Facebook and other platforms supported by yt-dlp). 🔗🌐
*   **Audio Processing:** Upload and process local audio files (MP3, WAV, OGG). 🎧📂
*   **Video Processing:** Upload and process local video files (MP4, MKV, AVI). 🎬🎥
*   **Vocal Extraction:** Separates vocals from the instrumental track. 🎤🎼
*   **Processed File Downloads:** Download the separated vocals, instrumental track, or the processed video with extracted vocals. ⬇️💾
*   **User-Friendly Interface:** Easy-to-use tabbed interface powered by Streamlit. 💻🖱️
*   **Dockerized:** Easily deployable using the provided Dockerfile. 🐳📦

## 🚀 Getting Started 🚀

### ⚙️ Prerequisites ⚙️

*   Docker (if you want to run in a container) 🐳
*   Python 3.9+ (if running locally) 🐍
*   `pip` (Python package installer) 📦

### 🐳 Installation (using Docker) 🐳

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd Omar-YYoussef-Audio_Music_splitter
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t audio-splitter .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 audio-splitter
    ```

    The app will be accessible in your web browser at `http://localhost:8501`. 🌐

### 💻 Installation (Locally) 💻

1.  **Clone the repository:**
    ```bash
     git clone https://github.com/username/Omar-YYoussef-Audio_Music_splitter.git
     cd Omar-YYoussef-Audio_Music_splitter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Make sure you have `ffmpeg` installed on your system.* For Ubuntu/Debian systems, you can install it using:
      ```bash
      sudo apt-get update
      sudo apt-get install ffmpeg
      ```
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The app will be accessible in your web browser at `http://localhost:8501`. 🌐

## 🕹️ Usage 🕹️

The application has three main tabs:

### URL Processing 🔗

1.  Paste the URL of the video you want to process into the text input. ⌨️
2.  Click the "Process URL" button. ▶️
3.  Wait for the video to be downloaded and processed. ⏳
4.  Download the processed video or the separated vocal track when prompted. ⬇️

### Audio Processing 🎧

1.  Upload an audio file (MP3, WAV, or OGG). 📂
2.  Click the "Process Audio" button. ▶️
3.  Wait for the audio to be processed. ⏳
4.  Download the separated vocal track when prompted. ⬇️

### Video Processing 🎥

1.  Upload a video file (MP4, MKV, or AVI). 🎬
2.  Click the "Process Video" button. ▶️
3.  Wait for the video to be processed. ⏳
4.  Download the processed video or the separated vocal track when prompted. ⬇️

After processing is complete, a button will appear that allows you to start the process over with a new file. 🔄


## 🛠️ Technologies Used 🛠️

*   **Python:** Core programming language. 🐍
*   **Streamlit:** Web framework for building interactive apps. 💻
*   **Demucs:** Deep learning model for music source separation. 🧠🎶
*   **FFmpeg:** Multimedia framework for audio and video manipulation. 🎬🔊
*   **yt-dlp:** Command-line program to download videos from websites. 🌐⬇️
*   **Docker:** Containerization platform. 🐳

## 📝 License 📝

[MIT License]

## 🤝 Contributing 🤝

Contributions are welcome! Feel free to submit pull requests or open issues for bugs and feature requests. 💡

## 👨‍💻 Author 👨‍💻

Omar Youssef

## 🙏 Acknowledgments 🙏

*   This application is based on the excellent work of the Demucs and FFmpeg teams. 👏
*   The Streamlit team for providing a great platform for web applications. 💻
