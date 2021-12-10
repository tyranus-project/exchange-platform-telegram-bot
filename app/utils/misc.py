from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

from loguru import logger

from app.keyboards.inline import call_setup_order_keyboard, call_order_categories_keyboard, order_content_keyboard
from app.loader import db


