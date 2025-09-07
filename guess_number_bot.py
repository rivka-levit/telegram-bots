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


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а тебе нужно его угадать\nУ тебя есть {ATTEMPTS} '
        'попыток\n\nДоступные команды:\n\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?'
    )


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: {user["total_games"]}\n'
        f'Игр выиграно: {user["wins"]}'
    )


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Игра окончена!\n'
            'Захочешь сыграть снова - пиши ;)'
        )
    else:
        await message.answer(
            'А мы с тобой и так не играем.\n'
            'Захочешь сыграть - пиши 😉'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
