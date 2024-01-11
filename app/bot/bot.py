import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import app.bot.handlers.echo as echo
import app.bot.handlers.config as config

load_dotenv()


class DefaultConfig:
    PORT = int(os.environ.get("PORT", 5000))
    TELEGRAM_TOKEN = os.environ.get("API_TELEGRAM", "")
    MODE = os.environ.get("MODE", "webhook")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=DefaultConfig.LOG_LEVEL,
        )


async def start_bot():

    # Initialize bot and dispatcher
    bot = Bot(token=DefaultConfig.TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(config.router)
    dp.include_router(echo.router)

    if DefaultConfig.MODE == "webhook":
        await bot.set_webhook(DefaultConfig.WEBHOOK_URL + '/' + DefaultConfig.TELEGRAM_TOKEN)
        logging.info(f"Start webhook mode on port {DefaultConfig.PORT}")
    else:
        logging.info(f"Start polling mode")
        
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
