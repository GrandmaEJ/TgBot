def help():
    return {
        "name": "𝐈𝐦𝐚𝐠𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝",
        "author": "𝐆𝐫𝐚𝐧𝐝𝐩𝐚 𝑬𝐉",
        "v": "0.1",
        "usages": "use /img [query] -[limit] ",
        "details": "This Command is used for download images"
    }

import os
import requests
from io import BytesIO
from PIL import Image
from aiogram import types
from aiogram.dispatcher import Dispatcher
from core.lib.img import fetch_images

# List of NSFW keywords
NSFW_KEYWORDS = [
    'nsfw', 
    'adult', 
    'porn', 
    'sex', 
    'nude', 
    'xxx', 
    'explicit',
    'pussy',
    'dick',
    'fuck',
    'fucked',
    'boob',
    'boobes',
    'boobe',
    'hentai',
    'hantai',
    'hantei',
    '18+',
    'erotic'
    ]

def is_valid_image(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image.verify()  # Verifies that the image file is valid
        return True
    except Exception as e:
        print(f"Image verification failed for {url}: {e}")
        return False

def register_command_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['image'])
    async def img_search(message: types.Message):
        query = message.text.split()
        
        if len(query) < 2:
            await message.reply("Please provide a search query and limit. Usage: /image [query] -[limit]")
            return
        
        limit = 1
        
        if '-' in query[-1]:
            try:
                limit = int(query[-1].strip('-'))
                query = query[1:-1]
            except ValueError:
                query = query[1:]
        
        search_query = " ".join(query)
        
        # Check for NSFW keywords in the query
        if any(nsfw_word in search_query.lower() for nsfw_word in NSFW_KEYWORDS):
            await message.reply("Your search query contains NSFW content, which is not allowed.")
            return
        
        await message.reply(f"Searching for {search_query} with a limit of {limit} images...")
        
        image_urls = fetch_images(search_query, limit)
        valid_images = []

        # Validate images
        for url in image_urls:
            if is_valid_image(url):
                valid_images.append(url)
                if len(valid_images) >= limit:
                    break
        
        if not valid_images:
            await message.reply("No valid images found.")
            return
        # 10 batch
        for i in range(0, len(valid_images), 10):
            media = [types.InputMediaPhoto(url) for url in valid_images[i:i+10]]
            await message.answer_media_group(media)
        
        if len(valid_images) < limit:
            await message.reply(f"Only {len(valid_images)} valid images found. Some images may not be valid. Apologies for the inconvenience.")