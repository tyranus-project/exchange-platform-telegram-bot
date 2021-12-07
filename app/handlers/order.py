from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from loguru import logger

from app.keyboards.inline import call_order_data_keyboard, call_order_categories_keyboard


order_categories = ["Information", "Documents", "Photos", "Videos", "Location", "Other"]


class CreateOrder(StatesGroup):
    waiting_for_order_data = State()
    waiting_for_order_name = State()
    waiting_for_order_category = State()
    waiting_for_short_description = State()
    waiting_for_price = State()
    waiting_for_address = State()


async def setup_order_data(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
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


async def finish_order_data_setup(callback: types.CallbackQuery, state: FSMContext):
    # order_data = await state.get_data()
    # logger.info(f"{order_data}")
    await callback.message.edit_text("Finished")
    await state.reset_state()


def register_order_handlers(dp: Dispatcher):
    dp.register_message_handler(setup_order_data, Text(equals="Create order", ignore_case=True))
    dp.register_callback_query_handler(order_name_button, Text(equals="name"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_order_name, state=CreateOrder.waiting_for_order_name)
    dp.register_callback_query_handler(order_category_button, Text(equals="categories"), state=CreateOrder.waiting_for_order_data)
    dp.register_callback_query_handler(enter_order_category, Text(startswith="category"), state=CreateOrder.waiting_for_order_category)
    dp.register_callback_query_handler(back_setup_order_data, Text(equals="back_order_data_keyboard"), state=CreateOrder.waiting_for_order_category)
    dp.register_callback_query_handler(order_short_description_button, Text(equals="short_description"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_short_description, state=CreateOrder.waiting_for_short_description)
    dp.register_callback_query_handler(order_price_button, Text(equals="price"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_price, state=CreateOrder.waiting_for_price)
    dp.register_callback_query_handler(order_address_button, Text(equals="address"), state=CreateOrder.waiting_for_order_data)
    dp.register_message_handler(enter_address, state=CreateOrder.waiting_for_address)
    dp.register_callback_query_handler(finish_order_data_setup, Text(equals="save_order_data"), state=CreateOrder.waiting_for_order_data)
