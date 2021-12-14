from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def call_setup_order_keyboard(
        name=None, description=None, price=None, address=None, access=None, preview=None, content=None
) -> InlineKeyboardMarkup:
    setup_order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{'✔ Name' if name else '➕ Add name'}", callback_data="name")],
            [InlineKeyboardButton(f"{'✔ Description' if description else '➕ Add description'}", callback_data="description")],
            [InlineKeyboardButton(f"{'✔ Price' if price else '➕ Add price'}", callback_data="price")],
            [InlineKeyboardButton(f"{'✔ Address' if address else '➕ Add address'}", callback_data="address")],
            [InlineKeyboardButton(f"{'✔ Access' if access else '➕ Add access'}", callback_data="access")],
            [InlineKeyboardButton(f"{'✔ Content' if content else '➕ Add content'}", callback_data="content")],
            [InlineKeyboardButton(f"{'✔ Preview' if preview else '➕ Add preview files'}", callback_data="preview")],
            [InlineKeyboardButton("Ok", callback_data="save_order")]
        ]
    )
    return setup_order_keyboard


def call_order_access_keyboard(access: str = None, back_button: bool = True) -> InlineKeyboardMarkup:
    access_buttons = [
        InlineKeyboardButton(f"{'✔ ' if access == 'public' else ''}Public", callback_data="public_access"),
        InlineKeyboardButton(f"{'✔ ' if access == 'private' else ''}Private", callback_data="private_access")
    ]
    order_access_keyboard = InlineKeyboardMarkup(row_width=2).add(*access_buttons)
    # For possible reuse in market handlers
    if back_button:
        order_access_keyboard.add(InlineKeyboardButton("< Back", callback_data="back"))
    return order_access_keyboard


order_preview_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton("➕ Add photo", callback_data="photo")],
                [InlineKeyboardButton("➕ Add video", callback_data="video")],
                [InlineKeyboardButton("➕ Add audio", callback_data="audio")],
                [InlineKeyboardButton("➕ Add document", callback_data="document")],
                [InlineKeyboardButton("➰ Reset preview files", callback_data="reset_preview")],
                [InlineKeyboardButton("< Back", callback_data="back")]
            ]
        )

order_content_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton("➕ Add message", callback_data="message")],
            [InlineKeyboardButton("➕ Add photo", callback_data="photo")],
            [InlineKeyboardButton("➕ Add video", callback_data="video")],
            [InlineKeyboardButton("➕ Add audio", callback_data="audio")],
            [InlineKeyboardButton("➕ Add document", callback_data="document")],
            [InlineKeyboardButton("➰ Reset content", callback_data="reset_content")],
            [InlineKeyboardButton("< Back", callback_data="back")]
        ]
    )
