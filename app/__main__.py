from aiogram import Dispatcher, executor

from loguru import logger

from app import handlers
from app.loader import exchange_platform_dispatcher
from app.utils.set_bot_commands import set_default_commands


async def on_startup(dp: Dispatcher):
    handlers.setup_handlers(dp)
    await set_default_commands(dp)
    logger.info("Exchange platform bot launched!")


async def on_shutdown(dp: Dispatcher):
    logger.info("Shutting down...")
    # await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info("Exchange platform bot finished!")


if __name__ == "__main__":
    logger.info("Starting Exchange platform bot...")
    executor.start_polling(exchange_platform_dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)
