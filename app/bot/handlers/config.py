import logging

from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.utils.formatting import Italic, Text

from app.bot.messages import *
from app.database import models
from app.database.database import get_db
from app.utils.history import clear_history

router = Router()


@router.message(F.text, Command("start"))
async def start_command_handler(message: types.Message):
    """Send a message when the command /start is issued."""
    
    chat_id = message.chat.id

    logging.info(f"Bot started in chat {chat_id}")

    async with get_db() as db:
        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()

        if not chat:
            chat = models.Chat(id=chat_id)

            db.add(chat)
            db.commit()
            db.refresh(chat)

    text = Text(Italic(MSG_START))
    await message.answer(**text.as_kwargs())


@router.message(F.text, Command("help"))
async def help_command_handler(message: types.Message):
    """Send a help message when the command /help is issued."""
    
    text = Text(Italic("Справка:\n\n"), MSG_HELP)
    await message.answer(**text.as_kwargs())


@router.message(F.text, Command("reset"))
async def reset_command_handler(message: types.Message):
    """Reset message history"""
    
    chat_id = message.chat.id

    await clear_history(chat_id)

    text = Text(Italic(MSG_RESET_HISTORY))
    await message.answer(**text.as_kwargs())


@router.message(F.text, Command("frequency"))
async def frequency_command_handler(message: types.Message, command: CommandObject):
    """Change frequency when the command /frequency is issued."""
    
    chat_id = message.chat.id

    if command.args is None:
        text = Text(Italic(MSG_NO_ARGS))
        await message.answer(**text.as_kwargs())
        return

    try:
        frequency = int(command.args)

        if not(1 <= frequency <= 100):
            text = Text(Italic(MSG_WRONG_FREQUENCY))
            await message.answer(**text.as_kwargs())
            return
        
    except:
        text = Text(Italic(MSG_WRONG_FREQUENCY))
        await message.answer(**text.as_kwargs())
        return

    async with get_db() as db:

        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        chat.frequency = frequency / 100
        db.commit()
        db.refresh(chat)

    text = Text(Italic(MSG_FREQUENCY_UPDATED))
    await message.answer(**text.as_kwargs())


@router.message(lambda message: message.text.startswith('/'))
async def any_command_handler(message: types.Message):
    """Print unknown command on any command"""
    
    text = Text(Italic(MSG_NO_COMMAND))
    await message.answer(**text.as_kwargs())
