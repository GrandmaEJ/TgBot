from aiogram import types
from aiogram.dispatcher import Dispatcher
import os
import importlib

def register_command_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['help'])
    async def help_command(message: types.Message):
        query = message.text.split()
        if len(query) == 1:
            # Display names of all commands
            help_text = "Available commands:\n"
            
            command_count = 1
            for filename in os.listdir('src'):
                if filename.endswith('.py') and filename != ['help.py','start.py']:
                    module_name = filename[:-3]
                    try:
                        module = importlib.import_module(f'src.{module_name}')
                        if hasattr(module, 'help'):
                            command_help = module.help()
                            help_text += f"{command_count}. {command_help['name'].split(' ')[0]}\n"
                            command_count += 1
                    except Exception as e:
                        print(f"Error loading help for {module_name}: {e}")

            await message.reply(help_text or "No commands found.")
        
        elif len(query) == 2 and query[1].startswith('-'):
            command_name = query[1].strip('-')
            
            # Display help for a specific command
            try:
                module = importlib.import_module(f'src.{command_name}')
                if hasattr(module, 'help'):
                    command_help = module.help()
                    help_text = f"/{command_name} - {command_help['name']}\n"
                    help_text += f"Author: {command_help['author']}\n"
                    help_text += f"Version: {command_help['v']}\n"
                    help_text += f"Usage: {command_help['usages']}\n"
                    help_text += f"Details: {command_help['details']}\n"
                    help_text += f"\nJoin @grandpa_bot_support for more \n"
                    
                    await message.reply(help_text)
                else:
                    await message.reply(f"No help information available for /{command_name}.")
            except ModuleNotFoundError:
                await message.reply(f"Command /{command_name} not found.")
            except Exception as e:
                print(f"Error loading help for {command_name}: {e}")
                await message.reply(f"Error retrieving help for /{command_name}.")