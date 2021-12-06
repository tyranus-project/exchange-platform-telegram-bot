from aiogram import Dispatcher

from loguru import logger

from .default import register_default_handlers
from .unsupported import register_unsupported_handlers


def setup_handlers(dp: Dispatcher):
    logger.info("Configuring handlers...")
    register_default_handlers(dp)
    register_unsupported_handlers(dp)
