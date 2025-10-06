import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUser,
    KeyboardButtonRequestUsers,
    Message,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from environs import Env

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='#%(levelname)-8s [%(asctime)s] - %(filename)s:%(lineno)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

env = Env()
env.read_env()

logger.info('Creating Bot...')
bot = Bot(token=env('TEST_BOT_TOKEN'))
dp = Dispatcher()
logger.info('Bot created successfully.')

# ------ Create buttons ------

request_user_btn = KeyboardButton(
    text="Выбрать пользователя",
    request_user=KeyboardButtonRequestUser(
        request_id=42,
        user_is_premium=False
    )
)
request_users_btn = KeyboardButton(
    text="Выбрать пользователей",
    request_users=KeyboardButtonRequestUsers(
        request_id=77,
        user_is_premium=False,
        max_quantity=3
    )
)
request_chat_btn = KeyboardButton(
    text="Выбрать чат",
    request_chat=KeyboardButtonRequestChat(
        request_id=1408,
        chat_is_channel=False,
        chat_is_forum=False
    )
)

# ------ Create keyboard ------

kb_builder = ReplyKeyboardBuilder()
kb_builder.row(request_user_btn, request_users_btn, request_chat_btn, width=1)
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)

# ---------- Handlers ----------

@dp.message(CommandStart())
async def process_start_command(message: Message):
    logger.info(f'User {message.from_user.id} started the bot.')
    await message.answer(
        text='Экспериментируем со специальными кнопками',
        reply_markup=keyboard
    )


# Choose one user handler
@dp.message(F.user_shared)
async def process_user_shared(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))


# Choose several users handler
@dp.message(F.users_shared)
async def process_users_shared(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))


# Choose a chat from the list
@dp.message(F.chat_shared)
async def process_chat_shared(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))


if __name__ == '__main__':
    dp.run_polling(bot)
