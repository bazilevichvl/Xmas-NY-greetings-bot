import asyncio
import logging
import sys
import os
import aiogram
from aiogram import types
from aiogram.utils.callback_data import CallbackData
import psycopg2

logging.basicConfig(level=logging.INFO)

review_callback_data = CallbackData("post", "id", "action")

async def main():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        logging.error("Postgres database URL is not specified")
        sys.exit(-1)

    db = psycopg2.connect(DATABASE_URL)
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    if not TELEGRAM_API_TOKEN:
        logging.error("Telegram API token is not specified")
        sys.exit(-1)

    ADMIN_ID = os.getenv("ADMIN_ID")
    if not ADMIN_ID:
        logging.error("Admin ID is not specified")
        sys.exit(-1)

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
Используй команду /greet, чтобы отправить поздравление.\n

Ты будешь получать поздравления от случайных пользователей, так что не забудь
позвать твоих друзей, чтобы увеличить количество отправляемых и получаемых
поздравлений:)
        """)

    @dispatcher.message_handler(commands=["greet"])
    async def greet(message: types.Message):
        # Extract greeting text
        text = message.get_args().strip()
        if len(text) == 0:
            await message.answer("Это все, что ты можешь мне сказать?(")
        else:
            # Save to db
            greeting_id = -1
            with db.cursor() as curr:
                curr.callproc("store_greeting", [text])
                greeting_id = curr.fetchone()[0]
            db.commit()
            logging.info(f"New greeting {greeting_id}")

            # Send for approval
            buttons = [
                        types.InlineKeyboardButton(text="👍", callback_data=review_callback_data.new(id=greeting_id, action="approve")),
                        types.InlineKeyboardButton(text="👎", callback_data=review_callback_data.new(id=greeting_id, action="reject"))
                      ]
            kb = types.InlineKeyboardMarkup(row_width=2)
            kb.add(*buttons)
            await bot.send_message(ADMIN_ID, f"#{greeting_id}\n{text}", reply_markup=kb)

    @dispatcher.message_handler()
    async def echo(message: types.Message):
        await message.answer(
            f"Я тебя не понимаю, {message.from_user.full_name}"
        )

    @dispatcher.callback_query_handler(review_callback_data.filter())
    async def callbacks_approval(call: types.CallbackQuery, callback_data):
        uid = call.from_user.id
        if uid != ADMIN_ID:
            return
        greeting_id = callback_data["greeting_id"]
        action = callback_data["action"]
        logging.info(f"Handling callback {action}#{greeting_id}")
        if action == "approve":
            # get text
            text = ""
            uid = -1
            with db.cursor() as curr:
                curr.callproc("get_greeting", [greeting_id])
                text = curr.fetchone()[0]
                curr.callproc("get_random_user", [])
                uid = curr.fetcone()[0]
            # send to random user
            await bot.send_message(uid, text)

        with db.cursor() as curr:
            curr.callproc("remove_greeting", [greeting_id])
        db.commit()

        await call.answer("", markdown=types.reply_keyboard.ReplyKeyboardRemove())

    logging.info("Starting bot")
    await dispatcher.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
