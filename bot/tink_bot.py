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
    await message.answer("Бот запущен")


c = 0
@dp.message_handler()
async def tink(message : types.message):
    global c
    c+=1
    if (c > 5) or (message.reply_to_message and message.reply_to_message['from']["id"] == 5616329848):
        
        model = model.to('cpu')
        inputs = tokenizer("@@ПЕРВЫЙ@@ " + str(message.text.lower()) + " @@ВТОРОЙ@@ ", return_tensors='pt')
        generated_token_ids = model.generate(
            **inputs,
            top_k=10,
            top_p=0.95,
            num_beams=3,
            num_return_sequences=1,
            do_sample=True,
            no_repeat_ngram_size=1,
            temperature=1.0,
            repetition_penalty=2.0,
            length_penalty=1.0,
            eos_token_id=50257,
            max_new_tokens=48
        )

        context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]

        s = context_with_response[0].split('@@')[-1].strip()
        if s[:2] == ', ':
            s = s[2:]
        s.replace('<pad>', '')
        s.replace('�', '')
        for ch in ['))', '((', '!!!', '???', '(c', '(с', '11', '00', 'адин']:
            if ch in s:
                s = s.partition(ch)[0]
        
        await message.reply(s)
        c = 0

        # # # await message.reply(message.text)
        # await bot.send_message(message.from_user.id, message.text)


executor.start_polling(dp, skip_updates=True)
