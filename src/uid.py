def help():
    return {
        "name" : "𝐔𝐢𝐝 𝐂𝐨𝐦𝐦𝐚𝐧𝐝",
        "author" : "𝐆𝐫𝐚𝐧𝐝𝐩𝐚 𝑬𝐉",
        "v" : "0.1",
        "usages" : "use /uid ",
        "details" : "This Command used for getting Profile Image , Uid , Usename, Name"
    }

from aiogram import types
from aiogram.dispatcher import Dispatcher

def register_command_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['uid'])
    async def cmd_uid(message: types.Message):
        user = message.from_user
        user_id = user.id
        name = user.full_name
        username = f"@{user.username}" if user.username else "𝙽𝚞𝚕𝚕"
        bio = user.bio if hasattr(user, 'bio') and user.bio else "𝙽𝚞𝚕𝚕"

        user_info = (
            f"\n\n𝐔𝐈𝐃    : <code>{user_id}</code>\n"
            f"𝐍𝐚𝐦𝐞  : {name}\n\n"
            f"𝐔𝐬𝐞𝐫𝐍𝐚𝐦𝐞 : {username}\n"
            f"𝐁𝐈𝐎       : {bio}\n"
        )

        
        
        # Fetch the user's profile photos
        user_photos = await message.bot.get_user_profile_photos(user_id, limit=1)

        if user_photos.total_count > 0:
            photo = user_photos.photos[0][0]  # Get the first photo in the first photo group
            await message.answer_photo(photo.file_id, caption=user_info, parse_mode=types.ParseMode.HTML)
        else:
            await message.answer("𝚈𝚘𝚞 𝚑𝚊𝚟𝚎𝚗'𝚝 𝙿𝚛𝚘𝚏𝚒𝚕𝚎 𝙿𝚑𝚘𝚝𝚘 .")
            await message.answer(user_info, parse_mode=types.ParseMode.HTML)