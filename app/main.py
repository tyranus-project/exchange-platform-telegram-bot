from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import BOT_TOKEN
from app.handlers.default import register_default_handlers
from app.utils.set_bot_commands import set_default_commands


async def on_startup(dp: Dispatcher):
    await set_default_commands(dp)
    register_default_handlers(dp)


async def on_shutdown(dp: Dispatcher):
    await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    exchange_platform_bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = MemoryStorage()
    exchange_platform_dispatcher = Dispatcher(exchange_platform_bot, storage=storage)
    executor.start_polling(exchange_platform_dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)
