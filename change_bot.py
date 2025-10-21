import requests

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from environs import Env

env = Env()
env.read_env()

USERS = dict()

bot = Bot(
    token=env.str('TEST_BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def convert_amount(base_cur: str, target_cur: str, amount: int | float) -> float:
    api_key = env.str('RATE_API_KEY')
    base_url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair'

    r = requests.get(f'{base_url}/{base_cur}/{target_cur}/{amount}')
    data = r.json()

    return float(data['conversion_result'])



def get_change_keyboard(
        base_cur: str = 'USD',
        target_cur: str = 'ILS'
) -> InlineKeyboardMarkup:
    change_btn = InlineKeyboardButton(
        text='🔄',
        callback_data='reverse'
    )
    base_btn = InlineKeyboardButton(
        text=base_cur,
        callback_data='choose_base_cur'
    )
    target_btn = InlineKeyboardButton(
        text=target_cur,
        callback_data='choose_target_cur'
    )

    builder = InlineKeyboardBuilder()
    builder.row(base_btn, change_btn, target_btn, width=3)

    return builder.as_markup()


def get_exchange_message(
        base_sum: int | float = 0,
        target_sum: int | float = 0
) -> str:
    """Get text message for main exchange window."""

    text = (f'<b>=== <u>Currency Exchange</u> ===</b>\n\n\n'
            f'<b>{base_sum:.2f}</b>    ➡️    <b>{target_sum:.2f}</b>\n\n\n'
            f'Enter your sum to convert ⬇\n\n')

    return text


@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id not in USERS:
        USERS[user_id] = {'base_cur': 'USD', 'target_cur': 'ILS'}

    await message.answer(
        text=get_exchange_message(),
        reply_markup=get_change_keyboard(USERS[user_id]['base_cur'], USERS[user_id]['target_cur'])
    )


@dp.callback_query(F.data == 'reverse')
async def reverse_currencies(callback: CallbackQuery):
    user_id = callback.from_user.id
    USERS[user_id]['base_cur'], USERS[user_id]['target_cur'] = USERS[user_id]['target_cur'], USERS[user_id]['base_cur']
    await callback.message.edit_reply_markup(
        reply_markup=get_change_keyboard(
            base_cur=USERS[user_id]['base_cur'],
            target_cur=USERS[user_id]['target_cur']
        )
    )


@dp.message(lambda x: x.text.isdigit())
async def number_sent(message: Message):
    user_id = message.from_user.id
    base_cur = USERS[user_id]['base_cur']
    target_cur = USERS[user_id]['target_cur']
    amount = float(message.text)

    result = convert_amount(base_cur, target_cur, amount)

    await message.answer(
        text = get_exchange_message(amount, result),
        reply_markup=get_change_keyboard(base_cur, target_cur)
    )


if __name__ == '__main__':
    dp.run_polling(bot)
