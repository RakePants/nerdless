import re
from random import choice
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-medium')
model_sad = AutoModelWithLMHead.from_pretrained('../weights/nerdless_trained_sad1')
model_toxic = AutoModelWithLMHead.from_pretrained('../weights/nerdless_trained5')
model_vulgar = AutoModelWithLMHead.from_pretrained('../weights/nerdless_trained_vulgar1')

BOT_TOKEN_PATH = "token.txt"
bot_token = open(BOT_TOKEN_PATH).readline()
bot = Bot(token=bot_token)
BOT_ID = int(bot_token.split(':')[0])
BOT_NAME = "nerdless_bot"
dp = Dispatcher(bot)


history_dict = dict()
@dp.message_handler(commands=["start"])
async def start(message : types.message):
    await message.answer("Я здесь " + u'🤖' + '\n' + "сейчас выбран режим sad")
    global history_dict
    history_dict[message.chat.id] = ["@@ВТОРОЙ@@ " + "Я здесь " + u'🤖' + "сейчас выбран режим sad", model_sad, "режим sad", 0]
    
    
@dp.message_handler(commands=["help"])
async def send_help(message : types.message):
    await message.reply("/start - перезапуск бота.\n\nВ боте реализовано 3 режима: toxic, sad, vulgar. Между ними можно переключаться по командам /toxic, /sad, /vulgar.\n/preset - просмотреть режим\n\nБот самостоятельно отвечает на случайные сообщения.\nМожно принудительно начать диалог с ботом, упомянув его: @nerdless_bot <сообщение>.\n\nЧтобы начать диалог с ботом, когда он уже что-либо написал, используйте функцию reply. Бот будет помнить все сообщения такой цепочки.\nЧтобы закончить такой диалог с ботом и очистить его память, используйте /end.")


@dp.message_handler(commands=["sad"])
async def change_to_sad(message : types.message):
    global model_sad
    global history_dict
    
    await message.answer(u'⚫' + " Успешно выбран режим sad")
    history_dict[message.chat.id] = ["@@ВТОРОЙ@@ " + "Успешно выбран режим sad", model_sad, "режим sad " + u'😰', 0]
    

@dp.message_handler(commands=["toxic"])
async def change_to_toxic(message : types.message):
    global model_toxic
    global history_dict
    
    await message.answer(u'⚫' + " Успешно выбран режим toxic")
    history_dict[message.chat.id] = ["@@ВТОРОЙ@@ " + "Успешно выбран режим toxic", model_toxic, "режим toxic " + u'😡', 0]


@dp.message_handler(commands=["vulgar"])
async def change_to_vulgar(message : types.message):
    global model_vulgar
    global history_dict
    
    await message.answer(u'⚫' + " Успешно выбран режим vulgar")
    history_dict[message.chat.id] = ["@@ВТОРОЙ@@ " + "Успешно выбран режим vulgar", model_vulgar, "режим vulgar " + u'🍑', 0]
    
 
@dp.message_handler(commands=["preset"])
async def see_preset(message : types.message):
    global history_dict
    
    await message.answer(u'⚫' + "Сейчас выбран " + history_dict[message.chat.id][2])
    history_dict[message.chat.id][0] = u'⚫' + "@@ВТОРОЙ@@ " + "Сейчас выбран " + history_dict[message.chat.id][2]
    
    
# answer generation and handling
def generate(input, username, model):
    inputs = tokenizer(input, return_tensors='pt')
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
    #print(context_with_response)

    # raw response handling
    response = context_with_response[0].split('@@')[-1].strip()

    response = response.replace('<pad>', '')
    response = response.replace('�', '')
    response = re.sub("^[.,] ", "", response)
    response = re.sub("/b.?$", "", response)
    response = re.sub('/b.?', u'🤖', response)
    response = re.sub('[тТ]х?ре[а-я]?д', 'чат', response)
    response = re.sub("[Аа]нон[а-я]*", username, response)

    for ch in ['))', '((', '!!!', '???', '(c', '(с', '(С', '(C','()', ')(', 'адин']:
        if ch in response:
            response = response.partition(ch)[0]

    return response


@dp.message_handler(commands=["end"])
async def end_dialogue(message : types.message):
    global history_dict

    history_dict[message.chat.id][0] = ""
    history_dict[message.chat.id][3] = 0
    
    await message.reply("ладно, проехали")
    

@dp.message_handler()
async def tink(message : types.message):

    global history_dict
    history_dict[message.chat.id][3] += 1

    if message.reply_to_message and (message.reply_to_message['from']["id"] == BOT_ID):
        history_dict[message.chat.id][3] = 0
        response = generate(history_dict[message.chat.id][0] + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ ", message['from']['first_name'], history_dict[message.chat.id][1])
        history_dict[message.chat.id][0] = history_dict[message.chat.id][0] + " @@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
        await message.reply(response)

    elif (history_dict[message.chat.id][3] > choice([5, 6, 7, 8])) or (('@' + BOT_NAME) in message.text.lower() and '/' not in message.text.lower()):
        history_dict[message.chat.id][3] = 0
        response = generate("@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " , message['from']['first_name'], history_dict[message.chat.id][1])
        history_dict[message.chat.id][0] = "@@ПЕРВЫЙ@@ " + message.text.lower() + " @@ВТОРОЙ@@ " + response
        await message.reply(response)


executor.start_polling(dp, skip_updates=True)
