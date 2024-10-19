import logging
import time

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import asyncio
import csv
import pandas as pd

# Инициализация бота и логирования
API_TOKEN = '6976460514:AAG89jfnmFMr1Afv_iytwW8NwvCzCL1cOwU'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
data = 'data.csv'


# Состояния
class Form(StatesGroup):
    name = State()
    email = State()
    phone = State()
    feedback = State()
    other_question = State()

def check_user_in_csv(user_id):
    with open(data, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if str(row[0]) == str(user_id):
                return row  # Возвращаем всю строку данных, если пользователь найден
    return None  # Если пользователя нет

def update_data(user_id, title, value):
    df = pd.read_csv('data.csv').set_index('id')
    df.loc[user_id, title] = value
    df.to_csv('data.csv')

# Стартовое сообщение
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    found = check_user_in_csv(user_id)
    if found is None or found[1] == '':
        with open(data, mode='a', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, None, None, None, "name", None, None, None, None])
        await message.answer(
            "🐾Мяу! Привет, я Бисквитик, твой добрый и ласковый помощник. Давай подружимся! Как тебя зовут? 😻")
    await Form.name.set()

# Сбор имени
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_id = message.from_user.id
    found = check_user_in_csv(user_id)
    if found[1] == '':
        update_data(user_id,'name',message.text)
    update_data(user_id, 'state', 'email')
    await message.answer(
            f"🐾Мурр, приятно познакомиться, {message.text}! Оставь, пожалуйста, свой адрес электронной почты, чтобы мы всегда могли быть на связи! 💌")
    await Form.email.set()


# Сбор email
@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    user_id = message.from_user.id
    found = check_user_in_csv(user_id)
    if found[2] == '':
        update_data(user_id, 'email', message.text)
    update_data(user_id, 'state', 'phone')
    share_phone_button = KeyboardButton(text="📱 Поделиться номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(share_phone_button)
    await message.answer("🐾Мяу, ещё мне нужен твой номер телефона, чтобы оставаться на связи! 📱", reply_markup=keyboard)
    await Form.phone.set()


# Сбор номера телефона
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    import yookassa

    def create_payment():
        yookassa.Configuration.account_id = 331223
        yookassa.Configuration.secret_key = 'live_f2-p06BIc-YtxL4AB8nBwaQ0nIN6joAL8NuslxbIAKU'
        payment = yookassa.Payment.create({
            "amount": {
                "value": 1,
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

    user_id = message.from_user.id
    found = check_user_in_csv(user_id)
    if found[3] == '':
        update_data(user_id, 'phone', message.contact.phone_number)
    update_data(user_id, 'state', 'status')
    await state.update_data(phone=message.contact.phone_number)
    url, id = create_payment()
    await message.answer(
        "🐾Ох, ты знаешь, у хозяйки есть замечательный продукт, который точно тебе понравится! 🌟 Практикум 'Чистый дом' 🌟 — это твой ключ к уюту и порядку. Вот ссылка для оплаты: " + url,
        reply_markup=types.ReplyKeyboardRemove())
    update_data(user_id, 'state', 'cause')
    count = 0
    while not check(id):
        count +=1
        time.sleep(1)
        if count == 600: break
    if check(id):
        await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Отлично, оплата прошла. Переходи к тетушке Блеск!")
        update_data(user_id, 'status', 'OK')
    else:
        await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Что-то не понравилось? Выбери причину:")
        update_data(user_id, 'status', 'Failed')
        # Подсказки для ответов
        feedback_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        feedback_keyboard.add("💸 Цена высока", "⏳ Боюсь, что не хватит времени", "🤔 Не уверен, что поможет",
                              "💭 Другой вопрос")
        await message.answer("Выбери причину, и я мурлыкну в ответ! 😸", reply_markup=feedback_keyboard)
    await Form.feedback.set()



# Обработка причин отказа
@dp.message_handler(state=Form.feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    if message.text == "💸 Цена высока":
        await message.answer(
            "🐾Мур-мур, понимаю, 2000 рублей могут показаться значительной суммой, но это целый месяц доступа!")
    elif message.text == "⏳ Боюсь, что не хватит времени":
        await message.answer(
            "🐾Мур, боишься, что не успеешь? Практикум можно пройти за 3 дня, но доступ — целый месяц! 📅")
    elif message.text == "🤔 Не уверен, что поможет":
        await message.answer("🐾Мурр, ты будешь удивлён результатом! Расхламление и уборка сделают твой дом уютным! 🏡✨")
    elif message.text == "💭 Другой вопрос":
        await message.answer("🐾Мяу! Задай свой вопрос, и моя хозяйка Валерия скоро ответит!")
        await Form.other_question.set()


# Обработка других вопросов
@dp.message_handler(state=Form.other_question)
async def process_other_question(message: types.Message, state: FSMContext):
    await message.answer("🐾 Я передал твой вопрос хозяйке. Скоро она ответит!")
    await state.finish()


# Напоминание об оплате
async def remind_payment(user_id):
    await bot.send_message(user_id, "🐾 Мяу, это снова Бисквитик! Практикум 'Чистый дом' всё ещё ждёт тебя! 🏡💙")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)