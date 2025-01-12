# 🎵 Vocal Separator - Audio/Video Music Splitter 🎵

![image](https://github.com/user-attachments/assets/2b6bd6c4-5e40-4640-bb82-07dea4125868)


---

## 📝 **Description**

**Vocal Separator** is a powerful tool designed to separate vocals from music in audio and video files. Built with Python and Streamlit, this application leverages the **Demucs** machine learning model for high-quality vocal extraction. Whether you're working with audio files, video files, or even video URLs, this tool makes it easy to isolate vocals and download the results.

---

## 🚀 **Features**

- **🎧 Audio Processing**: Upload audio files (MP3, WAV, OGG) and extract vocals with a single click.
- **🎥 Video Processing**: Upload video files (MP4, MKV, AVI) to extract audio, separate vocals, and recombine with the original video.
- **🔗 URL Processing**: Paste a video URL (e.g., YouTube, Facebook) to download, process, and extract vocals directly.
- **📥 Download Results**: Download the processed vocals or final video files effortlessly.
- **🐳 Docker Support**: Easily deploy the application using Docker for seamless compatibility across platforms.

---

## 🛠️ **Technologies Used**

- **Python** 🐍
- **Streamlit** 🎈
- **Demucs** 🎶
- **FFmpeg** 🎥
- **PyTorch** 🔥
- **yt-dlp** 📥
- **Docker** 🐳



## 🛠️ **Installation**

### **Prerequisites**
- Python 3.9+
- Docker (optional)

### **Local Setup**
1. Clone the repository:
   git clone https://github.com/your-username/Omar-YYoussef-Audio_Music_splitter.git
   cd Omar-YYoussef-Audio_Music_splitter
Install dependencies:

pip install -r requirements.txt
Run the application:


streamlit run app.py
Docker Setup
Build the Docker image:


docker build -t vocal-separator .
Run the Docker container:


docker run -p 8501:8501 vocal-separator
Access the app at http://localhost:8501.

🎮 Usage
Audio Processing:

Upload an audio file (MP3, WAV, OGG).

Click Process Audio.

Download the separated vocals.

Video Processing:

Upload a video file (MP4, MKV, AVI).

Click Process Video.

Download the processed video or vocals.

URL Processing:

Paste a video URL (e.g., YouTube, Facebook).

Click Process URL.

Download the processed video or vocals.

📂 Project Structure
Copy
Omar-YYoussef-Audio_Music_splitter/
├── README.md
├── Dockerfile
├── app.py
├── audio_processor.py
├── link_processor.py
├── requirements.txt
└── video_processor.py
🤝 Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a pull request.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.


🙏 Acknowledgments
Demucs for the vocal separation model.

Streamlit for the amazing web app framework.

FFmpeg for audio/video processing.

yt-dlp for video downloading.
