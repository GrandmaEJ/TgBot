from aiogram import types
from aiogram.dispatcher import Dispatcher

def register_command_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        await message.answer("Hello! Welcome to our bot. Use /help to see available commands.")