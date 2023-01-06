from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import random
from transformers import AutoTokenizer, AutoModelWithLMHead


tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-small')
model = AutoModelWithLMHead.from_pretrained('C:/Users/Миша/PycharmProjects/nlp/tink')
model = model.to('cpu')

BOT_TOKEN_PATH = "C:/Users/Миша/PycharmProjects/nlp/token.txt"
bot_token = open(BOT_TOKEN_PATH).readline()
bot = Bot(token=bot_token)
BOT_ID = 5616329848
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message : types.message):
    await message.answer("Я здесь")


def gener(input):
    inputs = tokenizer(str(input), return_tensors='pt')
    
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
        max_new_tokens=40
    )

    context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]

    # raw response handling
    response = context_with_response[0].split('@@')[-1].strip()
    
    if response[:2] == ', ':
        response = response[2:]
        
    response = response.replace('<pad>', '')
    response = response.replace('�', '')
    
    for ch in ['))', '((', '!!!', '???', '(c', '(с', '()', 'адин']:
        if ch in response:
            response = response.partition(ch)[0]
    
    return response
    

history = ""
num_msg = 0

@dp.message_handler()
async def tink(message : types.message):
    
    global num_msg
    global counter_text
    global history
    num_msg += 1
    
    if (num_msg > 5):
        history = ""
        response = gener("@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ ")
        await message.reply(response)
        num_msg = 0
        history = "@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
        
    elif message.reply_to_message and message.reply_to_message['from']["id"] == BOT_ID:
        response = gener(history + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ ")
        history = history + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
        await message.reply(response)
        num_msg = 0


executor.start_polling(dp, skip_updates=True)
