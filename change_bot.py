import logging
import sys

import requests

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
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

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(filename)s:%(lineno)d - %(message)s",
    stream=sys.stdout,
)
# def get_supported_currencies() -> list[list[str]]:
#     api_key = env.str('RATE_API_KEY')
#     url = f'https://v6.exchangerate-api.com/v6/{api_key}/codes'
#     r = requests.get(url)
#     return r.json()['supported_codes']


USERS = dict()
CURRENCIES = {
    'AED': 'United Arab Emirates Dirham',
    'ARS': 'Argentine Peso',
    'AUD': 'Australian Dollar',
    'BWP': 'Botswanan Pula',
    'BGN': 'Bulgarian Lev',
    'BHD': 'Bahraini Dinar',
    'BND': 'Brunei Dollar',
    'BRL': 'Brazilian Real',
    'CAD': 'Canadian Dollar',
    'CHF': 'Swiss Franc',
    'CLP': 'Chilean Peso',
    'CNY': 'Chinese Yuan',
    'COP': 'Colombian Peso',
    'CZK': 'Czech Republic Koruna',
    'DKK': 'Danish Krone',
    'EUR': 'Euro',
    'GBP': 'British Pound Sterling',
    'HKD': 'Hong Kong Dollar',
    'HRK': 'Croatian Kuna',
    'HUF': 'Hungarian Forint',
    'IDR': 'Indonesian Rupiah',
    'ILS': 'Israeli New Sheqel',
    'INR': 'Indian Rupee',
    'IRR': 'Iranian Rial',
    'ISK': 'Icelandic Krona',
    'JPY': 'Japanese Yen',
    'KRW': 'South Korean Won',
    'KWD': 'Kuwaiti Dinar',
    'KZT': 'Kazakhstani Tenge',
    'LKR': 'Sri Lankan Rupee',
    'LYD': 'Libyan Dinar',
    'MUR': 'Mauritian Rupee',
    'MXN': 'Mexican Peso',
    'MYR': 'Malaysian Ringgit',
    'NOK': 'Norwegian Krone',
    'NPR': 'Nepalese Rupee',
    'NZD': 'New Zealand Dollar',
    'OMR': 'Omani Rial',
    'PHP': 'Philippine Peso',
    'PKR': 'Pakistani Rupee',
    'PLN': 'Polish Zloty',
    'QAR': 'Qatari Rial',
    'RON': 'Romanian Leu',
    'RUB': 'Russian Ruble',
    'SAR': 'Saudi Riyal',
    'SEK': 'Swedish Krona',
    'SGD': 'Singapore Dollar',
    'THB': 'Thai Baht',
    'TRY': 'Turkish Lira',
    'TTD': 'Trinidad and Tobago Dollar',
    'TWD': 'New Taiwan Dollar',
    'USD': 'United States Dollar',
    'VEF': 'Venezuelan Bolivar Fuerte',
    'ZAR': 'South African Rand'
}

bot = Bot(
    token=env.str('TEST_BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def convert_amount(base_cur: str, target_cur: str, amount: int | float) -> float:
    """Converts amount from base currency to target currency."""

    api_key = env.str('RATE_API_KEY')
    base_url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair'

    r = requests.get(f'{base_url}/{base_cur}/{target_cur}/{amount}')
    data = r.json()

    return float(data['conversion_result'])


class BaseCurrencyCallbackFactory(CallbackData, prefix='source'):
    """Base currency callback factory."""

    code: str


class TargetCurrencyCallbackFactory(CallbackData, prefix='target'):
    """Target currency callback factory."""

    code: str


def exchange_keyboard(base_cur: str, target_cur: str) -> InlineKeyboardMarkup:
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


def base_currencies_choice_keyboard() -> InlineKeyboardMarkup:
    codes_buttons = list()

    for code, name in CURRENCIES.items():
        currency_btn = InlineKeyboardButton(
            text=code,
            callback_data=BaseCurrencyCallbackFactory(code=code).pack()
        )
        codes_buttons.append(currency_btn)

    builder = InlineKeyboardBuilder()
    builder.row(*codes_buttons, width=5)

    return builder.as_markup()


def target_currencies_choice_keyboard() -> InlineKeyboardMarkup:
    codes_buttons = list()

    for code, name in CURRENCIES.items():
        currency_btn = InlineKeyboardButton(
            text=code,
            callback_data=TargetCurrencyCallbackFactory(code=code).pack()
        )
        codes_buttons.append(currency_btn)

    builder = InlineKeyboardBuilder()
    builder.row(*codes_buttons, width=5)

    return builder.as_markup()


def get_exchange_message(
        base_sum: int | float,
        target_sum: int | float,
        user_id: str | int
) -> str:
    """Get text message for main exchange window."""

    text = (f'{USERS[user_id]['base_cur']}  <b>{base_sum:,.2f}</b>    ➡️    '
            f'{USERS[user_id]['target_cur']}  <b>{target_sum:,.2f}</b>\n\n\n'.replace(',', ' '))

    return text


# ---------------------- Handlers ---------------------------

@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id not in USERS:
        USERS[user_id] = {'base_cur': 'USD', 'target_cur': 'ILS'}

    keyboard = exchange_keyboard(
        base_cur=USERS[user_id]['base_cur'],
        target_cur=USERS[user_id]['target_cur']
    )

    await message.answer(
                text=get_exchange_message(0, 0, user_id=user_id),
                reply_markup=keyboard
            )


@dp.callback_query(F.data=='choose_base_cur')
async def choose_base_cur(callback: CallbackQuery):
    keyboard = base_currencies_choice_keyboard()
    text = 'Choose your base currency.'
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@dp.callback_query(F.data=='choose_target_cur')
async def choose_base_cur(callback: CallbackQuery):
    keyboard = target_currencies_choice_keyboard()
    text = 'Choose your target currency.'
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@dp.callback_query(F.data == 'reverse')
async def reverse_currencies(callback: CallbackQuery):
    user_id = callback.from_user.id
    USERS[user_id]['base_cur'], USERS[user_id]['target_cur'] = USERS[user_id]['target_cur'], USERS[user_id]['base_cur']
    await callback.message.edit_reply_markup(
        reply_markup=exchange_keyboard(
            base_cur=USERS[user_id]['base_cur'],
            target_cur=USERS[user_id]['target_cur']
        )
    )


@dp.callback_query(BaseCurrencyCallbackFactory.filter())
async def process_base_currency_choice(
        callback: CallbackQuery,
        callback_data: BaseCurrencyCallbackFactory
):
    user_id = callback.from_user.id
    USERS[user_id]['base_cur'] = callback_data.code

    await callback.message.edit_text(
        text=get_exchange_message(0, 0, user_id=user_id),
        reply_markup=exchange_keyboard(
            base_cur=USERS[user_id]['base_cur'],
            target_cur=USERS[user_id]['target_cur']
        )
    )


@dp.callback_query(TargetCurrencyCallbackFactory.filter())
async def process_target_currency_choice(
        callback: CallbackQuery,
        callback_data: TargetCurrencyCallbackFactory
):
    user_id = callback.from_user.id
    USERS[user_id]['target_cur'] = callback_data.code

    await callback.message.edit_text(
        text=get_exchange_message(0, 0, user_id=user_id),
        reply_markup=exchange_keyboard(
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
        text=get_exchange_message(amount, result, user_id=user_id),
        reply_markup=exchange_keyboard(base_cur, target_cur)
    )


if __name__ == '__main__':
    dp.run_polling(bot)
