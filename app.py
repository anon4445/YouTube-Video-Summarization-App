import streamlit as st
from moviepy.editor import VideoFileClip
import yt_dlp
import os
import subprocess
from openai import OpenAI

def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192'
            }
        ],
        'outtmpl': '%(title)s.%(ext)s'  
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_path = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')
        
        if not os.path.exists(audio_path):
            st.error("Error: Audio file was not saved properly.")
            return None

        mono_audio_path = audio_path.replace('.wav', '_mono.wav')
        subprocess.run(['ffmpeg', '-i', audio_path, '-ac', '1', mono_audio_path], check=True)

        os.remove(audio_path)

        return mono_audio_path
    except Exception as e:
        st.error(f"Error downloading or processing audio: {e}")
        return None

def transcribe_audio(audio_path):
    server = "grpc.nvcf.nvidia.com:443"
    metadata = {
        "function-id": "d8dd4e9b-fbf5-4fb0-9dba-8cf436c8d965",
        "authorization": "Bearer "
    }
    command = [
        "python", "python-clients/scripts/asr/transcribe_file.py",
        "--server", server,
        "--use-ssl",
        "--metadata", "function-id", metadata["function-id"],
        "--metadata", "authorization", metadata["authorization"],
        "--language-code", "en-US",
        "--input-file", audio_path
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        transcription = result.stdout
        return transcription
    except subprocess.CalledProcessError as e:
        st.error("An error occurred during transcription")
        st.error(e.stderr)
        return None


def summarize_transcription(transcription_text):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=""
    )
    
    completion = client.chat.completions.create(
        model="meta/llama-3.2-3b-instruct",
        messages=[{"role": "user", "content": f"Summarize the following transcription: {transcription_text}"}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    summary = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            summary += chunk.choices[0].delta.content 

    return summary


def main():
    st.title("YouTube Video Summarization")
    with st.form("youtube_form"):
        video_url = st.text_input("Enter a YouTube video URL for transcription and summarization")
        submit_button = st.form_submit_button(label="Process Video")

    if submit_button and video_url:
        st.info("Downloading audio from YouTube video...")
        audio_path = download_youtube_audio(video_url)
        
        if audio_path:
            st.success("Audio downloaded successfully! Starting transcription...")
            transcription = transcribe_audio(audio_path)
            
            if transcription:
                st.info("Generating summary...")
                summary = summarize_transcription(transcription)

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Transcription Result")
                    st.text_area("Transcription", transcription, height=300)

                with col2:
                    st.subheader("Summary")
                    st.text_area("Summary", summary, height=300)

            os.remove(audio_path)

if __name__ == "__main__":
    main()
