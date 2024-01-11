from aiogram import F, Router, types
from app.bot.messages import *
from app.bot.middlewares.answer import AnswerMiddleware
from app.utils.history import update_history, get_history, represent_history
from app.ai.pipeline import answer

router = Router()
router.message.middleware(AnswerMiddleware())


@router.message(F.text)
async def text_message_handler(message: types.Message, history_mode: str):
    """Answer a user's message with LM"""

    chat_id = message.chat.id
    bot = message.bot

    await update_history(chat_id=chat_id, role="first", content=message.text, mode=history_mode)
    
    await bot.send_chat_action(chat_id=chat_id, action='typing')
    history = await get_history(chat_id)
    represented_history = await represent_history(history)
    lm_answer = await answer(represented_history)

    await update_history(chat_id=chat_id, role="second", content=lm_answer)

    await message.reply(lm_answer)
