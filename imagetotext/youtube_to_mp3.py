import os
from pytube import YouTube

def youtube_to_mp3(url):
    youtube = YouTube(url)

    # extracting audio
    vid = youtube.streams.filter(only_audio=True).first()

    destination = "."

    # downloading 
    out_file = vid.download(output_path=destination)
    os.rename(out_file, "audio_file.mp3")