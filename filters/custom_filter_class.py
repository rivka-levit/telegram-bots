from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message

BOT_TOKEN = 'BOT TOKEN HERE'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# List ID of bot administrators.
admin_ids: list[int] = [173901673]


# Custom filter to check if user is admin
class IsAdmin(BaseFilter):
    def __init__(self, ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# This handler works if the message is from admin
@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    await message.answer(text='Вы админ')


# This handler works if the message is not from admin
@dp.message()
async def answer_if_not_admins_update(message: Message):
    await message.answer(text='Вы не админ')


if __name__ == '__main__':
    dp.run_polling(bot)
