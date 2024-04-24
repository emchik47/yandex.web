import webbrowser
import telebot
from telebot import types
import sqlite3
import requests
from bs4 import BeautifulSoup
from config import TOKEN, StartText, UnCom, HelpText

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, StartText)
    if message.text == '/help':
        bot.send_message(message.chat.id, HelpText)


@bot.message_handler(commands=['randomfood'])
def eda(message):
    page = requests.get('http://89.108.110.52/sbs/random.shtml')
    soup = BeautifulSoup(page.text, "html.parser")
    pic = soup.findAll(class_='img2')
    link = soup.findAll(class_='btnGreen2 flR')
    x1 = page.text.find('<h1>')
    x2 = page.text.find('</h1>')
    name = page.text[x1 + 4:x2]
    subs = soup.findAll(class_='detail_img')
    subs = str(subs)
    x1 = subs.find('<p>')
    x2 = subs.find('</p>')
    subs = subs[x1 + 3:x2]
    subs = subs.rstrip()
    pic = str(pic)
    pic = "https://" + pic[pic.find('src') + 7:pic.find('jpg') + 3]
    pic = requests.get(pic)
    out = open('assets/img.jpg', 'wb')
    out.write(pic.content)
    out.close()
    link = str(link)
    link = "https:/" + link[link.find('//') + 1: link.find('shtml') + 5]
    bot.send_photo(message.chat.id, photo=open('assets/img.jpg', 'rb'),
                   caption=f'Название: {name}\n\nОписание: {subs}\n\nссылка: {link}', parse_mode='HTML')


@bot.message_handler(commands=['sportpit'])
def sportpit(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Спортивное питание🤩'))
    markup.add(types.KeyboardButton('Стероиды🔞'))
    bot.send_message(message.chat.id, "Выберите вид", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Спортивное питание🤩':
        mk = types.ReplyKeyboardMarkup()
        mk.add(types.KeyboardButton('Протеин'))
        mk.add(types.KeyboardButton('Креатин'))
        bot.send_message(message.chat.id, 'Что вас интересует?', reply_markup=mk)
        bot.register_next_step_handler(message, on_click1)

    if message.text == 'Стероиды🔞':
        mk = types.ReplyKeyboardMarkup()
        mk.add(types.KeyboardButton('Метан'))
        mk.add(types.KeyboardButton('Болденон'))
        bot.send_message(message.chat.id, 'Внимание: опасно☣ для здоровья. Информация представлена для '
                                          'ознакомления. Перед применением нужно проконсультироваться со специалистом',
                         reply_markup=mk)
        bot.register_next_step_handler(message, on_click2)


def on_click1(message):
    con = sqlite3.connect('webproject')
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM sportpit
                            WHERE name = '{message.text}'""").fetchone()
    result = list(result)
    vr = result[3].split('\n')
    for i in range(len(vr)):
        vr[i] = '• ' + vr[i]
    vr = '\n'.join(vr)
    result[3] = vr
    vr = result[4].split('\n')
    for i in range(len(vr)):
        vr[i] = '• ' + vr[i]
    vr = '\n'.join(vr)
    result[4] = vr
    mk = types.ReplyKeyboardRemove()
    x = f'Название: {result[1]}\n\nОписание: {result[2]}\n\nПлюсы:\n{result[3]}\n\nМинусы:\n{result[4]}'
    bot.send_photo(message.chat.id, photo=open(f'assets/{result[5]}', 'rb'), caption=x, reply_markup=mk)


def on_click2(message):
    con = sqlite3.connect('webproject')
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM steroids
                                WHERE name = '{message.text}'""").fetchone()
    result = list(result)
    vr = result[3].split('\n')
    for i in range(len(vr)):
        vr[i] = '• ' + vr[i]
    vr = '\n'.join(vr)
    result[3] = vr
    vr = result[4].split('\n')
    for i in range(len(vr)):
        vr[i] = '• ' + vr[i]
    vr = '\n'.join(vr)
    result[4] = vr
    mk = types.ReplyKeyboardRemove()
    x = f'Название: {result[1]}\n\nОписание: {result[2]}\n\nДействие на организм:\n{result[3]}\n\nПобочные эффекты:\n{result[4]}'
    bot.send_photo(message.chat.id, photo=open(f'assets/{result[5]}', 'rb'), caption=x, reply_markup=mk)


@bot.message_handler()
def text(message):
    if message.entities != None:
        if message.entities[0].type == 'bot_command':
            bot.send_message(message.chat.id, UnCom, parse_mode='HTML')


bot.infinity_polling()
