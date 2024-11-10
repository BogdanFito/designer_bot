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
API_TOKEN = '7832082508:AAH0oww7qfosltq1bjouXJCNucrHfiCIF70'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
data = '../data.csv'


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
        await message.answer(
            "👋Приветствую! Меня зовут Тётя Блеск, и я — помощница Валерии Жилич в этом практикуме. Представь меня как свекровь, которая следит за тем, как ты ведешь хозяйство. У меня глаз-алмаз, я вижу все мелочи! 😏")

    else:
        await message.answer("Чёт я тя не вижу в базе! Обратись к Валерии для уточнения информации!!")
    await Form.name.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)