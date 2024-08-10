def help():
    return {
        "name" : "𝐓𝐫𝐚𝐧𝐬𝐥𝐚𝐭𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝",
        "author" : "𝐆𝐫𝐚𝐧𝐝𝐩𝐚 𝑬𝐉",
        "v" : "0.1",
        "usages" : "/translate [text] [lang_code] ",
        "details" : "This Command for translate text"
    }

from aiogram import types
from aiogram.dispatcher import Dispatcher

import requests



DEFAULT_LANG_CODE = 'bn' 

def translate_text(text, lang_code):
    url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={lang_code}&dt=t&q={requests.utils.quote(text)}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0][0][0]
    else:
        return "Error: Translation failed"



def register_command_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['translate'])

    async def handle_translate(message: types.Message):
        # Extract command arguments
        args = message.get_args().strip()
    
        if not args:
            await message.reply("Please provide text to translate. Usage: /translate [text] [-lang_code]")
            return
    
        # Default language code
        lang_code = DEFAULT_LANG_CODE
    
        # If text contains multiple lines or no language code specified
        if '\n' in args:
            text = args
        else:
            # Check if lang_code is provided in the text
            if ' ' in args and args[-3] == '-':
                lang_code = args[-2:]
                text = args[:-3].strip()
            else:
                # Split text and possible lang_code
                parts = args.split(' ')
                if len(parts) == 2 and len(parts[1]) == 2:
                    text, lang_code = parts
                else:
                    text = args
    
        translated_text = translate_text(text, lang_code)
        await message.reply(f"Translated Text:\n{translated_text}")

