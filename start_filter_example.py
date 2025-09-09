"""
Custom realization of /start command filter.
"""

from aiogram import Bot, Dispatcher
from aiogram.types import Message

BOT_TOKEN = 'BOT_TOKEN'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def start_filter(message: Message):
    return message.text and message.text.startswith('/start')


@dp.message(start_filter)
async def process_start_command(message: Message):
    await message.answer('This is the start command')


if __name__ == '__main__':
    dp.run_polling(bot)
