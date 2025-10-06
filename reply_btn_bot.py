from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup
)

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('TEST_BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Create buttons
btn_1 = KeyboardButton(text='Собак 🦮')
btn_2 = KeyboardButton(text='Огурцов 🥒')

# Create keyboard object with buttons
keyboard = ReplyKeyboardMarkup(
    keyboard=[[btn_1, btn_2]],
    resize_keyboard=True,
    one_time_keyboard=True,  # collapse keyboard
    input_field_placeholder='Нажмите кнопку с ответом'
)


# Start command handler
@dp.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(
        text='Чего кошки боятся больше?',
        reply_markup=keyboard
    )


# Handler for the answer `Собак 🦮`
@dp.message(F.text=='Собак 🦮')
async def process_dog_answer(message: Message):
    await message.answer(
        text='Да, несомненно, кошки боятся собак. '
             'Но вы видели как они боятся огурцов?',
        # reply_markup=ReplyKeyboardRemove()
    )


# Handler for the answer `Огурцов 🥒`
@dp.message(F.text=='Огурцов 🥒')
async def process_cucumber_answer(message: Message):
    await message.answer(
        text='Да, иногда кажется, что огурцов '
             'кошки боятся больше',
        # reply_markup=ReplyKeyboardRemove()
    )


if __name__ == '__main__':
    dp.run_polling(bot)
