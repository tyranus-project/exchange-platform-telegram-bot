import json

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

from loguru import logger

from app.keyboards.inline import call_setup_order_keyboard, call_order_categories_keyboard, order_content_keyboard, order_preview_keyboard
from app.loader import db

order_categories = ["Information", "Documents", "Photos", "Videos", "Location", "Other"]


class CreateOrder(StatesGroup):
    order = State()
    name = State()
    category = State()
    description = State()
    price = State()
    address = State()
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
    if await state.get_state() is None:
        await message.answer("Welcome message")
    current_data = await state.get_data()
    await message.answer(
        "Order data:",
        reply_markup=call_setup_order_keyboard(**current_data)
    )
    await CreateOrder.order.set()


async def add_name(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter order name")
    await CreateOrder.name.set()


async def enter_name(message: types.Message, state: FSMContext):
    if len(message.text) > 100:
        await message.reply(
            "This name is too long, the maximum is 70 characters.\n"
            "Try again!"
        )
        return
    await state.update_data(name=message.text)
    await setup_order(message, state)


async def add_category(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Select the category for the order:")
    await callback.message.edit_reply_markup(call_order_categories_keyboard(order_categories))
    await CreateOrder.category.set()


async def select_category(callback: types.CallbackQuery, state: FSMContext):
    category_name = callback.data.split('_')[1]
    await state.update_data(category=category_name)
    await callback.message.edit_text(f"Selected category: {category_name}")
    await setup_order(callback.message, state)


async def back_setup_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await setup_order(callback.message, state)


async def add_description(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter the description of the order")
    await CreateOrder.description.set()


async def enter_description(message: types.Message, state: FSMContext):
    if len(message.text) > 350:
        await message.reply(
            "This description is too long, the maximum is 150 characters.\n"
            "Try again!"
        )
        return
    await state.update_data(description=message.text)
    await setup_order(message, state)


async def add_price(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter the price of the order")
    await CreateOrder.price.set()


async def enter_price(message: types.Message, state: FSMContext):
    # TODO: Add pattern for price
    await state.update_data(price=message.text)
    await setup_order(message, state)


async def add_address(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter the address for payment")
    await CreateOrder.address.set()


async def enter_address(message: types.Message, state: FSMContext):
    # TODO: Add pattern for address
    await state.update_data(address=message.text)
    await setup_order(message, state)


async def enter_items(content_type: str, message: types.Message, state: FSMContext, preview=False) -> None:
    if message.content_type != content_type:
        await message.answer(f"You must send {content_type}. Try again!")
    else:
        prefix = "preview" if preview else "content"
        current_data = await state.get_data()
        if prefix not in current_data:
            current_data[prefix] = {}
        if content_type == "text":
            if len(message.text) == 4096:
                await message.reply("Please note that this message will be added")
            if "message" not in current_data[prefix]:
                current_data[prefix]["message"] = []
            current_data[prefix]["message"] += [message.text]
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
    await callback.message.edit_text(f"Add the photo for the order preview")
    await CreateOrder.preview_photo.set()


async def enter_preview_photo(message: types.Message, state: FSMContext):
    await enter_items("photo", message, state, preview=True)


async def add_preview_video(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add the video for the order preview")
    await CreateOrder.preview_video.set()


async def enter_preview_video(message: types.Message, state: FSMContext):
    await enter_items("video", message, state, preview=True)


async def add_preview_audio(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add the audio for the order preview")
    await CreateOrder.preview_audio.set()


async def enter_preview_audio(message: types.Message, state: FSMContext):
    await enter_items("audio", message, state, preview=True)


async def add_preview_document(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add the document for the order preview")
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
    await callback.message.edit_text(f"Add the comment for the order or the information itself you are going to sell")
    await CreateOrder.content_message.set()


async def enter_content_message(message: types.Message, state: FSMContext):
    await enter_items("text", message, state)


async def add_content_photo(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add the photo you are going to sell")
    await CreateOrder.content_photo.set()


async def enter_content_photo(message: types.Message, state: FSMContext):
    await enter_items("photo", message, state)


async def add_content_video(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add the video you are going to sell")
    await CreateOrder.content_video.set()


async def enter_content_video(message: types.Message, state: FSMContext):
    await enter_items("video", message, state)


async def add_content_audio(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add the audio you are going to sell")
    await CreateOrder.content_audio.set()


async def enter_content_audio(message: types.Message, state: FSMContext):
    await enter_items("audio", message, state)


async def add_content_document(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add the document you are going to sell")
    await CreateOrder.content_document.set()


async def enter_content_document(message: types.Message, state: FSMContext):
    await enter_items("document", message, state)


async def finish_order_data_setup(callback: types.CallbackQuery, state: FSMContext):
    order_data = await state.get_data()
    if len(order_data) >= 6:
        # logger.info(f"{order_data}")
        await db.add_order(callback.from_user.id, **order_data)
        await callback.message.edit_text("Your order has been added")
        # logger.info(await db.get_order(1))
        # content = dict(await db.get_content(1))
        # logger.info(content)
        # content = json.loads((await db.get_content(1))[0])
        # logger.info(content)
        # preview = dict(await db.get_preview_files(1))
        # logger.info(preview)
        # preview = json.loads((await db.get_preview_files(1))[0])
        # logger.info(preview)
        await state.finish()
    else:
        await callback.message.edit_text(
            "Not all order data has been entered.\n"
            "Add missing by clicking on the buttons:",
            reply_markup=call_setup_order_keyboard(**order_data)
        )
        return


def register_order_handlers(dp: Dispatcher):
    dp.register_message_handler(setup_order, Text(equals="Create order", ignore_case=True))
    dp.register_callback_query_handler(add_name, Text(equals="name"), state=CreateOrder.order)
    dp.register_message_handler(enter_name, state=CreateOrder.name)
    dp.register_callback_query_handler(add_category, Text(equals="categories"), state=CreateOrder.order)
    dp.register_callback_query_handler(select_category, Text(startswith="category"), state=CreateOrder.category)
    dp.register_callback_query_handler(back_setup_order, Text(equals="back_setup_order_keyboard"), state=CreateOrder.states_names)
    dp.register_callback_query_handler(add_description, Text(equals="description"), state=CreateOrder.order)
    dp.register_message_handler(enter_description, state=CreateOrder.description)
    dp.register_callback_query_handler(add_price, Text(equals="price"), state=CreateOrder.order)
    dp.register_message_handler(enter_price, state=CreateOrder.price)
    dp.register_callback_query_handler(add_address, Text(equals="address"), state=CreateOrder.order)
    dp.register_message_handler(enter_address, state=CreateOrder.address)
    dp.register_callback_query_handler(add_preview, Text(equals="preview"), state=CreateOrder.order)
    dp.register_callback_query_handler(add_preview_photo, Text(equals="photo"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_photo, content_types=ContentType.ANY, state=CreateOrder.preview_photo)
    dp.register_callback_query_handler(add_preview_video, Text(equals="video"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_video, content_types=ContentType.ANY, state=CreateOrder.preview_video)
    dp.register_callback_query_handler(add_preview_audio, Text(equals="audio"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_audio, content_types=ContentType.ANY, state=CreateOrder.preview_audio)
    dp.register_callback_query_handler(add_preview_document, Text(equals="document"), state=CreateOrder.preview)
    dp.register_message_handler(enter_preview_document, content_types=ContentType.ANY, state=CreateOrder.preview_document)
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
    dp.register_callback_query_handler(finish_order_data_setup, Text(equals="save_order"), state=CreateOrder.order)
