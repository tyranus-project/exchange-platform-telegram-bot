from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import asyncio
import uvloop

from app.config import *
from app.db.database import Database


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()

exchange_platform_bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(REDIS_HOST, REDIS_PORT, db=5)
exchange_platform_dispatcher = Dispatcher(exchange_platform_bot, loop=loop, storage=storage)
db = Database(name=PG_NAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT, loop=loop)
