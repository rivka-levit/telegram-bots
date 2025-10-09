import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
    BotCommandScopeDefault,
    Message,
)

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('TEST_BOT_TOKEN')

# Commands for default scope
DEFAULT_COMMANDS = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="help", description="Справка"),
]

# Commands for private scope
PERSONAL_COMMANDS = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="profile", description="Мой профиль"),
    BotCommand(command="settings", description="Настройки"),
    BotCommand(command="delpersonal", description="❌ Удалить персональное меню"),
]

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    """
    Handler works on /start command and sets up personal commands for the user.
    """

    # Create the scope for specific chat
    scope = BotCommandScopeChat(chat_id=message.chat.id)

    # Set up personal commands
    await bot.set_my_commands(commands=PERSONAL_COMMANDS, scope=scope)

    await message.answer(
        "Вам установлены персональные команды!\n"
        "Нажмите на кнопку 'Menu' или введите '/', чтобы увидеть их.\n"
        "Чтобы вернуть стандартные команды, используйте /delpersonal"
    )


@router.message(Command("delpersonal"))
async def process_del_personal_command(message: Message, bot: Bot):
    """
    Handler works on /delpersonal command and delete personal commands for
    the user.
    """

    # Create the same scope that was on set up
    scope = BotCommandScopeChat(chat_id=message.chat.id)

    # Delete the commands for this scope
    await bot.delete_my_commands(scope)

    await message.answer(
        "Персональные команды удалены. Теперь вы снова видите команды по умолчанию."
    )


async def on_startup(bot: Bot):
    """Set up default scope commands on startup of the bot."""

    logging.info("Starting bot... Setting up default commands.")
    await bot.set_my_commands(DEFAULT_COMMANDS, BotCommandScopeDefault())


async def on_shutdown(bot: Bot):
    """Delete default scope commands on shutdown of the bot."""

    logging.info("Bot stopping... Removing the default commands.")
    await bot.delete_my_commands(BotCommandScopeDefault())


async def main():
    if not BOT_TOKEN:
        logging.error(
            "The bot token was not found. Set the BOT_TOKEN environment variable."
        )
        return

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
               "%(lineno)d - %(name)s - %(message)s",
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register functions on startup and shutdown of the bot.
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Connect router
    dp.include_router(router)

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
