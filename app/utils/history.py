import ast
import json
import logging

from app.database import models
from app.database.database import get_db
from app.ai.lm import tokenizer


async def get_history(chat_id: int) -> list:
    """Get full history for text generation model"""

    async with get_db() as db:
        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        history = ast.literal_eval(str(chat.history))

    return history


async def update_history(chat_id: int, role: str, content: str = None) -> None:
    """Add message to history"""

    full_history = await get_history(chat_id)
    history = full_history[:3]

    async with get_db() as db:

        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()

        history.append({"role": role, "content": content})
        chat.history = json.dumps(history)

        db.commit()
        db.refresh(chat)

    logging.info(f"Updated history for chat {chat_id}")


async def clear_history(chat_id: int) -> None:
    """Replace the history with an empty list"""

    async with get_db() as db:
        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        chat.history = "[]"
        
        db.commit()
        db.refresh(chat)

    logging.info(f"Reset history for chat {chat_id}")


async def represent_history(history: list) -> str:
    """Turn JSON history into language model representation"""

    token_first = tokenizer.convert_ids_to_tokens(50257)  # @@ПЕРВЫЙ@@
    token_second = tokenizer.convert_ids_to_tokens(50258) # @@ВТОРОЙ@@

    representation = ""
    for item in history: representation += f"{token_first if item['role'] == 'first' else token_second}{item['content']}"
    representation += token_second

    return representation
