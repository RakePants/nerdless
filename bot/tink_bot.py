import re
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from transformers import AutoTokenizer, AutoModelWithLMHead
from functools import lru_cache

tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-medium')
model = AutoModelWithLMHead.from_pretrained('../weights/nerdless_trained5')
model = model.to('cpu')

BOT_TOKEN_PATH = "token.txt"
bot_token = open(BOT_TOKEN_PATH).readline()
bot = Bot(token=bot_token)
BOT_ID = 5616329848
dp = Dispatcher(bot)


history_dict = dict()
@dp.message_handler(commands=["start"])
async def start(message : types.message):
    await message.answer("Я здесь" + u'🤖')
    global history_dict
    history_dict[message.chat.id] = "@@ВТОРОЙ@@ " + "Я здесь " + u'🤖'
    

# answer generation and handling
def generate(input, username):
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
        max_new_tokens=30
    )

    context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
    print(context_with_response)

    # raw response handling
    response = context_with_response[0].split('@@')[-1].strip()
    
    response = response.replace('<pad>', '')
    response = response.replace('�', '')
    response = re.sub("^[.,] ", "", response)
    response = re.sub("/b.?$", "", response)
    response = re.sub('/b.?', u'🤖', response)
    response = re.sub('[тТ]ре[а-я]д?', 'чат', response)
    response = re.sub("[Аа]нон[а-я]?", username, response)
    
    for ch in ['))', '((', '!!!', '???', '(c', '(с', '(С', ')(', '(C','()', 'адин']:
        if ch in response:
            response = response.partition(ch)[0]
    
    return response
    

num_msg = 0
@dp.message_handler()
async def tink(message : types.message):

    global num_msg
    global history_dict
    num_msg += 1
    
    if (num_msg > 5) or ('@testnalohabot' in message.text.lower()):
        history_dict[message.chat.id] = ""
        response = generate("@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " , message['from']['first_name'])
        await message.reply(response)
        num_msg = 0
        history_dict[message.chat.id] = "@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
        
    elif message.reply_to_message and (message.reply_to_message['from']["id"] == BOT_ID):
        if message.text.lower().strip() == "хватит":
            history_dict[message.chat.id] = ""
            await message.reply("ладно, проехали")
            num_msg = 0
        else:
            num_msg = 0
            response = generate(history_dict[message.chat.id] + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ ", message['from']['first_name'])
            history_dict[message.chat.id] = history_dict[message.chat.id] + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
            await message.reply(response)


executor.start_polling(dp, skip_updates=True)
