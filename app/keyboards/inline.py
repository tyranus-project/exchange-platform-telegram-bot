from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def call_setup_order_keyboard(
        name=None, category=None, description=None, price=None, address=None,
        message=None, photo=None, video=None, audio=None, document=None
):
    setup_order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{'✔ Name' if name else '➕ Add name'}", callback_data="name")],
            [InlineKeyboardButton(f"{'✔ Category' if category else '➕ Add category'}", callback_data="categories")],
            [InlineKeyboardButton(f"{'✔ Description' if description else '➕ Add description'}", callback_data="description")],
            [InlineKeyboardButton(f"{'✔ Price' if price else '➕ Add price'}", callback_data="price")],
            [InlineKeyboardButton(f"{'✔ Address' if address else '➕ Add address'}", callback_data="address")],
            [InlineKeyboardButton(f"{'✔ Content' if message or photo or video or audio or document else '➕ Add content'}", callback_data="content")],
            [InlineKeyboardButton("Ok", callback_data="save_order")]
        ]
    )
    return setup_order_keyboard


def call_order_categories_keyboard(order_categories):
    categories_buttons = [
        InlineKeyboardButton(f"{category}", callback_data=f"category_{category}") for category in order_categories
    ]
    back_order_setup_keyboard = [
        InlineKeyboardButton(f"Back", callback_data="back_setup_order_keyboard")
    ]
    order_categories_keyboard = InlineKeyboardMarkup(row_width=3)
    order_categories_keyboard.add(*categories_buttons)
    order_categories_keyboard.insert(*back_order_setup_keyboard)
    return order_categories_keyboard


order_content_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton("➕ Add message", callback_data="message")],
            [InlineKeyboardButton("➕ Add photo", callback_data="photo")],
            [InlineKeyboardButton("➕ Add video", callback_data="video")],
            [InlineKeyboardButton("➕ Add audio", callback_data="audio")],
            [InlineKeyboardButton("➕ Add document", callback_data="document")],
            [InlineKeyboardButton("Back", callback_data="back_setup_order_keyboard")]
        ]
    )
