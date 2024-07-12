import json
import os
import telegram
from telegram import Bot as TelegramBot
from telegram.error import TelegramError
import asyncio

class Bot:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(script_dir, 'settings.json')
        with open(settings_path, 'r') as f:
            settings = json.loads(f.read())
        self.chat_id = settings['chat_id']
        self.bot = TelegramBot(token=settings['bot_token'])

    async def send_text(self, text):
        try:
            return await self.bot.send_message(chat_id=self.chat_id, text=text)
        except TelegramError as e:
            print(f"Failed to send text message: {e}")
            return None

    async def send_image(self, path):
        try:
            with open(path, 'rb') as f:
                return await self.bot.send_photo(chat_id=self.chat_id, photo=f)
        except TelegramError as e:
            print(f"Failed to send image: {e}")
            return None

    async def delete_msg(self, msg_id):
        try:
            await self.bot.delete_message(chat_id=self.chat_id, message_id=msg_id)
        except TelegramError as e:
            print(f"Failed to delete message: {e}")
