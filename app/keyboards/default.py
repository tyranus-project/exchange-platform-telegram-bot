from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Create order"), KeyboardButton(text="Market")],
        [KeyboardButton(text="Settings"), KeyboardButton(text="Support")]
    ],
    resize_keyboard=True
)
