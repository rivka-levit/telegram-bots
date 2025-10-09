from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from environs import Env

env = Env()
env.read_env()

bot = Bot(token=env('TEST_BOT_TOKEN'))
dp = Dispatcher()

# Create buttons
button_1 = InlineKeyboardButton(
    text="КНОПКА 1",
    callback_data="button_1_click"
)
button_2 = InlineKeyboardButton(
    text="КНОПКА 2",
    callback_data="button_2_click"
)

# Create keyboard object
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button_1], [button_2]]
)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Это инлайн-кнопки. Нажми на любую!',
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "button_1_click")
async def process_button1_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Была нажата КНОПКА 1',
        reply_markup=callback.message.reply_markup
    )


@dp.callback_query(F.data == "button_2_click")
async def process_button2_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Была нажата КНОПКА 2',
        reply_markup=callback.message.reply_markup
    )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data `button_1_click` или `button_2_click`
@dp.callback_query(F.data.in_({'button_1_click', 'button_2_click'}))
async def process_buttons_callback(callback: CallbackQuery):
    await callback.answer()


if __name__ == '__main__':
    dp.run_polling(bot)
