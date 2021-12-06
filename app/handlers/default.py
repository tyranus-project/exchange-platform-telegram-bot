from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart

from app.keyboards.default import main_menu_keyboard
from app.loader import db


async def cmd_start(message: types.Message):
    await message.answer(
        "Welcome!",
        reply_markup=main_menu_keyboard
    )
    if await db.verification(message.from_user.id):
        await message.answer("You have already used this bot")
    else:
        await message.answer("You have added to db!")
        await db.add_user(message.from_user.id, message.from_user.locale.language_name)


async def cmd_help(message: types.Message):
    await message.answer("Help message")


async def cmd_main_menu(message: types.Message):
    await message.answer(
        "Main menu",
        reply_markup=main_menu_keyboard
    )


def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, CommandStart(), state="*")
    dp.register_message_handler(cmd_help, CommandHelp(), state="*")
    dp.register_message_handler(cmd_main_menu, commands=["menu"], state="*")
