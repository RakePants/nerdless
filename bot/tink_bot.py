from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import random
from transformers import AutoTokenizer, AutoModelWithLMHead

PATH_TO_MODEL = 'C:/Users/Миша/PycharmProjects/nlp/tink'
tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-small')
model = AutoModelWithLMHead.from_pretrained(PATH_TO_MODEL)

PATH_TO_BOT_TOKEN = "C:/Users/Миша/PycharmProjects/nlp/token.txt"
bot_token = open(PATH_TO_BOT_TOKEN).readline()
bot = Bot(token="bot_token")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message : types.message):
    await message.answer("пук пук")


c = 0
@dp.message_handler()
async def tink(message : types.message):
    global c
    c+=1
    if (c > 5) or (message.reply_to_message and message.reply_to_message['from']["id"] == 5616329848):
        inputs = tokenizer("@@ПЕРВЫЙ@@ " + str(message.text.lower()) + " @@ВТОРОЙ@@", return_tensors='pt')
        generated_token_ids = model.generate(
            **inputs,
            top_k=10,
            top_p=0.95,
            num_beams=1,
            num_return_sequences=1,
            do_sample=True,
            no_repeat_ngram_size=2,
            temperature=0.1,
            repetition_penalty=1.2,
            length_penalty=1.0,
            eos_token_id=50257,
            max_new_tokens=20
        )
        context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
        await message.reply(context_with_response[0].split("@@ВТОРОЙ@@")[1])
        c = 0

        # # # await message.reply(message.text)
        # await bot.send_message(message.from_user.id, message.text)


executor.start_polling(dp, skip_updates=True)
