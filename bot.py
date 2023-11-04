'''Чтобы узнать, как заполнить конфигурационный файл (conf), прочитайте урок, ссылка на который дана в readme.
Из файла убраны прямые ссылки на медиа и айди из телеграмма.
Они заменены фразами mapid, videoid, bingoid, yourtelegramid, FEEDBACKGROUPID и так далее.'''

import json
import random
import time
import flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import conf

TOKEN = conf.TOKEN
WEBHOOK_HOST = conf.WEBHOOK_HOST
WEBHOOK_PORT = conf.WEBHOOK_PORT

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TOKEN)

bot = telebot.TeleBot(TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# подгружаем текстовые медиа / ссылки на медиафайлы которые лежат на облаке
with open('/home/username/projectfolder/journal.tsv', encoding='utf-8') as f:
    quotes = f.readlines()
with open('/home/username/projectfolder/photos.txt', encoding='utf-8') as f:
    photos = f.readlines()
photos = [p.strip('\n') for p in photos]
with open('/home/username/projectfolder/script.json', encoding='utf-8') as f:
    script = json.loads(f.read())

userdict = {}
photodict = {}
quotedict = {}

# Генерируем клавитуру, которая появляется при нажатии /start
def gen_markup(digit):
    next = str(int(digit) + 1)
    markup = InlineKeyboardMarkup()
    if digit == '1':
        markup.add(InlineKeyboardButton("2. Начать путешествие по корпусу!", callback_data="2"))
        markup.add(InlineKeyboardButton("О спектакле", callback_data="team"))
        return markup

    markup.add(InlineKeyboardButton("В начало", callback_data="1"))
    markup.add(InlineKeyboardButton(script[next]['heading'].strip('*'), callback_data=next))
    markup.add(InlineKeyboardButton("О спектакле", callback_data="team"))
    return markup

# Генерируем шаблонный ответ на выбор пользователя
def generate_call(call):
    numbid = call.data
    header = script[numbid]['heading']
    if 'content' in script[numbid].keys():
        content = script[numbid]['content']
        text = header + '\n\n' + content
        bot.send_message(call.from_user.id, text, parse_mode='Markdown', reply_markup=gen_markup(call.data))

    if 'link' in script[numbid].keys():
        link = script[numbid]['link']
        bot.send_audio(call.from_user.id, f'https://docs.google.com/uc?id={link}')

# В зависимости от эпизода спектакля, пользователю выдаются разные медиа.
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "1":
        send_welcome(call.from_user.id)
        bot.answer_callback_query(call.id)

    elif call.data == "10":
        bot.answer_callback_query(call.id)
        generate_call(call)
        time.sleep(0.2) # чтобы не перегрузить глаза пользователя, медиа отправляются с небольшой задержкой
        bot.send_photo(call.from_user.id, "https://docs.google.com/uc?id=mapid")

#       в Спектакле есть эпизод, в котором пользователю предлагается отвечать на вопросы.
#       Телеграм создает новый опрос в каждом чате, поэтому, чтобы другие пользователи могли увидеть,
#       что ответили участни_цы спектакля до них, я пересылаю каждому пользователю опрос, который был сгенерирован в чате со мной.
  
    elif call.data == "13":
        bot.answer_callback_query(call.id)
        bot.send_message(call.from_user.id, "*13. Вперёд к исследованию сообществ!*", parse_mode='Markdown')
        time.sleep(0.2)
        for idi in ['214', '215', '216', '217', '218']:
            bot.forward_message(call.from_user.id, yourtelegramid, idi)
            time.sleep(1)

        call.data = "18"
        generate_call(call)
    elif call.data == "19":
        bot.answer_callback_query(call.id)
        bot.send_message(call.from_user.id, "*19. Проверим!*", parse_mode='Markdown')
        time.sleep(0.2)
        for idi in ['289', '290', '291', '292', '293']:
            bot.forward_message(call.from_user.id, yourtelegramid, idi)
            time.sleep(1)
        call.data = "24"
        generate_call(call)

    elif call.data == "25":
        bot.answer_callback_query(call.id)
        bot.send_message(call.from_user.id, "*25. Посмотрим!*", parse_mode='Markdown')
        time.sleep(0.2)
        for idi in ['319', '320', '321', '322', '323']:
            bot.forward_message(call.from_user.id, yourtelegramid, idi)
            time.sleep(1)
        call.data = "30"
        generate_call(call)

    elif call.data == "33":
        bot.answer_callback_query(call.id)
        generate_call(call)
        time.sleep(0.5)
        bot.send_video(call.from_user.id, 'https://docs.google.com/uc?id=videoid', supports_streaming=True) 

    elif call.data == "34":
        bot.answer_callback_query(call.id)
        generate_call(call)
        bot.send_photo(call.from_user.id, "https://docs.google.com/uc?id=bingoid")

    elif call.data == '48':
        bot.answer_callback_query(call.id)

        numbid = call.data
        header = script[numbid]['heading']
        content = script[numbid]['content']
        text = header + '\n\n' + content

        next = str(int(numbid) + 1)
        markup = InlineKeyboardMarkup()

        markup.add(InlineKeyboardButton("В начало", callback_data="1"))
        markup.add(InlineKeyboardButton("Журнал: часть 1", callback_data="mood1"))
        markup.add(InlineKeyboardButton("Журнал: часть 2", callback_data="mood2"))
        markup.add(InlineKeyboardButton("Журнал: часть 3", callback_data="mood3"))
        markup.add(InlineKeyboardButton("Фотографии", callback_data="randomphoto"))
        markup.add(InlineKeyboardButton("Случайные цитаты из журнала", callback_data="randomquote"))
        markup.add(InlineKeyboardButton("Сделать запись в журнале", callback_data="sharemood"))
        markup.add(InlineKeyboardButton(script[next]['heading'].strip('*'), callback_data=next))
        markup.add(InlineKeyboardButton("О спектакле", callback_data="team"))

        bot.send_message(call.from_user.id, text, parse_mode='Markdown', reply_markup=markup)
        time.sleep(0.5)
        bot.send_message(call.from_user.id, "_Если вдруг потерятесь в количестве медиа, вернитесь к этой записи и выберите пункт «Закончить изучение настроений»_", parse_mode="Markdown")


    elif call.data == '57':
        bot.answer_callback_query(call.id)
      
        numbid = call.data
        header = script[numbid]['heading']
        if 'content' in script[numbid].keys():
            content = script[numbid]['content']
            text = header + '\n\n' + content
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("В начало", callback_data="1"))
            markup.add(InlineKeyboardButton("О спектакле", callback_data="team"))
            bot.send_message(call.from_user.id, text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'mood1':
        bot.answer_callback_query(call.id)
        bot.send_audio(call.from_user.id, 'https://docs.google.com/uc?id=audioid') #tonya
    elif call.data == 'mood2':
        bot.answer_callback_query(call.id)
        bot.send_audio(call.from_user.id, 'https://docs.google.com/uc?id=audioid') #sasha
    elif call.data == 'mood3':
        bot.answer_callback_query(call.id)
        bot.send_audio(call.from_user.id, 'https://docs.google.com/uc?id=audioid') #lyonya

#       в секции "Дневник настроений" есть возможность просмотреть случайные фотографии / цитаты.
#       Для каждого пользователя создается отдельный словарь фото / цитат, которые ему уже отправлялись.
#       При выборе "Прислать еще" присылаются новые фото/цитаты, которы участни_ца еще не видела.
#       Из словаря они удаляются.  
    
    elif call.data == 'randomphoto':
        bot.answer_callback_query(call.id)
        if call.from_user.id not in photodict.keys():
            photodict[call.from_user.id]  = [i for i in range(len(photos))]
        ids = photodict[call.from_user.id]
        if len(ids) > 0:
            selection = random.choice(ids)
            ids.remove(selection)
            photodict[call.from_user.id] = list(ids)
            bot.send_photo(call.from_user.id, f"https://docs.google.com/uc?id={photos[selection]}")
            time.sleep(1)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Да", callback_data="randomphoto"))
            markup.add(InlineKeyboardButton("Вернуться в меню", callback_data="48"))
            bot.send_message(call.from_user.id, 'Прислать еще?', reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Вернуться в меню", callback_data="48"))
            bot.send_message(call.from_user.id, 'Вы посмотрели все фотографии!', reply_markup=markup)

    elif call.data == 'randomquote':
        bot.answer_callback_query(call.id)
        if call.from_user.id not in quotedict.keys():
            quotedict[call.from_user.id]  = [i for i in range(len(quotes))]

        ids = quotedict[call.from_user.id]
        if len(ids) > 0:
            selection = random.choices(ids, k=10)
            ids = set(ids) - set(selection)
            quotedict[call.from_user.id] = list(ids)
            for item in list(selection):
                bot.send_message(call.from_user.id, quotes[item])
                time.sleep(1)

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Да", callback_data="randomquote"))
            markup.add(InlineKeyboardButton("Вернуться в меню", callback_data="48"))
            bot.send_message(call.from_user.id, 'Прислать еще?', reply_markup=markup)

        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Вернуться в меню", callback_data="48"))
            bot.send_message(call.from_user.id, 'Вы прочитали все цитаты!', reply_markup=markup)

    elif call.data == 'sharemood':
        bot.answer_callback_query(call.id)
        bot.send_message(call.from_user.id, 'Выберите команду /basmachmood')

    elif call.data == "team":
        bot.answer_callback_query(call.id)
        bot.send_message(call.from_user.id, '''*Команда спектакля:*\n
• Антонина Морозова (сценарий)
• Леонид Болховский (саунд-дизайн)
• Анастасия Панасюк (бот)
• Александра Хвостова
• Алевтина Намёткина
• Елизавета Иванова
• Митя Лобанов
• Диана Габитова

В спектакле использованы фотографии Фёдора Рощина и трек «Menysid» (Nicolas Jaar).

_Передать сообщение команде: /thankyoukurilka_''', parse_mode="Markdown")

    else:
        bot.answer_callback_query(call.id)
        generate_call(call)



# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if isinstance(message, telebot.types.Message):
        sendto = message.chat.id
    else:
        sendto = message
    bot.send_message(
        sendto,
        '''Привет, дорогой участник или участница спектакля\!
Мы — команда аудиоспектакля «Невидимый Басмач», проводником в который служит этот чудесный телеграм\-бот\.
Чтобы ваш театральный опыт состоялся в полной мере, подготовьте, пожалуйста, заряженный телефон с наушниками и исследовательский интерес\.
Как только вы будете готовы начать, нажмите, пожалуйста, на кнопку «Начать путешествие по корпусу\!»\.

Спектакль идет 1\-1\.5 часа\.

_Боту может понадобиться несколько секунд, чтобы «проснуться»\. Если этого не происходит или у вас есть другие технические вопросы, пишите @mjolnika\. В крайнем случае ||вы можете воспользоваться записью спектакля [здесь](https://t.me/+SfgwTvzXBn9hMzIy)\.||_''',
        reply_markup=gen_markup('1'), parse_mode='MarkdownV2', disable_web_page_preview=True)

# Обработчик обратной связи6 функции, которые пересылают сообщения в чат команды
@bot.message_handler(commands=['basmachroad', 'basmachfeelings', 'basmachmood', 'basmachstory', 'thankyoukurilka'])
def logmessage(message):
    userid = message.chat.id
    if userid not in userdict.keys():
        userdi = {
            'basmachroad':0,
            'basmachfeelings':0,
            'basmachmood': 0,
            'basmachstory':0,
            'thankyoukurilka':0
        }
        userdict[userid] = userdi
    tag = message.text.strip('/')
    userdict[userid][tag] = 1
    bot.send_message(userid, "_Введите сообщение, которое вы хотите передать:_", parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def forwardtext(message):
    userid = message.chat.id
    if userid in userdict.keys():
        for k, v in userdict[userid].items():
            if v == 1:
                bot.send_message(FEEDBACKGROUPID, f"*{k.replace('basmach', '').upper()}*:\n\n{message.text}", parse_mode='Markdown')
                userdict[userid][k] = 0
                bot.send_message(userid, "Спасибо! Мы получили ваше сообщение.")

@bot.message_handler(content_types=['voice'])
def forwardvoice(message):
    userid = message.chat.id
    if userid in userdict.keys():
        for k, v in userdict[userid].items():
            if v == 1:
                bot.send_message(FEEDBACKGROUPID, f"*{k.replace('basmach', '').upper()}VOICE*:", parse_mode='Markdown')
                bot.send_voice(FEEDBACKGROUPID, message.voice.file_id)
                userdict[userid][k] = 0
                bot.send_message(userid, "Спасибо! Мы получили ваше сообщение.")


@bot.message_handler(content_types=['sticker'])
def forwardsticker(message):
    userid = message.chat.id
    if userid in userdict.keys():
        for k, v in userdict[userid].items():
            if v == 1:
                bot.send_message(FEEDBACKGROUPID, f"*{k.replace('basmach', '').upper()}STICKER*:", parse_mode='Markdown')
                bot.send_sticker(FEEDBACKGROUPID, message.sticker.file_id)
                userdict[userid][k] = 0
                bot.send_message(userid, "Спасибо! Мы получили ваше сообщение.")


@bot.message_handler(content_types=['photo'])
def forwardphoto(message):
    userid = message.chat.id
    if userid in userdict.keys():
        for k, v in userdict[userid].items():
            if v == 1:
                bot.send_message(FEEDBACKGROUPID, f"*{k.replace('basmach', '').upper()}IMAGE*:", parse_mode='Markdown')
                bot.send_photo(FEEDBACKGROUPID, message.photo[-1].file_id)
                userdict[userid][k] = 0
                bot.send_message(userid, "Спасибо! Мы получили ваше сообщение.")

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
