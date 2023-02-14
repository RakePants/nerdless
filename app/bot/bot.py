import re
import random
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

class ChatInfo():
    def __init__(self):
        self.history = ""
        self.model = model_sad
        self.model_name_text = "режим sad"
        self.num_msg = 0
        self.cooldown = (5, 9)
               
chats_info = dict()
''' chats_info = {chat_id_1: ChatInfo(), 
    chat_id_2: ChatInfo(),
    ...}
'''


@dp.message_handler(commands=["start"])
async def start(message : types.message):
    await message.answer(f"Бот запущен {u'🤖'}")
    global chats_info
    chats_info[message.chat.id] = ChatInfo()
    
    
@dp.message_handler(commands=["help"])
async def send_help(message : types.message):
    await message.reply("/start - перезапуск бота.\n\nВ боте реализовано 3 режима: toxic, sad, vulgar. Между ними можно переключаться по командам /toxic, /sad, /vulgar.\n/status -  посмотреть состояние бота\n\nБот самостоятельно отвечает на случайные сообщения.\nМожно принудительно начать диалог с ботом, упомянув его: @nerdless_bot <сообщение>.\n\nЧтобы начать диалог с ботом, когда он уже что-либо написал, используйте функцию reply. Бот будет помнить все сообщения такой цепочки.\nЧтобы закончить такой диалог с ботом и очистить его память, используйте /end.")


@dp.message_handler(commands=["sad"])
async def change_to_sad(message : types.message):
    global model_sad
    global chats_info
    
    chats_info[message.chat.id].model = model_sad
    chats_info[message.chat.id].model_name_text = "режим sad"
    await message.answer(f"{u'⚫'} Успешно выбран режим sad")
    

@dp.message_handler(commands=["toxic"])
async def change_to_toxic(message : types.message):
    global model_toxic
    global chats_info
    
    chats_info[message.chat.id].model = model_toxic
    chats_info[message.chat.id].model_name_text = "режим toxic"
    await message.answer(f"{u'⚫'} Успешно выбран режим toxic")


@dp.message_handler(commands=["vulgar"])
async def change_to_vulgar(message : types.message):
    global model_vulgar
    global chats_info
    
    chats_info[message.chat.id].model = model_vulgar
    chats_info[message.chat.id].model_name_text = "режим vulgar"
    await message.answer(f"{u'⚫'} Успешно выбран режим vulgar")
  
    
@dp.message_handler(commands=["cooldown"])
async def set_cooldown(message : types.message):
    global chats_info
    try:
        if all(int(words) >= 3 for words in message.text.split(' ')[1:]):
            if (len(message.text.split(' ')) == 3) and (int(message.text.split(' ')[1]) <= int(message.text.split(' ')[2])):
                cooldown_tuple = int(message.text.split(' ')[1]), int(message.text.split(' ')[2])
                
                chats_info[message.chat.id].cooldown = cooldown_tuple
                await message.answer(f"{u'⚫'} Cooldown ответа {str(cooldown_tuple[0])} - {str(cooldown_tuple[1])} сообщений")
                
            elif (len(message.text.split(' ')) == 2):
                cooldown_tuple = int(message.text.split(' ')[1]), int(message.text.split(' ')[1])
                
                chats_info[message.chat.id].cooldown = cooldown_tuple
                await message.answer(f"{u'⚫'} Cooldown ответа {str(cooldown_tuple[0])} сообщений")

            else:
                raise Exception()

        else:
            raise Exception()
        
    except:
        await message.answer(f"{u'⚫'} Введите команду правильно")
    

@dp.message_handler(commands=["end"])
async def end_dialogue(message : types.message):
    global chats_info

    chats_info[message.chat.id].history = ""
    chats_info[message.chat.id].num_msg = 0
    
    await message.reply("ладно, проехали")
    
    
@dp.message_handler(commands=["status"])
async def see_status(message : types.message):
    global chats_info
    
    await message.answer(f"{u'⚫'} Сейчас выбран {chats_info[message.chat.id].model_name_text}\nCooldown {str(chats_info[message.chat.id].cooldown[0])} - {str(chats_info[message.chat.id].cooldown[1])} сообщений\nВ чате {chats_info[message.chat.id].num_msg} сообщений") 
    
        
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

   
@dp.message_handler()
async def send_message(message : types.message):

    global chats_info
    chats_info[message.chat.id].num_msg += 1

    if message.reply_to_message and (message.reply_to_message['from']["id"] == BOT_ID):
        if (len(message.text) <= 200) and (chats_info[message.chat.id].history.count('@@ВТОРОЙ@@') <= 4):
            chats_info[message.chat.id].num_msg = 0
            response = generate(f"{chats_info[message.chat.id].history} @@ПЕРВЫЙ@@ {message.text} @@ВТОРОЙ@@ ", message['from']['first_name'], chats_info[message.chat.id].model)
            chats_info[message.chat.id].history = chats_info[message.chat.id].history + " @@ПЕРВЫЙ@@ " + message.text + " @@ВТОРОЙ@@ " + response
            await message.reply(response)
        else:
            chats_info[message.chat.id].num_msg = 0
            chats_info[message.chat.id].history = ""
            await message.reply(f"{u'⚫'} Много букв")

    elif (chats_info[message.chat.id].num_msg >= random.randint(chats_info[message.chat.id].cooldown[0], chats_info[message.chat.id].cooldown[1])) or (('@' + BOT_NAME) in message.text.lower() and '/' not in message.text.lower()) and (len(message.text) <= 200):
        chats_info[message.chat.id].num_msg = 0
        response = generate(f"@@ПЕРВЫЙ@@ {message.text} @@ВТОРОЙ@@ " , message['from']['first_name'], chats_info[message.chat.id].model)
        chats_info[message.chat.id].history = "@@ПЕРВЫЙ@@ " + message.text + " @@ВТОРОЙ@@ " + response
        await message.reply(response)


executor.start_polling(dp, skip_updates=True)
