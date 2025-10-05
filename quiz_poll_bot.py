from aiogram import Bot, Dispatcher, F
from aiogram.enums import PollType
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    KeyboardButtonPollType,
    Message,
    PollAnswer,
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

bot = Bot(token=env('TEST_BOT_TOKEN'))
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


@dp.message(CommandStart())
async def process_start(message: Message):
    await message.answer(
        text="Let's experiment with special buttons",
        reply_markup=keyboard
    )


@dp.message(F.poll.type == PollType.QUIZ)
async def process_poll_quiz(message: Message):
    await message.answer_poll(
        question=message.poll.question,
        options=[opt.text for opt in message.poll.options],
        is_anonymous=False,
        type=message.poll.type,
        correct_option_id=message.poll.correct_option_id,
        explanationf=message.poll.explanation,
        explanation_entities=message.poll.explanation_entities,
        message_effect_id='5104841245755180586'
    )


@dp.message(F.poll.type == PollType.REGULAR)
async def process_poll_regular(message: Message):
    await message.answer_poll(
        question=message.poll.question,
        options=[opt.text for opt in message.poll.options],
        is_anonymous=False,
        type=message.poll.type,
        allows_multiple_answers=message.poll.allows_multiple_answers,
        message_effect_id='5107584321108051014'
    )


@dp.poll_answer()
async def process_answer_poll(poll_answer: PollAnswer):
    print(poll_answer.model_dump_json(indent=2, exclude_none=True))


# @dp.message(F.poll)
# async def process_poll(message: Message):
#     print(message.model_dump_json(indent=4, exclude_none=True))


if __name__ == '__main__':
    dp.run_polling(bot)
