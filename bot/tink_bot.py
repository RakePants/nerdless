from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import random
import re
from transformers import AutoTokenizer, AutoModelWithLMHead


tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-small')
model = AutoModelWithLMHead.from_pretrained('../weights/nerdless_trained_sad1')
model = model.to('cpu')

BOT_TOKEN_PATH = "token.txt"
bot_token = open(BOT_TOKEN_PATH).readline()
bot = Bot(token=bot_token)
BOT_ID = 5616329848
dp = Dispatcher(bot)

history = ""
@dp.message_handler(commands=["start"])
async def start(message : types.message):
    await message.answer("Я здесь")
    history = "@@ВТОРОЙ@@ " + "Я здесь"

# answer generation and handling
def generate(input):
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
    
    if ', ' in response[:4]:
        response = response.replace(', ', '')
        
    if '.' in response[:3]:
        response = response.replace('.', '')
    
    response = re.sub("/b/$", "", response)
    response = response.replace('<pad>', '')
    response = response.replace('�', '')
    response = response.replace('тред', 'чат')
    response = response.replace('тхреад', 'чат')
    response = response.replace('Тред', 'Чат')
    response = response.replace('/b/', 'тг')
    
    for ch in ['))', '((', '!!!', '???', '(c', '(с', '(С', '(C','()', 'адин']:
        if ch in response:
            response = response.partition(ch)[0]
    
    return response
    

num_msg = 0
@dp.message_handler()
async def tink(message : types.message):
    
    global num_msg
    global counter_text
    global history
    num_msg += 1
    
    if (num_msg > 5):
        history = ""
        response = generate("@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ ")
        await message.reply(response)
        num_msg = 0
        history = "@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
        
    elif message.reply_to_message and message.reply_to_message['from']["id"] == BOT_ID:
        if message.text.lower() == "хватит":
            history = ""
            await message.reply("ладно")
            num_msg = 0
        else:
            num_msg = 0
            response = generate(history + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ ")
            history = history + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
            await message.reply(response)


executor.start_polling(dp, skip_updates=True)
