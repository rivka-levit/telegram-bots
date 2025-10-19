import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from environs import Env

env = Env()
env.read_env()

bot = Bot(token=env.str('TEST_BOT_TOKEN'))
dp = Dispatcher()


LEXICON: dict[str, str] = {
    'audio': '🎶 Аудио',
    'text': '📃 Текст',
    'photo': '🖼 Фото',
    'video': '🎬 Видео',
    'document': '📑 Документ',
    'voice': '📢 Голосовое сообщение',
    'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
    'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
    'photo_id1': 'AgACAgQAAxkBAAICJmj08x39Y5mdJe0_6_HRVtdx90ZDAAKeyDEb-2ypU1UagOqXzHmsAQADAgADeAADNgQ',
    'photo_id2': 'AgACAgQAAxkBAAICKGj08zkYOMHQOtITsiqSMX3Q1clbAAKfyDEb-2ypU99gMwABO9z6hwEAAwIAA3kAAzYE',
    'voice_id1': 'AwACAgQAAxkBAAICFmj08O-5ENvRtMAimCl5gFEym7ueAAKxHQAC-2ypU2IlRq_1z9z_NgQ',
    'voice_id2': 'AwACAgQAAxkBAAICGGj08PWJgP9rDjnqO8X3RL7OBPGwAAKyHQAC-2ypU2S3GXGM87HYNgQ',
    'audio_id1': 'CQACAgQAAxkBAAICImj08siEfy-lMFFlm44h7wI4DngHAAK4HQAC-2ypUxDtwbpfznmJNgQ',
    'audio_id2': 'CQACAgQAAxkBAAICJGj08uoQuwgD3X1aZYXRsBppnVDdAAK5HQAC-2ypU-0J-832DvsQNgQ',
    'document_id1': 'BQACAgQAAxkBAAICHmj08mkAAeVPhUbC91PAuujZvRD9rwACtR0AAvtsqVOfwJcHKdCW7TYE',
    'document_id2': 'BQACAgQAAxkBAAICIGj08pjRUSbVsJkzP_6WN2E_QCbcAAK3HQAC-2ypU4VVAAEVGRuKPTYE',
    'video_id1': 'BAACAgQAAxkBAAICGmj08eyntY75OPEHB-JjAyokl4H0AAKzHQAC-2ypU9WQw2imF4pzNgQ',
    'video_id2': 'BAACAgQAAxkBAAICHGj08gc2DKjLKV8DZIAPy6J_isZRAAK0HQAC-2ypU0ukFI-EClFfNgQ',
}


def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    """Generate keyboards with inline buttons."""

    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))

    # Fill builder row with buttons
    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    markup = get_markup(2, 'photo')
    await message.answer_photo(
        photo=LEXICON['photo_id1'],
        caption='Это фото 1',
        reply_markup=markup
    )


@dp.callback_query(F.data.in_(
    ['text', 'audio', 'video', 'document', 'photo', 'voice']
))
async def process_button_press(callback: CallbackQuery, bot: Bot):
    markup = get_markup(2, 'photo')
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=LEXICON['photo_id2'],
                caption='Это фото 2'
            ),
            reply_markup=markup
        )
    except TelegramBadRequest:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=LEXICON['photo_id1'],
                caption='Это фото 1'
            ),
            reply_markup=markup
        )


# Этот хэндлер будет срабатывать на все остальные сообщения
@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Не понимаю')


if __name__ == '__main__':
    dp.run_polling(bot)
