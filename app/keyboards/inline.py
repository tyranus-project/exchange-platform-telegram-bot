from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton("Profile", callback_data="profile"),
                InlineKeyboardButton("Market", callback_data="market")
            ],
            [
                InlineKeyboardButton("Support", callback_data="support")
            ]
        ]
    )

market_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton("Public", callback_data="public"),
                InlineKeyboardButton("Private", callback_data="private")
            ],
            [
                InlineKeyboardButton("Create order", callback_data="create_order")
            ],
            [
                InlineKeyboardButton("< Back", callback_data="back_main_menu")
            ]
        ]
    )


def call_create_order_menu_keyboard(
        name=None, description=None, price=None, address=None, access=None, content=None, preview=None
) -> InlineKeyboardMarkup:
    create_order_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{'✔ Name' if name else '➕ Add name'}", callback_data="name")],
            [InlineKeyboardButton(f"{'✔ Description' if description else '➕ Add description'}", callback_data="description")],
            [InlineKeyboardButton(f"{'✔ Price' if price else '➕ Add price'}", callback_data="price")],
            [InlineKeyboardButton(f"{'✔ Address' if address else '➕ Add address'}", callback_data="address")],
            [InlineKeyboardButton(f"{'✔ Access' if access else '➕ Add access'}", callback_data="access")],
            [InlineKeyboardButton(f"{'✔ Content' if content else '➕ Add content'}", callback_data="content")],
            [InlineKeyboardButton(f"{'✔ Preview' if preview else '➕ Add preview files'}", callback_data="preview")],
            [InlineKeyboardButton("< Back", callback_data="back_market_menu")]
        ]
    )
    if name and description and price and address and access and content:
        create_order_menu_keyboard.insert(InlineKeyboardButton("Ok", callback_data="save_order"))
    return create_order_menu_keyboard


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
