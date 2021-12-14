import uuid

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

from loguru import logger

from app.keyboards.default import main_menu_keyboard
from app.keyboards.inline import call_setup_order_keyboard, call_order_access_keyboard, order_content_keyboard, order_preview_keyboard
from app.loader import db


class CreateOrder(StatesGroup):
    order = State()
    name = State()
    description = State()
    price = State()
    address = State()
    access = State()
    preview = State()
    preview_photo = State()
    preview_video = State()
    preview_audio = State()
    preview_document = State()
    content = State()
    content_message = State()
    content_photo = State()
    content_video = State()
    content_audio = State()
    content_document = State()


async def setup_order(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state not in CreateOrder.states_names:
        # await state.reset_state()
        await message.answer(
            "Welcome message for create order...",
            reply_markup=types.ReplyKeyboardRemove()
        )
    current_data = await state.get_data()
    await message.answer(
        "Order data:",
        reply_markup=call_setup_order_keyboard(**current_data)
    )
    await CreateOrder.order.set()


async def add_name(callback: types.CallbackQuery):
    await callback.message.edit_text("Enter the name for your order")
    await CreateOrder.name.set()


async def enter_name(message: types.Message, state: FSMContext):
    if len(message.text) > 100:
        await message.reply(
            "This name is too long, the maximum is 100 characters.\n"
            "Try again!"
        )
        return
    await state.update_data(name=message.text)
    await setup_order(message, state)


async def add_description(callback: types.CallbackQuery):
    await callback.message.edit_text("Enter the description for your order")
    await CreateOrder.description.set()


async def enter_description(message: types.Message, state: FSMContext):
    if len(message.text) > 350:
        await message.reply(
            "This description is too long, the maximum is 350 characters.\n"
            "Try again!"
        )
        return
    await state.update_data(description=message.text)
    await setup_order(message, state)


async def add_price(callback: types.CallbackQuery):
    await callback.message.edit_text("Enter the price for your order")
    await CreateOrder.price.set()


async def enter_price(message: types.Message, state: FSMContext):
    # TODO: Add pattern for price
    await state.update_data(price=message.text)
    await setup_order(message, state)


async def add_address(callback: types.CallbackQuery):
    await callback.message.edit_text("Enter the address for payment")
    await CreateOrder.address.set()


async def enter_address(message: types.Message, state: FSMContext):
    # TODO: Add pattern for address
    await state.update_data(address=message.text)
    await setup_order(message, state)


async def add_access(callback: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    await callback.message.edit_text(
        "Select the access type for your order.\n"
        "Public - the order will be available in the market for all.\n"
        "Private - the order will be available in the market only after entering a special identifier, "
        "which you will receive after saving the order."
    )
    if "access" in current_data:
        await callback.message.edit_reply_markup(call_order_access_keyboard(current_data["access"]))
    else:
        await callback.message.edit_reply_markup(call_order_access_keyboard())
    await CreateOrder.access.set()


async def select_access(callback: types.CallbackQuery, state: FSMContext):
    access = callback.data.split('_')[0]
    await state.update_data(access=access)
    await callback.message.edit_text(f"Selected access type: {access}")
    await setup_order(callback.message, state)


async def back_setup_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await setup_order(callback.message, state)


async def enter_items(content_type: str, message: types.Message, state: FSMContext, preview=False) -> None:
    if message.content_type != content_type:
        await message.answer(
            f"You must send {content_type}.\n"
            "Try again!"
        )
    else:
        prefix = "preview" if preview else "content"
        current_data = await state.get_data()
        if prefix not in current_data:
            current_data[prefix] = {}
        # text type item is used only for "content"
        if content_type == "text":
            if len(message.text) == 4096:
                await message.reply("Please note that this message will be added")
            if "message" not in current_data["content"]:
                current_data["content"]["message"] = []
            current_data["content"]["message"] += [message.text]
        elif content_type == "photo":
            if "photo" not in current_data[prefix]:
                current_data[prefix]["photo"] = []
            current_data[prefix]["photo"] += [message.photo[-1].file_id]
        elif content_type == "video":
            if "video" not in current_data[prefix]:
                current_data[prefix]["video"] = []
            current_data[prefix]["video"] += [message.video.file_id]
        elif content_type == "audio":
            if "audio" not in current_data[prefix]:
                current_data[prefix]["audio"] = []
            current_data[prefix]["audio"] += [message.audio.file_id]
        elif content_type == "document":
            if "document" not in current_data[prefix]:
                current_data[prefix]["document"] = []
            current_data[prefix]["document"] += [message.document.file_id]
        await state.update_data(current_data)
        await message.answer(
            "\n".join(
                f"Number of {content_type}s: {len(current_data[prefix][content_type])}"
                for content_type in current_data[prefix]
            ),
            reply_markup=order_preview_keyboard if preview else order_content_keyboard
        )
        await state.set_state(CreateOrder.preview.state if preview else CreateOrder.content.state)


async def reset_items(callback: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    items_category = callback.data.split('_')[1]
    if items_category in current_data:
        del current_data[items_category]
        await state.set_data(current_data)
        if items_category == "preview":
            await callback.message.edit_text(
                "Add preview files (it is not necessary):",
                reply_markup=order_preview_keyboard
            )
        else:
            await callback.message.edit_text(
                "Add content (you must add at least one item):",
                reply_markup=order_content_keyboard
            )
    else:
        await callback.answer()


async def add_preview(callback: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    await callback.message.edit_text(
        "\n".join(
            f"Number of {content_type}s: {len(current_data['preview'][content_type])}"
            for content_type in current_data['preview']
        ) if 'preview' in current_data else "Add preview files (it is not necessary):\n",
        reply_markup=order_preview_keyboard
    )
    await CreateOrder.preview.set()


async def add_preview_photo(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the photo for the order preview")
    await CreateOrder.preview_photo.set()


async def enter_preview_photo(message: types.Message, state: FSMContext):
    await enter_items("photo", message, state, preview=True)


async def add_preview_video(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the video for the order preview")
    await CreateOrder.preview_video.set()


async def enter_preview_video(message: types.Message, state: FSMContext):
    await enter_items("video", message, state, preview=True)


async def add_preview_audio(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the audio for the order preview")
    await CreateOrder.preview_audio.set()


async def enter_preview_audio(message: types.Message, state: FSMContext):
    await enter_items("audio", message, state, preview=True)


async def add_preview_document(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the document for the order preview")
    await CreateOrder.preview_document.set()


async def enter_preview_document(message: types.Message, state: FSMContext):
    await enter_items("document", message, state, preview=True)


async def add_content(callback: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    await callback.message.edit_text(
        "\n".join(
            f"Number of {content_type}s: {len(current_data['content'][content_type])}"
            for content_type in current_data['content']
        ) if 'content' in current_data else "Add content (you must add at least one item):",
        reply_markup=order_content_keyboard
    )
    await CreateOrder.content.set()


async def add_content_message(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the comment for the order or the information itself you are going to sell")
    await CreateOrder.content_message.set()


async def enter_content_message(message: types.Message, state: FSMContext):
    await enter_items("text", message, state)


async def add_content_photo(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the photo you are going to sell")
    await CreateOrder.content_photo.set()


async def enter_content_photo(message: types.Message, state: FSMContext):
    await enter_items("photo", message, state)


async def add_content_video(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the video you are going to sell")
    await CreateOrder.content_video.set()


async def enter_content_video(message: types.Message, state: FSMContext):
    await enter_items("video", message, state)


async def add_content_audio(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the audio you are going to sell")
    await CreateOrder.content_audio.set()


async def enter_content_audio(message: types.Message, state: FSMContext):
    await enter_items("audio", message, state)


async def add_content_document(callback: types.CallbackQuery):
    await callback.message.edit_text("Add the document you are going to sell")
    await CreateOrder.content_document.set()


async def enter_content_document(message: types.Message, state: FSMContext):
    await enter_items("document", message, state)


async def save_order(callback: types.CallbackQuery, state: FSMContext):
    order_data = await state.get_data()
    if len(order_data) >= 6 and "content" in order_data:
        if order_data["access"] == "private":
            order_data["access_token"] = uuid.uuid4()
            await callback.message.edit_text(order_data["access_token"])
            save_order_answer = (
                "Your order has been saved.\n"
                "Remember that it is only available by the special identifier above."
            )
        else:
            await callback.message.delete()
            save_order_answer = "Your order has been saved and is now available in the market."
        try:
            await db.add_order(callback.from_user.id, **order_data)
        except Exception as err:
            logger.info(err)
            await callback.message.answer(
                "Something went wrong.\n"
                "Try later!",
                reply_markup=main_menu_keyboard
            )
        else:
            await callback.message.answer(
                save_order_answer,
                reply_markup=main_menu_keyboard
            )
        await state.finish()
    else:
        await callback.message.edit_text(
            "Not all order data has been entered.\n"
            "Add missing by clicking on the buttons:",
            reply_markup=call_setup_order_keyboard(**order_data)
        )


def register_order_handlers(dp: Dispatcher):
    dp.register_message_handler(setup_order, Text(equals="Create order", ignore_case=True), state="*")
    dp.register_callback_query_handler(add_name, Text(equals="name"), state=CreateOrder.order)
    dp.register_message_handler(enter_name, state=CreateOrder.name)
    dp.register_callback_query_handler(back_setup_order, Text(equals="back"), state=CreateOrder.states_names)
    dp.register_callback_query_handler(add_description, Text(equals="description"), state=CreateOrder.order)
    dp.register_message_handler(enter_description, state=CreateOrder.description)
    dp.register_callback_query_handler(add_price, Text(equals="price"), state=CreateOrder.order)
    dp.register_message_handler(enter_price, state=CreateOrder.price)
    dp.register_callback_query_handler(add_address, Text(equals="address"), state=CreateOrder.order)
    dp.register_message_handler(enter_address, state=CreateOrder.address)
    dp.register_callback_query_handler(add_access, Text(equals="access"), state=CreateOrder.order)
    dp.register_callback_query_handler(select_access, Text(endswith="access"), state=CreateOrder.access)
    dp.register_callback_query_handler(add_preview, Text(equals="preview"), state=CreateOrder.order)
    dp.register_callback_query_handler(add_preview_photo, Text(equals="photo"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_photo, content_types=ContentType.ANY, state=CreateOrder.preview_photo)
    dp.register_callback_query_handler(add_preview_video, Text(equals="video"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_video, content_types=ContentType.ANY, state=CreateOrder.preview_video)
    dp.register_callback_query_handler(add_preview_audio, Text(equals="audio"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_audio, content_types=ContentType.ANY, state=CreateOrder.preview_audio)
    dp.register_callback_query_handler(add_preview_document, Text(equals="document"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_document, content_types=ContentType.ANY, state=CreateOrder.preview_document)
    dp.register_callback_query_handler(reset_items, Text(startswith="reset"), state=CreateOrder.states_names)
    dp.register_callback_query_handler(add_content, Text(equals="content"), state=CreateOrder.order)
    dp.register_callback_query_handler(add_content_message, Text(equals="message"), state=CreateOrder.content)
    dp.register_message_handler(enter_content_message, state=CreateOrder.content_message)
    dp.register_callback_query_handler(add_content_photo, Text(equals="photo"), state=CreateOrder.content)
    dp.register_message_handler(enter_content_photo, content_types=ContentType.ANY, state=CreateOrder.content_photo)
    dp.register_callback_query_handler(add_content_video, Text(equals="video"), state=CreateOrder.content)
    dp.register_message_handler(enter_content_video, content_types=ContentType.ANY, state=CreateOrder.content_video)
    dp.register_callback_query_handler(add_content_audio, Text(equals="audio"), state=CreateOrder.content)
    dp.register_message_handler(enter_content_audio, content_types=ContentType.ANY, state=CreateOrder.content_audio)
    dp.register_callback_query_handler(add_content_document, Text(equals="document"), state=CreateOrder.content)
    dp.register_message_handler(enter_content_document, content_types=ContentType.ANY, state=CreateOrder.content_document)
    dp.register_callback_query_handler(save_order, Text(equals="save_order"), state=CreateOrder.order)
