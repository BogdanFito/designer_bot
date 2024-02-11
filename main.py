import os
from background import keep_alive
import pip
pip.main(['install', 'pytelegrambotapi'])
import telebot
from telebot import types
import time

bot = telebot.TeleBot('6976460514:AAG89jfnmFMr1Afv_iytwW8NwvCzCL1cOwU')

@bot.message_handler(commands=['start'])
def get_info(message):
  keyboard = types.InlineKeyboardMarkup()
  switch_button = types.InlineKeyboardButton('Подробнее', callback_data='switch')
  keyboard.add(switch_button)
  
  bot.send_message(message.from_user.id, "Приветствую!\nЗдесь ты можешь приобрести мой чек-лист «Первые шаги в ремонте» или узнать подробнее для кого он нужен.",  reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
  bot.send_message(message.from_user.id, 'Я вас не понимаю. Напишите /start и пользуйтесь встроенными кнопками.')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
  if callback.data == 'switch':
    keyboard = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton('Купить чек-лист', callback_data='switch2')
    keyboard.add(switch_button)
    bot.send_message(callback.message.chat.id, 'Чек-лист «Первые шаги в ремонте» состоит из 13 страниц самой полезной информации про то, как начать ремонт самостоятельно или с привлечением специалистов на некоторых этапах работ.\n\n<b>Стоимость 990₽ - доступ НАВСЕГДА</b>\n\nПриобрести чек-лист👇🏻\n\n<i>Проверка оплаты проходит в течение 5-10 минут. <b>После успешной оплаты придёт сообщение с ссылками на чек-лист.\n\nПосле оплаты возврат средств не осуществляется!</b></i>', parse_mode='html',reply_markup=keyboard)

keep_alive()
bot.polling(non_stop=True, interval=0)
