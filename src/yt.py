def help():
    return {
        "name" : "𝐒𝐨𝐧𝐠 𝐂𝐨𝐦𝐦𝐚𝐧𝐝",
        "author" : "𝐆𝐫𝐚𝐧𝐝𝐩𝐚 𝑬𝐉",
        "v" : "0.1",
        "usages" : "use /song [query/yt_link]",
        "details" : "This Command used for search song from youtube as a audio"
    }


import os
import json
import re
import requests
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from core.lib.yt import async_get_video_links
from tempfile import NamedTemporaryFile
import asyncio


# YouTube Data API Key
with open('config.json') as f:
    config = json.load(f)

# Constants
API_KEY = config["google_api"]




SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos'
CHANNEL_URL = 'https://www.googleapis.com/youtube/v3/channels'

NSFW_KEYWORDS = ["nsfw", "18+", "adult", "sex", "porn"]

# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

# Check if query contains NSFW keywords
def is_nsfw(query):
    return any(keyword in query.lower() for keyword in NSFW_KEYWORDS)

def search_youtube(query, max_results=1):
    params = {
        'part': 'snippet',
        'q': query,
        'key': API_KEY,
        'maxResults': max_results,
        'type': 'video'
    }
    response = requests.get(SEARCH_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_video_details(video_id):
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': video_id,
        'key': API_KEY
    }
    response = requests.get(VIDEO_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_channel_details(channel_id):
    params = {
        'part': 'snippet,statistics',
        'id': channel_id,
        'key': API_KEY
    }
    response = requests.get(CHANNEL_URL, params=params)
    response.raise_for_status()
    return response.json()

async def download_audio(url, output_path):
    yt_links = await async_get_video_links(url, resolution='audio', download_type='audio')
    audio_url = yt_links['audio_url']
    response = requests.get(audio_url, stream=True)
    response.raise_for_status()

    # Ensure the temp directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

async def handle_song_command(message: types.Message):
    query = message.text.split(maxsplit=1)

    if len(query) < 2:
        await message.reply("Please provide a YouTube link or search query. Usage: /song [link/query]")
        return

    query = query[1].strip()

    if is_nsfw(query):
        await message.reply("This query is not allowed.")
        return

    # Search for videos using YouTube Data API
    search_results = search_youtube(query)
    if not search_results['items']:
        await message.reply("No results found.")
        return

    video_id = search_results['items'][0]['id']['videoId']
    video_details = get_video_details(video_id)['items'][0]
    channel_id = video_details['snippet']['channelId']
    channel_details = get_channel_details(channel_id)['items'][0]

    title = video_details['snippet']['title']
    views = video_details['statistics'].get('viewCount', 'N/A')
    likes = video_details['statistics'].get('likeCount', 'N/A')
    duration = video_details['contentDetails']['duration']
    channel_name = channel_details['snippet']['title']
    subscribers = channel_details['statistics'].get('subscriberCount', 'N/A')

    # Download the audio
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    audio_file_path = os.path.join("temp", f"{sanitize_filename(title)}.mp3")

    try:
        await download_audio(video_url, audio_file_path)

        caption = (
            f"Title: {title}\n"
            f"Channel: {channel_name}\n"
            f"Subscribers: {subscribers}\n"
            f"Views: {views}\n"
            f"Likes: {likes}\n"
            f"Duration: {duration}"
        )

        with open(audio_file_path, 'rb') as audio_file:
            await message.reply_audio(audio_file, caption=caption)
        
        os.remove(audio_file_path)
    except Exception as e:
        await message.reply(f"Failed to download or send audio. Error: {e}")

def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_song_command, Command('song'))