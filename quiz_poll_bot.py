from aiogram import Bot, Dispatcher, F
from aiogram.enums import PollType
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    KeyboardButtonPollType,
    Message,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from environs import Env

import logging
import sys

env = Env()
env.read_env()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(levelname)-8s [%(asctime)s] - %(filename)s:%(lineno)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

bot = Bot(token=env('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

# Create buttons
poll_quiz_btn = KeyboardButton(
    text='Создать опрос/викторину',
    request_poll=KeyboardButtonPollType()
)
poll_btn = KeyboardButton(
    text='Создать опрос',
    request_poll=KeyboardButtonPollType(type=PollType.REGULAR)
)
quiz_btn = KeyboardButton(
    text='Создать викторину',
    request_poll=KeyboardButtonPollType(type=PollType.QUIZ)
)

# Create keyboard
kb_builder = ReplyKeyboardBuilder()
kb_builder.row(poll_quiz_btn, poll_btn, quiz_btn, width=1)
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)

