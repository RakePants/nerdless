import random
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.bot.messages import *
from app.database import models
from app.database.database import get_db


class AnswerMiddleware(BaseMiddleware):
    async def roll_chance(self, chat_id) -> bool:
        async with get_db() as db:
            chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
            chance = chat.frequency
            return random.random() < chance

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        if isinstance(event, Message):
            bot_user = await data["bot"].get_me()
            bot_username = f"@{bot_user.username}"

            # If bot is mentioned, always answer
            if bot_username in event.text: 
                data['history_mode'] = 'clear'  # Drop history
                return await handler(event, data)
            
            # If bot's message is replied or it's a private chat, always answer
            elif (event.reply_to_message and event.reply_to_message.from_user.id == bot_user.id) or event.chat.type == 'private':  
                data['history_mode'] = 'append'  # Keep history
                return await handler(event, data)
            
            # Roll dice on other messages 
            elif await self.roll_chance(event.chat.id): 
                data['history_mode'] = 'clear'   # Drop history
                return await handler(event, data)
