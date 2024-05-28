import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from search import *

TOKEN = os.getenv("TOKEN")
admins = [897190202]

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: Message):
    admins.append(message.from_user.id)
    await message.reply("Welcome to the Lots Monitoring Bot!")


async def check_lots():
    print("checking lots")
    current_lots = fetch_lots()
    known_lots = load_known_lots()
    new_lots = get_new_lots(current_lots, known_lots)

    if new_lots:
        save_known_lots(current_lots)
        for admin in admins:
            for lot in new_lots:
                await bot.send_message(admin, f"New lot found: {lot['link']}")


async def start_bot():
    await dp.start_polling(bot)
