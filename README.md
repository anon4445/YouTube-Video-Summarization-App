# YouTube Video Summarization App

This repository provides a Streamlit application for summarizing YouTube video content by:

1. **Downloading** the audio from a YouTube video.
2. **Transcribing** the audio to text using NVIDIA's Automatic Speech Recognition (ASR) API.
3. **Summarizing** the transcription using Meta’s LLaMA model via NVIDIA’s hosted API.

The app uses `yt_dlp` for audio extraction, `ffmpeg` for processing, and NVIDIA’s cloud-hosted APIs for both transcription and summarization.

---

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/yt-video-summarization.git
    cd yt-video-summarization
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    pip install --force-reinstall git+https://github.com/nvidia-riva/python-clients.git
    git clone https://github.com/nvidia-riva/python-clients.git
    ```

3. **Set up your environment**:
   - Install `ffmpeg` and ensure it’s accessible in your system’s PATH.
   - Define the necessary environment variables for NVIDIA’s API access (see [Environment Variables](#environment-variables)).

---

## Usage

1. **Run the Streamlit app**:

    ```bash
    streamlit run app.py
    ```

2. **In the App**:
   - Open the app in your browser (usually at `http://localhost:8501`).
   - Enter a YouTube video URL and click **Process Video**.
   - The transcription and summary will be displayed upon completion.

---

## Environment Variables

Set the following environment variables for API access:

- `NVIDIA_ASR_SERVER_URL`: URL for NVIDIA’s ASR API server.
- `NVIDIA_ASR_API_FUNCTION_ID`: Function ID for ASR processing.
- `NVIDIA_ASR_API_AUTH_TOKEN`: Authorization token for ASR access.
- `NVIDIA_LLAMDA_API_KEY`: API key for the NVIDIA-hosted LLaMA summarization API.

---

## License

This project is licensed under the MIT License.
