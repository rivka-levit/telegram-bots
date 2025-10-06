import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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

BOT_TOKEN = env('TEST_BOT_TOKEN')

logger.info('Test bot starting...')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

kb_builder = ReplyKeyboardBuilder()
contact_btn = KeyboardButton(
    text='Send Phone Number',
    request_contact=True
)
geo_btn = KeyboardButton(
    text='Send Geo Location',
    request_location=True
)
kb_builder.row(contact_btn, geo_btn, width=1)

# Create keyboard object
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)


# Command /start handler
@dp.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(
        text='Special buttons experiment',
        reply_markup=keyboard
    )


# Contact sent handler
@dp.message(F.contact)
async def process_contact(message: Message):
    await message.answer(
        text=f'Your Phone Number is {message.contact.phone_number}',
    )
    print(message.model_dump_json(indent=2, exclude_none=True))


# Geolocation sent handler
@dp.message(F.location)
async def process_location(message: Message):
    await message.answer(
        text=f'Your Location is {message.location.latitude}, {message.location.longitude}',
    )
    print(message.model_dump_json(indent=2, exclude_none=True))


if __name__ == '__main__':
    dp.run_polling(bot)
