from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from dotenv import load_dotenv

import os
import random

load_dotenv()

bot = Bot(token=os.environ.get('GUESS_NUMBER_TOKEN'))
dp = Dispatcher()

ATTEMPTS = 5

user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}


def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(
        text='Сыграем в игру "Угадай число"?\n'
             'Чтобы узнать правила, отправь команду /help'
    )

if __name__ == '__main__':
    dp.run_polling(bot)
