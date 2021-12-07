from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def call_order_data_keyboard(name=None, short_description=None, price=None, address=None):
    order_data_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{'✅' if name else '☑'} Name", callback_data="name")],
            [InlineKeyboardButton(f"{'✅' if short_description else '☑'} Short description", callback_data="short_description")],
            [InlineKeyboardButton(f"{'✅' if price else '☑'} Price", callback_data="price")],
            [InlineKeyboardButton(f"{'✅' if address else '☑'} Address", callback_data="address")],
            [InlineKeyboardButton("Ok", callback_data="save_order_data")]
        ]
    )
    return order_data_keyboard
