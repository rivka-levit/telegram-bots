from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from dotenv import load_dotenv

import os

load_dotenv()


BOT_TOKEN = os.environ.get('ECHO_BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь, и в ответ я пришлю тебе твое сообщение'
    )


@dp.message()
async def send_echo(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается методом send_copy'
        )


if __name__ == '__main__':
    dp.run_polling(bot)

# @dp.message(F.photo)
# async def send_photo_echo(message: Message):
#     await message.reply_photo(message.photo[0].file_id)
#
#
# @dp.message(F.voice)
# async  def send_voice_answer(message: Message):
#     await message.answer(text='Вы прислали голосовое сообщение!')
#
#
# @dp.message(F.sticker)
# async def send_sticker_echo(message: Message):
#     print(message.model_dump_json(indent=2, exclude_none=True))
#     await message.reply_sticker(sticker=message.sticker.file_id)
#
#
# @dp.message()
# async def send_echo(message: Message):
#     await message.reply(text=message.text)


# # Регистрируем хэндлеры вместо декораторов
# dp.message.register(process_start_command, Command(commands='start'))
# dp.message.register(process_help_command, Command(commands='help'))
# dp.message.register(send_echo)
# dp.message.register(send_photo_echo, F.photo)
