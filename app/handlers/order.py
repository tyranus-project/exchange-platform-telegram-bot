from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

from loguru import logger

from app.keyboards.inline import call_order_data_keyboard, call_order_categories_keyboard, order_content_keyboard
from app.loader import db


order_categories = ["Information", "Documents", "Photos", "Videos", "Location", "Other"]


class CreateOrder(StatesGroup):
    waiting_for_order_data = State()
    waiting_for_order_name = State()
    waiting_for_order_category = State()
    waiting_for_short_description = State()
    waiting_for_price = State()
    waiting_for_address = State()
    waiting_for_content = State()
    waiting_for_content_message = State()
    waiting_for_content_photo = State()
    waiting_for_content_video = State()
    waiting_for_content_audio = State()


async def setup_order_data(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await state.update_data(message=[], photo=[], video=[], audio=[])
        await message.answer("Welcome message")
    current_data = await state.get_data()
    await message.answer(
        "Order data: what needs to be added:",
        reply_markup=call_order_data_keyboard(**current_data)
    )
    await CreateOrder.waiting_for_order_data.set()


async def order_name_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter the {callback.data} of the order")
    # await callback.message.delete_reply_markup()
    await CreateOrder.waiting_for_order_name.set()


async def enter_order_name(message: types.Message, state: FSMContext):
    if len(message.text) > 50:
        await message.reply(
            "This name is too long, the maximum is 50 characters.\n"
            "Try again!"
        )
        return
    await state.update_data(name=message.text)
    await setup_order_data(message, state)


async def order_category_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Select the category for the order")
    await callback.message.edit_reply_markup(call_order_categories_keyboard(order_categories))
    await CreateOrder.waiting_for_order_category.set()


async def enter_order_category(callback: types.CallbackQuery, state: FSMContext):
    category_name = callback.data.split('_')[1]
    await state.update_data(category=category_name)
    await callback.message.edit_text(f"Selected category: {category_name}")
    # await callback.message.delete()
    await setup_order_data(callback.message, state)


async def back_setup_order_data(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await setup_order_data(callback.message, state)


async def order_short_description_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter the short description of the order")
    await CreateOrder.waiting_for_short_description.set()


async def enter_short_description(message: types.Message, state: FSMContext):
    if len(message.text) > 150:
        await message.reply(
            "This name is too long, the maximum is 150 characters.\n"
            "Try again!"
        )
        return
    await state.update_data(short_description=message.text)
    await setup_order_data(message, state)


async def order_price_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter the price of the order")
    await CreateOrder.waiting_for_price.set()


async def enter_price(message: types.Message, state: FSMContext):
    # TODO: Add pattern for price
    await state.update_data(price=message.text)
    await setup_order_data(message, state)


async def order_address_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Enter the price of the order")
    await CreateOrder.waiting_for_address.set()


async def enter_address(message: types.Message, state: FSMContext):
    # TODO: Add pattern for address
    await state.update_data(address=message.text)
    await setup_order_data(message, state)


async def order_content_button(callback: types.CallbackQuery, state):
    current_data = await state.get_data()
    await callback.message.edit_text(f"Number of messages: {len(current_data['message'])}")
    await callback.message.edit_reply_markup(order_content_keyboard)
    await CreateOrder.waiting_for_content.set()


async def order_message_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add a comment for the order or the information itself that you want to sell")
    await CreateOrder.waiting_for_content_message.set()


async def enter_message(message: types.Message, state: FSMContext):
    if len(message.text) == 4096:
        await message.reply("Please note that this message will be added")
    current_data = await state.get_data()
    current_data["message"] += [message.text]
    await state.update_data(message=current_data["message"])
    await message.answer(
        f"Number of messages: {len(current_data['message'])}",
        reply_markup=order_content_keyboard
    )
    await CreateOrder.waiting_for_content.set()


async def order_photo_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add photo")
    await CreateOrder.waiting_for_content_photo.set()


async def enter_photo(message: types.Message, state: FSMContext):
    if message.content_type != "photo":
        await message.answer("You must send photo. Try again!")
        return
    current_data = await state.get_data()
    current_data["photo"] += [message.photo[-1].file_id]
    await state.update_data(photo=current_data["photo"])
    await message.answer(
        f"Number of messages: {len(current_data['message'])}\n"
        f"Number of photos: {len(current_data['photo'])}",
        reply_markup=order_content_keyboard
    )
    await CreateOrder.waiting_for_content.set()


async def order_video_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add video")
    await CreateOrder.waiting_for_content_video.set()


async def enter_video(message: types.Message, state: FSMContext):
    if message.content_type != "video":
        await message.answer("You must send video. Try again!")
        return
    current_data = await state.get_data()
    current_data["video"] += [message.video.file_id]
    await state.update_data(video=current_data["video"])
    await message.answer(
        f"Number of messages: {len(current_data['message'])}\n"
        f"Number of photos: {len(current_data['photo'])}\n"
        f"Number of videos: {len(current_data['video'])}",
        reply_markup=order_content_keyboard
    )
    await CreateOrder.waiting_for_content.set()


async def order_audio_button(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Add audio")
    await CreateOrder.waiting_for_content_audio.set()


async def enter_audio(message: types.Message, state: FSMContext):
    if message.content_type != "audio":
        await message.answer("You must send audio. Try again!")
        return
    current_data = await state.get_data()
    current_data["audio"] += [message.audio.file_id]
    await state.update_data(audio=current_data["audio"])
    await message.answer(
        f"Number of messages: {len(current_data['message'])}\n"
        f"Number of photos: {len(current_data['photo'])}\n"
        f"Number of videos: {len(current_data['video'])}\n"
        f"Number of audios: {len(current_data['audio'])}",
        reply_markup=order_content_keyboard
    )
    await CreateOrder.waiting_for_content.set()


async def finish_order_data_setup(callback: types.CallbackQuery, state: FSMContext):
    order_data = await state.get_data()
    if len(order_data) == 9 and (
            order_data["message"] or order_data["photo"] or order_data["video"] or order_data["audio"]
    ):
        # logger.info(f"{order_data}")
        await db.add_order(callback.from_user.id, **order_data)
        await callback.message.edit_text("Finished")
        if order_data["audio"]:
            for audio_id in order_data["audio"]:
                await callback.message.answer_audio(audio_id)
        await state.reset_state()
        logger.info(await db.get_order(1))
    else:
        await callback.message.edit_text(
            "Not all order data has been entered.\n"
            "Add missing by clicking on the buttons:",
            reply_markup=call_order_data_keyboard(**order_data)
        )
        return


def register_order_handlers(dp: Dispatcher):
    dp.register_message_handler(setup_order_data, Text(equals="Create order", ignore_case=True))
    dp.register_callback_query_handler(order_name_button, Text(equals="name"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_order_name, state=CreateOrder.waiting_for_order_name)
    dp.register_callback_query_handler(order_category_button, Text(equals="categories"), state=CreateOrder.waiting_for_order_data)
    dp.register_callback_query_handler(enter_order_category, Text(startswith="category"), state=CreateOrder.waiting_for_order_category)
    dp.register_callback_query_handler(back_setup_order_data, Text(equals="back_order_data_keyboard"), state=CreateOrder.states_names)
    dp.register_callback_query_handler(order_short_description_button, Text(equals="short_description"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_short_description, state=CreateOrder.waiting_for_short_description)
    dp.register_callback_query_handler(order_price_button, Text(equals="price"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_price, state=CreateOrder.waiting_for_price)
    dp.register_callback_query_handler(order_address_button, Text(equals="address"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_address, state=CreateOrder.waiting_for_address)

    dp.register_callback_query_handler(order_content_button, Text(equals="content"), state=CreateOrder.waiting_for_order_data)
    dp.register_callback_query_handler(order_message_button, Text(equals="message"), state=CreateOrder.waiting_for_content)
    dp.register_message_handler(enter_message, state=CreateOrder.waiting_for_content_message)

    dp.register_callback_query_handler(order_photo_button, Text(equals="photo"), state=CreateOrder.waiting_for_content)
    dp.register_message_handler(enter_photo, content_types=ContentType.ANY, state=CreateOrder.waiting_for_content_photo)

    dp.register_callback_query_handler(order_video_button, Text(equals="video"), state=CreateOrder.waiting_for_content)
    dp.register_message_handler(enter_video, content_types=ContentType.ANY, state=CreateOrder.waiting_for_content_video)

    dp.register_callback_query_handler(order_audio_button, Text(equals="audio"), state=CreateOrder.waiting_for_content)
    dp.register_message_handler(enter_audio, content_types=ContentType.ANY, state=CreateOrder.waiting_for_content_audio)

    dp.register_callback_query_handler(finish_order_data_setup, Text(equals="save_order_data"), state=CreateOrder.waiting_for_order_data)
