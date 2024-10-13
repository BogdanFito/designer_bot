import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import asyncio
import csv

# Инициализация бота и логирования
API_TOKEN = '6976460514:AAG89jfnmFMr1Afv_iytwW8NwvCzCL1cOwU'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
data = '../data.csv'


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


# Стартовое сообщение
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    with open(data, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, None, None, None, "name", None, None, None, None])

    await message.answer(
        "🐾Мяу! Привет, я Бисквитик, твой добрый и ласковый помощник. Давай подружимся! Как тебя зовут? 😻")
    await Form.name.set()


# Сбор имени
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        f"🐾Мурр, приятно познакомиться, {message.text}! Оставь, пожалуйста, свой адрес электронной почты, чтобы мы всегда могли быть на связи! 💌")
    await Form.email.set()


# Сбор email
@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    share_phone_button = KeyboardButton(text="📱 Поделиться номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(share_phone_button)
    await message.answer("🐾Мяу, ещё мне нужен твой номер телефона, чтобы оставаться на связи! 📱", reply_markup=keyboard)
    await Form.phone.set()


# Сбор номера телефона
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        "🐾Ох, ты знаешь, у хозяйки есть замечательный продукт, который точно тебе понравится! 🌟 Практикум 'Чистый дом' 🌟 — это твой ключ к уюту и порядку. Вот ссылка для оплаты: [ссылка]",
        reply_markup=types.ReplyKeyboardRemove())
    # через 10 минут отправляем follow-up
    await state.set_state(None)

    # Отправка follow-up сообщения через 10 минут
    await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Что-то не понравилось? Выбери причину:")

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

async def on_startup(_):
    arr = []  # абстрактный массив с юзер_айди
    for user_id in arr:
        await bot.send_message(chat_id=user_id, text="Бот запущен!")
        await asyncio.sleep(1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
