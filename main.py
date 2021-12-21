import asyncio
import logging
import os
import aiogram
from aiogram import types
import psycopg2

logging.basicConfig(level=logging.INFO)


async def main():
    DATABASE_URL = os.getenv("DATABASE_URL")
    db = psycopg2.connect(DATABASE_URL)
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    bot = aiogram.Bot(TELEGRAM_API_TOKEN)
    dispatcher = aiogram.Dispatcher(bot)

    @dispatcher.message_handler(commands=["start"])
    async def start(message: types.Message):
        uid = message.from_user.id
        with db.cursor() as curr:
            curr.callproc("register_user", [uid])
        db.commit()
        await message.answer("""
Привет! Я бот для обмена случайными анонимными новогодними поздравлениями!\n
Используй команду /greet, чтобы отправить поздравление.
Используй команду /rand, чтобы получить случайное поздравление.
        """)

    @dispatcher.message_handler()
    async def echo(message: types.Message):
        await message.answer(
            f"Я тебя не понимаю, {message.from_user.full_name}"
        )

    logging.info("Starting bot")
    await dispatcher.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
