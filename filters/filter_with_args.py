"""
Filter to pass arguments to a handler
"""

from aiogram import Bot, Dispatcher, F
from aiogram.filters import BaseFilter
from aiogram.types import Message

BOT_TOKEN = 'BOT_TOKEN'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Filter checks if there ara numbers in the message and passes the list of numbers to a handler
class NumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = list()

        # Extract numbers, add them to the list
        for word in message.text.split(' '):
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))

        if numbers:
            return {'numbers': numbers}

        return False


# Handler for updates start with `найди числа` and contain numbers
@dp.message(F.text.lower().startswith('найди числа'), NumbersInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(text=f'Нашел: {", ".join(str(num) for num in numbers)}')


# Handler for updates that start with `найди числа` but not contain numbers
@dp.message(F.text.lower().startswith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(text='Не нашел что-то :(')


if __name__ == '__main__':
    dp.run_polling(bot)