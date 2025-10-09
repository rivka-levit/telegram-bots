from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import LEXICON


def create_inline_keyboard(
        width: int,
        *args,
        **kwargs
) -> InlineKeyboardMarkup:
    """Function to create inline keyboard dynamically."""

    builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    # Fill the list with the buttons from *args and **kwargs
    for btn in args:
        buttons.append(InlineKeyboardButton(
            text=LEXICON[btn] if btn in LEXICON else btn,
            callback_data=btn
        ))

    for btn, text in kwargs.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=btn
        ))

    builder.row(*buttons, width=width)
    keyboard: InlineKeyboardMarkup = builder.as_markup()

    return keyboard
