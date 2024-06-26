import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from search import *

load_dotenv()

TOKEN = os.getenv("TOKEN")
admins = {897190202, 6550273340}

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: Message):
    print(f"{message.from_user.id} started bot")
    admins.add(message.from_user.id)
    await message.reply("Добро пожаловать на бот мониторинга лотов")


async def check_lots():
    print("checking lots")
    current_lots = fetch_lots()
    known_lots = load_known_lots()
    new_lots = get_new_lots(current_lots, known_lots)

    if new_lots:
        save_known_lots(current_lots)
        for admin in admins:
            for lot in new_lots:
                print(f"Sending message to {admin}: {lot['id']}")
                await bot.send_message(admin, f"Найден новый лот: {lot['link']}")


async def start_bot():
    await dp.start_polling(bot)
