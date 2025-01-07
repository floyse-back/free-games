from aiogram import Bot
from modules.TelegramBot.config import chat_id, API
from models.db_use import db_use

import asyncio
class telegram(db_use):
    def __init__(self):
        super().__init__()
        self.chat_id = chat_id
        self.bot = Bot(token=API)

    async def sendPhoto(self, img, data, url=None):
        try:
            async with self.bot:
                await self.bot.send_photo(photo=f"{img}", caption=f"{data}", chat_id=self.chat_id, parse_mode="Markdown")
                if url:
                    self.insert_message(url)
        except Exception as ex:
            print(f"Error {ex}")

    async def sendMessage(self,text):
        try:
            async with self.bot:
                await self.bot.send_message(text=text,chat_id=self.chat_id,parse_mode="Markdown")
        except Exception as ex:
            print(f"Error {ex}")
