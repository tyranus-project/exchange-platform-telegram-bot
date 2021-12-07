from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def call_order_data_keyboard(name=None, category=None, short_description=None, price=None, address=None):
    order_data_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{'✅' if name else '☑'} Name", callback_data="name")],
            [InlineKeyboardButton(f"{'✅' if category else '☑'} Category", callback_data="categories")],
            [InlineKeyboardButton(f"{'✅' if short_description else '☑'} Short description", callback_data="short_description")],
            [InlineKeyboardButton(f"{'✅' if price else '☑'} Price", callback_data="price")],
            [InlineKeyboardButton(f"{'✅' if address else '☑'} Address", callback_data="address")],
            [InlineKeyboardButton("Ok", callback_data="save_order_data")]
        ]
    )
    return order_data_keyboard


def call_order_categories_keyboard(order_categories):
    categories_buttons = [
        InlineKeyboardButton(f"{category}", callback_data=f"category_{category}") for category in order_categories
    ]
    back_order_data_keyboard = [
        InlineKeyboardButton(f"Back", callback_data="back_order_data_keyboard")
    ]
    order_categories_keyboard = InlineKeyboardMarkup(row_width=3)
    order_categories_keyboard.add(*categories_buttons)
    order_categories_keyboard.insert(*back_order_data_keyboard)
    return order_categories_keyboard
