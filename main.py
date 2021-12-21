import asyncio
import aiogram
import logging
from aiogram import types
import os

logging.basicConfig(level=logging.INFO)

async def main():
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    bot = aiogram.Bot(TELEGRAM_API_TOKEN)
    dispatcher = aiogram.Dispatcher(bot)

    @dispatcher.message_handler()
    async def echo(message: types.Message):
        await message.answer(message.text)

    logging.info("Starting bot")
    await dispatcher.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
