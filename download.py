from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from catolog import *
import sys
import os
import traceback
import json
load_dotenv(".env")
download = os.getenv("DOWNLOAD")
ytb_link = ["https://www.youtube.com/watch?v=", "https://music.youtube.com/watch?v=", "https://music.youtube.com/playlist?list=", "https://www.youtube.com/playlist?list=", "https://youtu.be/"]
#catalog = read_json()

ydl_opts = {
    'ffmpeg_location' : "/usr/bin/ffmpeg",  # Path to ffmpeg executable
    'no_post_overwrites': True,
    'ignoreerrors': True,
    'format': 'bestvideo+bestaudio',  # Select best audio quality
    'outtmpl': download + '/%(uploader)s - %(title)s.%(ext)s',  # Save file with the title of the video
    'postprocessors': [{  # Add post-processor to convert to mp3
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
}

def download_url(url):
    try:
        with YoutubeDL (ydl_opts) as dwld:
            dwld.download(url)
            """
            info = dwld.extract_info(url, download=False)
            if ("playlist?list" in url):
                urls = [entry['id'] for entry in info['entries']]
            else:
                urls = [info['id']]
            """ 
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else input("Enter YouTube URL: ")
    if not url.startswith(tuple(ytb_link)):
        print("Invalid YouTube URL. Please provide a valid link.")
        sys.exit(1)
    download_url(url)
    