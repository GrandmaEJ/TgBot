import os
import re
from pytubefix import Playlist, YouTube
from tenacity import retry, stop_after_attempt, wait_fixed
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

# Function to get download URL
def get_download_url(stream):
    return stream.url

# Function to download playlist
def get_playlist_links(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    links = []
    for index, video in enumerate(playlist.videos, start=1):
        yt = YouTube(video.watch_url)
        video_stream = yt.streams.filter(res=resolution).first()
        if not video_stream:
            video_stream = yt.streams.get_highest_resolution()
        audio_stream = yt.streams.get_audio_only()
        links.append({
            "video_title": yt.title,
            "video_url": get_download_url(video_stream),
            "audio_url": get_download_url(audio_stream)
        })
    return links

# Function to get video download URL
def get_video_links(url, resolution, download_type):
    yt = YouTube(url)
    video_stream = yt.streams.filter(res=resolution).first()
    if not video_stream:
        video_stream = yt.streams.get_highest_resolution()
    audio_stream = yt.streams.get_audio_only()

    if download_type == 'audio':
        return {"title": yt.title, "audio_url": get_download_url(audio_stream)}
    elif download_type == 'video':
        return {"title": yt.title, "video_url": get_download_url(video_stream)}
    else:  # both
        return {
            "title": yt.title,
            "video_url": get_download_url(video_stream),
            "audio_url": get_download_url(audio_stream)
        }

# Asynchronous function to handle download links using ThreadPoolExecutor
async def async_get_video_links(url, resolution, download_type):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, get_video_links, url, resolution, download_type)

async def async_get_playlist_links(url, resolution):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, get_playlist_links, url, resolution)