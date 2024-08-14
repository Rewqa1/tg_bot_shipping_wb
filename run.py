import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

from bot.handlers import router

load_dotenv('.env')

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

async def main():
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
