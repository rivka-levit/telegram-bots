import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo
)

from environs import Env

env = Env()
env.read_env()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='#%(levelname)-8s [%(asctime)s] - %(filename)s:%(lineno)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger.info('Creating Bot...')
bot = Bot(token=env('TEST_BOT_TOKEN'))
dp = Dispatcher()
logger.info('Bot created successfully.')

# Create button
web_app_btn = KeyboardButton(
    text='Start Web App',
    web_app=WebAppInfo(url="https://stepik.org/")
)

# Create keyboard
keyboard = ReplyKeyboardMarkup(
    keyboard=[[web_app_btn]],
    resize_keyboard=True
)


@dp.message(Command(commands='web_app'))
async def process_web_app_command(message: Message):
    logger.info('Processing Web App...')
    await message.answer(
        text='Экспериментируем со специальными кнопками',
        reply_markup=keyboard
    )


if __name__ == '__main__':
    dp.run_polling(bot)
