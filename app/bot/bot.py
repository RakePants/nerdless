import logging

from aiogram import Bot, Dispatcher

import app.bot.handlers.config as config
import app.bot.handlers.echo as echo
from app.settings import settings


async def start_bot():

    # Initialize bot and dispatcher
    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()

    dp.include_router(config.router)
    dp.include_router(echo.router)

    if settings.mode == "webhook":
        await bot.set_webhook(settings.webhook_url + '/' + settings.telegram_token)
        logging.info(f"Start webhook mode on port {settings.port}")
    else:
        logging.info(f"Start polling mode")
        
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
