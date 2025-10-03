import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


BOT_TOKEN = 'BOT TOKEN HERE'

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
keyword: ReplyKeyboardMarkup = kb_builder.as_markup(request_keyboard=True)


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
