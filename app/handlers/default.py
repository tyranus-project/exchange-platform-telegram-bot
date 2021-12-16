from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from app.keyboards.inline import main_menu_keyboard, market_menu_keyboard
from app.loader import db


async def main_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.reset_state()
    if message.text == "/start":
        await message.answer("Welcome message...")
        # Check the user in the database
        if await db.verification(message.from_user.id):
            await message.answer("You have already used this bot")
        else:
            await message.answer("You have added to db!")
            await db.add_user(message.from_user.id, message.from_user.locale.language_name)
    await message.answer(
        "Main menu message...",
        reply_markup=main_menu_keyboard
    )


async def back_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Main menu message...",
        reply_markup=main_menu_keyboard
    )


def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(main_menu, commands=["start", "menu"], state="*")
    dp.register_callback_query_handler(back_main_menu, Text(equals="back_main_menu"))
