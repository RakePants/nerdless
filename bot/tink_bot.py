from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import random
from transformers import AutoTokenizer, AutoModelWithLMHead


tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-small')
model = AutoModelWithLMHead.from_pretrained('C:/Users/Миша/PycharmProjects/nlp/tink')
model = model.to('cpu')

bot_token = open("C:/Users/Миша/PycharmProjects/nlp/token.txt").readline()
bot = Bot(token=bot_token)
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
        
    response.replace('<pad>', '')
    response.replace('�', '')
    
    for ch in ['))', '((', '!!!', '???', '(c', '(с', '()', '11', '00', 'адин']:
        if ch in response:
            response = response.partition(ch)[0]
    
    return response
    

text = ""
counter_text = 1
num_msg = 0
@dp.message_handler()
async def tink(message : types.message):
    
    global num_msg
    global counter_text
    global text
    num_msg += 1
    
    if (num_msg > 5):
        text = gener("@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@")[0]
        await message.reply(text.split("@@ВТОРОЙ@@")[1])
        num_msg = 0
        counter_text = 1
    elif message.reply_to_message and message.reply_to_message['from']["id"] == 5616329848:
        counter_text += 1
        text1 = gener(text + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@")[0]
        await message.reply(text1.split("@@ВТОРОЙ@@")[counter_text])
        num_msg = 0
        text = text1

        # # # await message.reply(message.text)
        # await bot.send_message(message.from_user.id, message.text)


executor.start_polling(dp, skip_updates=True)
