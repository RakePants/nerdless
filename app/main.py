import asyncio
import logging

from app.bot.bot import start_bot
from app.database.models import create_all
from app.settings import settings


# Start the Bot
if __name__ == "__main__":
    
    # Enable logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=settings.log_level,
    )
    logging.info(f"PORT: {settings.port}")

    # Create all tables if they do not already exist
    asyncio.run(create_all())

    # Run the bot
    asyncio.run(start_bot())
