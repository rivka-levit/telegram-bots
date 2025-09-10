from aiogram import Bot, Dispatcher
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated


BOT_TOKEN = 'BOT_TOKEN'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')
