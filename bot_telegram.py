from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import random
import sqlite3



bot = Bot(token="5616329848:AAEMYlp2rYunBGxrCoeyw7n40WsohaNb-g4")
dp = Dispatcher(bot)
slova5 = ["Красавчик","Нихуя крутой","Зачетно"]
slova4 = ["Нормуль","Зачетно стелишь","Респект"]

base = sqlite3.connect("database.db")
cursor = base.cursor()




@dp.message_handler(commands=["stata"])
async def commands(message : types.message):
    win = cursor.execute(f"SELECT win FROM stata WHERE id == {message.from_user.id}").fetchall()
    win1 = int(str(win[0])[1])
    lose = cursor.execute(f"SELECT lose FROM stata WHERE id == {message.from_user.id}").fetchall()
    lose1 = int(str(lose[0])[1])
    itog = ""
    if win1 >= lose1:
        itog = "Норм поц"
    else:
        itog = "Лошара пиздец"
    await message.answer(f"Попал: {win1}, Промахнулся: {lose1} \nИтог: {itog} ")




@dp.message_handler(commands=["start"])
async def commands(message : types.message):
    try:
        cursor.execute("INSERT INTO stata VALUES(?,?,?)", (message.from_user.id, 0,0))
        base.commit()
    except:
        pass
    await message.answer("Отправь эмоджи '🏀' в чат")




@dp.message_handler(content_types="dice")
async def lol(message : types.dice):
    win = cursor.execute(f"SELECT win FROM stata WHERE id == {message.from_user.id}").fetchall()
    win1 = int(str(win[0])[1])
    lose = cursor.execute(f"SELECT lose FROM stata WHERE id == {message.from_user.id}").fetchall()
    lose1 = int(str(lose[0])[1])
    if message.dice.value == 5 and message.dice.emoji == "🏀":
        cursor.execute(f"UPDATE stata SET win = {win1 + 1} WHERE id == {message.from_user.id}")
        base.commit()
        await asyncio.sleep(4)
        await message.answer(slova5[random.randint(0,2)])
    if message.dice.value == 4 and message.dice.emoji == "🏀":
        await asyncio.sleep(4)
        await message.answer(slova4[random.randint(0,2)])
    if message.dice.value == 3 and message.dice.emoji == "🏀":
        await asyncio.sleep(4)
        await message.answer("кринжа выдал")
    if message.dice.value == 2 and message.dice.emoji == "🏀":
        await asyncio.sleep(4)
        await message.answer("Лох епт")
    if message.dice.value == 1 and message.dice.emoji == "🏀":
        cursor.execute(f"UPDATE stata SET lose = {lose1 + 1} WHERE id == {message.from_user.id}")
        base.commit()
        await asyncio.sleep(4)
        await message.answer("ЛОШАРАААА")

    # # # await message.reply(message.text)
    # await bot.send_message(message.from_user.id, message.text)






executor.start_polling(dp, skip_updates=True)