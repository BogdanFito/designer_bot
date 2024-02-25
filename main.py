from background import keep_alive
import telebot
from telebot import types
from Strings import Strings

bot = telebot.TeleBot('6976460514:AAG89jfnmFMr1Afv_iytwW8NwvCzCL1cOwU')
strings = Strings()
allow = False  # make it True if payment is completed


@bot.message_handler(commands=['start'])
def get_info(message):
    keyboard = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton('Подробнее', callback_data='switch')
    keyboard.add(switch_button)

    bot.send_message(message.from_user.id, strings.getGreeting(), reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    bot.send_message(message.from_user.id, strings.getMistake())


@bot.message_handler(func=lambda message: allow)
def send_ending(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Забрать чек-лист', url=' https://disk.yandex.ru/d/oTnvS1oxNtuxpQ')
    button2 = types.InlineKeyboardButton('Забрать 🎁', url='https://disk.yandex.ru/d/aEj9GTEANTUhmQ')
    keyboard.add(button1, button2)
    bot.send_message(message.from_user.id, strings.getEnding(), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'switch':
        keyboard = types.InlineKeyboardMarkup()
        switch_button = types.InlineKeyboardButton('Купить чек-лист', callback_data='switch2')
        keyboard.add(switch_button)
        bot.send_message(callback.message.chat.id, strings.getMoreDetails(), parse_mode='html', reply_markup=keyboard)
    if callback.data == 'switch2':
        bot.send_message(callback.message.chat.id, strings.getLink(), parse_mode='html')


keep_alive()
bot.polling(non_stop=True, interval=0)
