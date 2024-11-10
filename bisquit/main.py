import logging
import time

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils import executor
import asyncio
import csv
import pandas as pd
import yookassa

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
    choice = State()
    current_task = State()
    offer = State()
    phone = State()
    feedback = State()
    other_question = State()
    remind = State()
    blesk = State()

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

def delete_row(user_id):
    # Загружаем данные в DataFrame, используя 'user_id' как индекс
    df = pd.read_csv('data.csv', index_col='id')

    # Проверяем наличие пользователя
    if user_id in df.index:
        # Удаляем строку по индексу
        df = df.drop(index=user_id)

        # Сохраняем изменения в файл
        df.to_csv('data.csv')
        print(f"Строка с user_id={user_id} успешно удалена.")
    else:
        print(f"Пользователь с user_id={user_id} не найден.")

# Стартовое сообщение
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    found = check_user_in_csv(user_id)
    if found is not None:
        delete_row(user_id)
    with open(data, mode='a', newline='\n', encoding='utf-8') as file:
        writer = csv.writer(file)
<<<<<<< HEAD
        writer.writerow([user_id, None, None, None, None, None, None, None, None])
=======
        writer.writerow([user_id, None, None, None, None, None, None, None])
>>>>>>> c9dad5b12775cf3bfd93c72b3a9a80324418019a
    await message.answer(
            "🐾Мяу! Привет, я Бисквитик, твой добрый и ласковый помощник. Давай подружимся! Как тебя зовут? 😻")
    await Form.name.set()

# Сбор имени
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_id = message.from_user.id
    update_data(user_id, 'name', message.text)
    await message.answer(
            f"🐾Мурр, приятно познакомиться, {message.text}! Оставь, пожалуйста, свой адрес электронной почты, чтобы мы всегда могли быть на связи! 💌")
    await Form.email.set()


# Сбор email
@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    user_id = message.from_user.id
    update_data(user_id, 'email', message.text)
    share_phone_button = KeyboardButton(text="📱 Поделиться номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(share_phone_button)
    await message.answer("🐾Мяу, ещё мне нужен твой номер телефона, чтобы оставаться на связи! 📱", reply_markup=keyboard)
    await Form.choice.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.choice)
async def process_choice_contact(message: types.Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        user_id = message.from_user.id
        update_data(user_id, 'phone', message.contact.phone_number)
        first_button = KeyboardButton(text="Практикум Чистый дом")
        second_button = KeyboardButton(text="Полезные материалы")
        third_button = KeyboardButton(text="Статьи")
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(first_button, second_button, third_button)
        await message.answer("🐾 Мяу-мяу, спасибо за номер, друг! Теперь мы точно не потеряемся! 😸 А чем тебе интереснее заняться прямо сейчас?", reply_markup=keyboard)
        await Form.current_task.set()

@dp.message_handler(state=Form.current_task)
async def process_current_task(message: types.Message, state: FSMContext):
    await state.update_data(current_task=message.text)

    if message.text == "Практикум Чистый дом":

        await state.update_data(offer=message.text)
        user_id = message.from_user.id
        update_data(user_id, 'interest', message.text)
        first_button = KeyboardButton(text="Да")
        second_button = KeyboardButton(text="Нет")
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(first_button, second_button)
        await message.answer(
            "🐾 Мурр, а ты знал, что у хозяйки есть продукт,, который точно тебе пригодится? 🌟 Практикум 'Чистый дом' 🌟 — это решение для тех, кто устал от беспорядка и хочет вернуть уют и комфорт. Представь, как здорово — избавиться от ненужных вещей, навести чистоту и создать такую систему хранения, что всё всегда на своих местах! Дом станет твоим местом силы и покоя. Муррр, бери скорее, не упусти свой шанс на уют! Муррр, заинтересовало? 💙",
            reply_markup=keyboard)

        await Form.phone.set()
    elif message.text == "Полезные материалы":
        pass
    else:
        pass



# Сбор номера телефона
@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
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

<<<<<<< HEAD
    user_id = message.from_user.id
    url, id = create_payment()
    link_button = InlineKeyboardButton(text="📱 Ссылка на оплату", url=url)
    keyboard = InlineKeyboardMarkup().add(link_button)
    if message.text == "Да":
        await message.answer("🐾 Мурр, отлично, что тебя заинтересовало!",reply_markup=ReplyKeyboardRemove())
        await message.answer("🐾 Стоимость — всего 2100 рублей, а доступ к практикуму 'Чистый дом' будет ровно на 30 дней. Ты сможешь пройти его даже за неделю, но валерия специально даёт целый месяц, чтобы ты мог подстроить программу под свой график. Уют и порядок ждут тебя, муррр, начинай прямо сейчас! 💙",
        reply_markup=keyboard)
        count = 0
        while not check(id):
            count +=1
            time.sleep(1)
            if count == 600 or check(id):
                break
        if check(id):
            await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Отлично, оплата прошла. Переходи к тетушке Блеск!")
            update_data(user_id, 'status', 'OK')
            await Form.blesk.set()
        else:
            await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Что-то не понравилось? Выбери причину:")
            update_data(user_id, 'status', 'Failed')
            # Подсказки для ответов
            feedback_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            feedback_keyboard.add("💸 Цена высока", "⏳ Боюсь, что не хватит времени", "🤔 Не уверен, что поможет",
                                  "💭 Другой вопрос")
            await message.answer("Выбери причину, и я мурлыкну в ответ! 😸", reply_markup=feedback_keyboard)
            await Form.feedback.set()
=======
    await state.update_data(phone=message.contact.phone_number)
    user_id = message.from_user.id
    update_data(user_id, 'phone', message.contact.phone_number)
    url, id = create_payment()
    link_button = KeyboardButton(text="📱 Ссылка на оплату", url=url)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(link_button)
    await message.answer(
        "🐾Ох, ты знаешь, у хозяйки есть замечательный продукт, который точно тебе понравится! 🌟 Практикум 'Чистый дом' 🌟 — это твой ключ к уюту и порядку.",
        reply_markup=keyboard)
    count = 0
    while not check(id):
        count +=1
        time.sleep(1)
        if count == 600 or check(id):
            break
    if check(id):
        await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Отлично, оплата прошла. Переходи к тетушке Блеск!")
        update_data(user_id, 'status', 'OK')
        await Form.blesk.set()
>>>>>>> c9dad5b12775cf3bfd93c72b3a9a80324418019a
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
    user_id = message.from_user.id
    if message.text == "💸 Цена высока":
        update_data(user_id, 'cause', 'price')
        await message.answer(
            "🐾Мур-мур, понимаю, 2000 рублей могут показаться значительной суммой, но это целый месяц доступа!")
        await Form.remind.set()
    elif message.text == "⏳ Боюсь, что не хватит времени":
        update_data(user_id, 'cause', 'time')
        await message.answer(
            "🐾Мур, боишься, что не успеешь? Практикум можно пройти за 3 дня, но доступ — целый месяц! 📅")
        await Form.remind.set()
    elif message.text == "🤔 Не уверен, что поможет":
        update_data(user_id, 'cause', 'help')
        await message.answer("🐾Мурр, ты будешь удивлён результатом! Расхламление и уборка сделают твой дом уютным! 🏡✨")
        await Form.remind.set()
    elif message.text == "💭 Другой вопрос":
        update_data(user_id, 'cause', 'other')
        await message.answer("🐾Мяу! Задай свой вопрос, и моя хозяйка Валерия скоро ответит!")
        await Form.other_question.set()


# Обработка других вопросов
@dp.message_handler(state=Form.other_question)
async def process_other_question(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    update_data(user_id, 'question', message.text)
    await message.answer("🐾 Я передал твой вопрос хозяйке. Скоро она ответит!")
    await Form.remind.set()


# Напоминание об оплате
@dp.message_handler(state=Form.remind)
async def remind_payment(message: types.Message, state: FSMContext):
<<<<<<< HEAD
    user_id = message.from_user.id
=======
>>>>>>> c9dad5b12775cf3bfd93c72b3a9a80324418019a
    await bot.send_message(user_id, "🐾 Мяу, это снова Бисквитик! Практикум 'Чистый дом' всё ещё ждёт тебя! 🏡💙\n Если передумаешь, жми на /start и заполняй анкету заново!")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)