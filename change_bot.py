from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
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
        base_sum: str = '-----',
        target_sum: str = '-----'
) -> str:
    """Get text message for main exchange window."""

    text = f'<b>Currency Exchange</b>\n\n{base_sum}    ➡️    {target_sum}\n\n '

    return text


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        text=get_exchange_message(),
        reply_markup=get_change_keyboard()
    )


if __name__ == '__main__':
    dp.run_polling(bot)