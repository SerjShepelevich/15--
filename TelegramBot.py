# pip install pyTelegramBotAPI
# https://github.com/eternnoir/pyTelegramBotAPI

import telebot
from telebot import apihelper
from datetime import datetime
import pandas as pd
import os
from pprint import pformat

TOKEN = ''

proxies = {
    'http': 'http://18.184.106.166:80',
    'https': 'http://83.97.23.90:18080',
}
admin_ID = 442341127

# загрузим старые заметки, если они есть
arhiv_zametok = 'arhive.csv'
if os.path.exists(arhiv_zametok):
    df = pd.read_csv(arhiv_zametok, sep=',')


apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def commnad_start_function(message):
    bot.reply_to(message, 'Рад Вас приветствовать. Бот архивариус готов!')

@bot.message_handler(commands = ['admin'], func = lambda message: message.from_user.id == admin_ID)
def admin(message):
    print(message)
    bot.reply_to(message, 'Хозяин, я рад тебя приветствовать!')


@bot.message_handler(commands = ['admin'])
def admin_(message):
    if (message.from_user.id == admin_ID):
        bot.reply_to(message, 'Хозяин, я рад тебя приветствовать!')
    else:
        bot.reply_to(message, 'Ты не мой хозяин!')

@bot.message_handler(commands = ['save'])
def save_record(message):
    arhiv_zametok = 'arhive.csv'
    if os.path.exists(arhiv_zametok):
        df = pd.read_csv(arhiv_zametok, sep = ',')
    else:
        df = pd.DataFrame()

    if (message.from_user.id == admin_ID):
        df1 = pd.DataFrame({'date':[datetime.now().date()],
            'text':[(message.text).replace('/save','')]})
        df = pd.concat([df, df1]).reset_index(drop = True)
        df.to_csv(arhiv_zametok, sep=',', index = False)
        bot.reply_to(message, f'Заметка сохранена')

@bot.message_handler(commands = ['show_all'])
def show_all(message):
    arhiv_zametok = 'arhive.csv'
    if os.path.exists(arhiv_zametok):
        df = pd.read_csv(arhiv_zametok, sep = ',')
    else:
        df = pd.DataFrame()
    if len(df.index) > 0:
        #formatted_result = pformat(df, width=80)
        formatted_result = rprint(df)
        bot.reply_to(message, f'Вот все заметки:\n {formatted_result}')
        #bot.reply_to(message, f'{formatted_result}')
    else:
        bot.reply_to(message, f'Ничего нет 8(')

@bot.message_handler(commands = ['del_rec'])
def del_rec(message):
    arhiv_zametok = 'arhive.csv'
    if os.path.exists(arhiv_zametok):
        df = pd.read_csv(arhiv_zametok, sep = ',')
    if (message.from_user.id == admin_ID):
        number_row = (message.text).replace('/del_rec','')
        number_row = int((number_row).replace(' ', ''))-1
        df = df.drop([number_row])
        df.to_csv(arhiv_zametok, sep=',', index = False)
        bot.reply_to(message, f'Строка удалена')

def rprint(df):
    text = ''
    for i in range(len(df.index)):
        text = text +str(i+1)+': ' +df.iloc[i]['date'] + ' ' + df.iloc[i]['text'] + '\n'
    return text


@bot.message_handler(content_types = ['text'])
def recieve_text(message):
    text = message.text
    bot.reply_to(message, f'Вы сказали:{text.upper()}')


# @bot.message_handler(content_types = ['text'])
# def recieve_text(message):
#     text = message.text
#     bot.reply_to(message, text[::-1])



bot.polling()