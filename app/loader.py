from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from app.config import BOT_TOKEN, REDIS_HOST, REDIS_PORT


exchange_platform_bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(REDIS_HOST, REDIS_PORT, db=5)
exchange_platform_dispatcher = Dispatcher(exchange_platform_bot, storage=storage)
