import asyncio
import logging

from app.bot.bot import DefaultConfig, start_bot
from app.database.models import create_all

# Start the Bot
if __name__ == "__main__":
    # Enable logging
    DefaultConfig.init_logging()
    logging.info(f"PORT: {DefaultConfig.PORT}")

    # Create all tables if they do not already exist
    asyncio.run(create_all())

    # Run the bot
    asyncio.run(start_bot())
