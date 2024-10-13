import telebot
from telebot import types
from Strings import Strings
import yookassa


bot = telebot.TeleBot('6976460514:AAG89jfnmFMr1Afv_iytwW8NwvCzCL1cOwU')
strings = Strings()
allow = False  # make it True if payment is completed

def create_payment():
    yookassa.Configuration.account_id = 331223
    yookassa.Configuration.secret_key = 'live_f2-p06BIc-YtxL4AB8nBwaQ0nIN6joAL8NuslxbIAKU'
    payment = yookassa.Payment.create({
        "amount": {
            "value": 990,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/design_valeriyazh_bot"
        },
        "description": "Покупка чек-листа",
        "capture": True
    })
    url = payment.confirmation.confirmation_url
    return url, payment.id


def check(id):
    payment = yookassa.Payment.find_one(id)
    if payment.status == 'succeeded':
        return True
    else:
        return False

@bot.message_handler(commands=['start'])
def get_info(message):
    keyboard = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton('Подробнее', callback_data='switch')
    keyboard.add(switch_button)

    bot.send_message(message.from_user.id, strings.getGreeting(), reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    bot.send_message(message.from_user.id, strings.getMistake())


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    url, id = create_payment()
    if callback.data == 'switch':
        keyboard = types.InlineKeyboardMarkup()
        switch_button = types.InlineKeyboardButton('Купить чек-лист', callback_data='switch2')
        keyboard.add(switch_button)
        bot.send_message(callback.message.chat.id, strings.getMoreDetails(), parse_mode='html', reply_markup=keyboard)
    if callback.data == 'switch2':
        bot.send_message(callback.message.chat.id, strings.getLink() + ' ' + url)
        while not check(id):
            continue
        if check(id):
            print('Оплата прошла!')
            bot.send_message(callback.message.chat.id, strings.getEnding() + '\n\nЗабрать чек-лист: https://disk.yandex.ru/d/oTnvS1oxNtuxpQ\n\nЗабрать 🎁: https://disk.yandex.ru/d/aEj9GTEANTUhmQ')

bot.polling(non_stop=True, interval=0)
