from aiogram import Bot
import logging

async def is_user_subscribed(bot: Bot, user_id, channels):
    for channel in channels:
        try:
            member = await bot.get_chat_member(channel, user_id)
            #logging.info(f"Checking membership for user {user_id} in channel {channel}: {member.status}")
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            #logging.error(f"Error checking subscription for user {user_id} in channel {channel}: {e}")
            return False
    return True