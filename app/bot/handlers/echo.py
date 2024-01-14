from aiogram import F, Router, types
from aiogram.utils.chat_action import ChatActionSender

from app.ai.pipeline import answer
from app.bot.messages import *
from app.bot.middlewares.answer import AnswerMiddleware
from app.utils.history import get_history, represent_history, update_history
from app.utils.processing import process_input

router = Router()
router.message.middleware(AnswerMiddleware())


@router.message(F.text)
async def text_message_handler(message: types.Message, history_mode: str):
    """Answer a user's message with LM"""

    chat_id = message.chat.id
    bot = message.bot
    bot_user = await bot.get_me()
    bot_username = f"@{bot_user.username}"

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):

        # Clean input from bot handle and cut to character limit
        input = await process_input(message.text, bot_username)
        await update_history(chat_id=chat_id, role="first", content=input, mode=history_mode)  # Push message to DB
        
        history = await get_history(chat_id)
        represented_history = await represent_history(history)  # Convert dialogue history to language model representation
        lm_answer = await answer(represented_history)

        await update_history(chat_id=chat_id, role="second", content=lm_answer)

    await message.reply(lm_answer)
