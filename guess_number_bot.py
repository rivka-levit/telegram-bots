from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from dotenv import load_dotenv

import os
import random

load_dotenv()

bot = Bot(token=os.environ.get('GUESS_NUMBER_TOKEN'))
dp = Dispatcher()

ATTEMPTS = 7

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
        user['secret_number'] = None
        user['attempts'] = 0
        await message.answer(
            'Игра окончена!\n'
            'Захочешь сыграть снова - пиши 😉'
        )
    else:
        await message.answer(
            'А мы с тобой и так не играем.\n'
            'Захочешь сыграть - пиши 😉'
        )


@dp.message(F.text.lower().in_([
    'да', 'давай', 'сыграем', 'игра', 'играть', 'играем', 'хочу', 'хочу играть'
]))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        await message.answer(
            'Играем!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру, я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль 😔\nЗахочешь сыграть - пиши!'
        )
    else:
        await message.answer(
            'Мы же играем сейчас. Пиши число от 1 до 100!\n'
            'Хочешь отменить игру? Пришли команду /cancel'
        )


# Handler for numbers 1 to 100 sent by user
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        num = int(message.text)
        if num == user['secret_number']:
            user['in_game'] = False
            user['secret_number'] = None
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer('Бинго! Число угадано! Сыграем еще?')
        elif num > user['secret_number']:
            user['attempts'] -= 1
            await message.answer(
                f'Мое число меньше.\n'
                f'Осталось {user["attempts"]} попыток.'
            )
        elif num < user['secret_number']:
            user['attempts'] -= 1
            await message.answer(
                f'Мое число больше.\n'
                f'Осталось {user["attempts"]} попыток.'
            )
        if user['in_game'] and user['attempts'] == 0:
            secret = user['secret_number']
            user['in_game'] = False
            user['secret_number'] = None
            user['total_games'] += 1
            await message.answer(
                f'Упс... Игра окончена. Попыток больше нет.\n'
                f'Моё число было {secret}\n'
                f'Хочешь попробовать еще раз?'
            )
    else:
        await message.answer('Мы еще не играем. Хочешь сыграть?')


if __name__ == '__main__':
    dp.run_polling(bot)
