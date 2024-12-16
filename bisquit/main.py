import logging
import time

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils import executor
import csv
import pandas as pd
import yookassa
import asyncio

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
            if row:
                if str(row[0]) == str(user_id):
                    return row  # Возвращаем всю строку данных, если пользователь найден
    return None  # Если пользователя нет

def update_data(user_id, title, value):
    df = pd.read_csv(data).set_index('id')
    df.loc[user_id, title] = value
    df.to_csv(data)

def delete_row(user_id):
    # Загружаем данные в DataFrame, используя 'user_id' как индекс
    df = pd.read_csv(data, index_col='id')

    # Проверяем наличие пользователя
    if user_id in df.index:
        # Удаляем строку по индексу
        df = df.drop(index=user_id)

        # Сохраняем изменения в файл
        df.to_csv(data)
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

        writer.writerow([user_id, None, None, None, None, None, None, None, None])
    await message.answer(
            "🐾Мяу! Привет, я Бисквитик, твой добрый и ласковый помощник. Давай подружимся! Как тебя зовут? 😻",reply_markup=ReplyKeyboardRemove())
    await Form.name.set()

# Сбор имени
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message):
    user_id = message.from_user.id
    update_data(user_id, 'name', message.text)
    await message.answer(
            f"🐾Мурр, приятно познакомиться, {message.text}, я ценю каждого своего друга и не хочу потерять связь с тобой! Оставь, пожалуйста, свой адрес электронной почты, чтобы мы всегда могли быть на связи! 💌 Обещаю, что никому, кроме неё, я его не передам — мурр, вся информация остаётся между нами! 😺")
    await Form.email.set()

# Сбор email
@dp.message_handler(state=Form.email)
async def process_email(message: types.Message):
    user_id = message.from_user.id
    update_data(user_id, 'email', message.text)
    share_phone_button = KeyboardButton(text="📱 Поделиться номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(share_phone_button)
    await message.answer("🐾Мяу, ещё мне нужно твой номер телефона. Это поможет оставаться рядом и не потеряться! 📱 Я обещаю не рассказывать твой номер никому и не кусать телефонные провода! 😸", reply_markup=keyboard)
    await Form.choice.set()

@dp.message_handler(content_types=[types.ContentType.CONTACT, types.ContentType.TEXT], state=Form.choice)
async def process_choice_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.contact:
        update_data(user_id, 'phone', message.contact.phone_number)
    else:
        update_data(user_id, 'phone', message.text)
    first_button = KeyboardButton(text="Практикум Чистый дом")
    second_button = KeyboardButton(text="Полезные материалы")
    third_button = KeyboardButton(text="Статьи")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(first_button, second_button, third_button)
    await message.answer("🐾 Мяу-мяу, спасибо за номер, друг! Теперь мы точно не потеряемся! 😸 А чем тебе интереснее заняться прямо сейчас?\n1️⃣ Хочешь узнать больше о практикуме 'Чистый дом'? Я с удовольствием поделюсь подробностями, как навести уют и порядок вокруг! 🏡✨\n2️⃣ Может, тебе интересно посмотреть полезные материалы? У моей хозяйки есть видео на YouTube, которые помогут сделать дом ещё уютнее, и тебе точно понравятся! 🎥💙\n3️⃣ А ещё у нас есть статьи, где мы делимся секретами уюта и организации пространства. Они обязательно вдохновят тебя на перемены! 📖🌟\nВыбирай, что ближе, и я сразу начну мурлыкать свои секреты! 😻", reply_markup=keyboard)
    await Form.current_task.set()

@dp.message_handler(state=Form.current_task)
async def process_current_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == "Практикум Чистый дом":
        update_data(user_id, 'interest', message.text)
        first_button = KeyboardButton(text="Да")
        second_button = KeyboardButton(text="Нет")
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(first_button, second_button)
        await message.answer(
            "🐾 Мурр, а ты знал, что у хозяйки есть продукт,, который точно тебе пригодится? 🌟 Практикум 'Чистый дом' 🌟 — это решение для тех, кто устал от беспорядка и хочет вернуть уют и комфорт. Представь, как здорово — избавиться от ненужных вещей, навести чистоту и создать такую систему хранения, что всё всегда на своих местах! Дом станет твоим местом силы и покоя. Муррр, бери скорее, не упусти свой шанс на уют! Муррр, заинтересовало? 💙",
            reply_markup=keyboard)

        await Form.phone.set()
    elif message.text == "Полезные материалы":
        await message.answer("🐾 Мурр! Ты выбрал видео — отличный выбор, друг! 😻 У Валерии есть замечательное видео о визуальном шуме и том, как он влияет на наш уют и спокойствие. 🌟\nПосмотри его на YouTube, вот ссылочка: [ссылка на видео].\nМур-мур, уверен, оно тебя вдохновит! 🏡✨ После просмотра расскажи, понравилось ли тебе, я всегда рад твоему мнению! 😸", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif message.text == "Статьи":
        await message.answer("🐾 Сейчас Валерия делится особенной подборкой подарков к Новому году! 🎄✨ В ней собрано более 100 идей на любой вкус и бюджет — от милых сувениров до стильных и практичных подарков. 🎁💡\nЗагляни сюда, чтобы найти вдохновение и порадовать своих близких:\nhttps://zhil-vall.yonote.ru/share/newyearsgifts\nМур-мур, уверен, ты найдёшь что-то особенное! Делись своими находками в социальных сетях и отмечай @zhilvall, нам всегда интересно, что ты выбрал. 😸", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await state.finish()

@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    def create_payment():
        yookassa.Configuration.account_id = 331223
        yookassa.Configuration.secret_key = 'live_f2-p06BIc-YtxL4AB8nBwaQ0nIN6joAL8NuslxbIAKU'
        payment = yookassa.Payment.create({
            "amount": {
                "value": 2300,
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
    url, id = create_payment()
    link_button = InlineKeyboardButton(text="📱 Ссылка на оплату", url=url)
    keyboard = InlineKeyboardMarkup().add(link_button)
    if message.text == "Да":
        await message.answer("🐾 Мурр, отлично, что тебя заинтересовало!",reply_markup=ReplyKeyboardRemove())
        await message.answer("🐾 Стоимость — всего 2300 рублей, а доступ к практикуму 'Чистый дом' будет ровно на 30 дней. Ты сможешь пройти его даже за неделю, но Валерия специально даёт целый месяц, чтобы ты мог подстроить программу под свой график. Уют и порядок ждут тебя, муррр, начинай прямо сейчас! 💙",
        reply_markup=keyboard)
        count = 0
        while not check(id):
            count +=1
            await asyncio.sleep(1)
            if count == 600 or check(id):
                break
        if check(id):
            await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Отлично, оплата прошла. Переходи к тетушке Блеск!")
            update_data(user_id, 'status', 'OK')
            await message.answer("🐾Мяу, вижу, что ты оплатил, здорово! Теперь я передам тебя тете Блеск, она у нас главная по выдаче материалов чистоты. Она может быть своевольной, но на самом деле очень милая, она всегда подкармливает меня вкусняшками и гладит за ушком. Надеюсь и ты с ней подружишься! 😸 Вот ссылка для общения с ней: @tetblesk_bot")
            await state.finish()
        else:
            await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Что-то не понравилось? Выбери причину:")
            update_data(user_id, 'status', 'Failed')
            # Подсказки для ответов
            feedback_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            feedback_keyboard.add("💸 Цена высока", "⏳ Нет времени", "🤔 Не поможет",
                                  "💭 Другой вопрос")
            await message.answer("Выбери причину, и я мурлыкну в ответ! 😸", reply_markup=feedback_keyboard)
            await Form.feedback.set()
    else:
        await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Что-то не понравилось? Выбери причину:")
        update_data(user_id, 'status', 'Failed')
        # Подсказки для ответов
        feedback_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        feedback_keyboard.add("💸 Цена высока", "⏳ Нет времени", "🤔 Не поможет",
                              "💭 Другой вопрос")
        await message.answer("Выбери причину, и я мурлыкну в ответ! 😸", reply_markup=feedback_keyboard)
        await Form.feedback.set()

# Обработка причин отказа
@dp.message_handler(state=Form.feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    feedback_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    feedback_keyboard.add("Нет, спасибо", "Я подумаю")
    if message.text == "💸 Цена высока":
        update_data(user_id, 'cause', 'price')
        await message.answer(
            "🐾Мур-мур, понимаю, 2100 рублей могут показаться значительной суммой. Но за эти деньги ты получаешь доступ к практикуму на целый месяц! 💙 Помимо основных уроков, там есть много дополнительных материалов, чек-листов и домашних заданий, которые помогут не потеряться в процессе. И между нами... там ещё есть кое-что особенное для тех, кто пройдет практикум, но об этом мне нельзя мяукать... 🐾 Представь, как изменится твой дом — уют и порядок того стоят! 🏡✨", reply_markup=feedback_keyboard)
        await Form.remind.set()
    elif message.text == "⏳ Нет времени":
        update_data(user_id, 'cause', 'time')
        await message.answer(
            "🐾Мур, боишься, что не успеешь? Не переживай! Ты можешь пройти практикум за 3 дня, но у тебя будет доступ целый месяц. 📅 Подстраивай уроки под свой ритм — у нас много чек-листов и заданий, которые помогут тебе двигаться уверенно и спокойно. И не волнуйся, если вдруг понадобится больше времени — у нас всё рассчитано на то, чтобы ты смог успеть даже с самым плотным графиком. Мурр, важен каждый шаг к уюту! 🕰️", reply_markup=feedback_keyboard)
        await Form.remind.set()
    elif message.text == "🤔 Не поможет":
        update_data(user_id, 'cause', 'help')
        await message.answer("🐾Мурр, сомневаешься, поможет ли? Поверь, ты будешь удивлён результатом! Наши простые шаги по расхламлению, уборке и организации пространства создадут настоящий уют в твоём доме. 💙 Чек-листы, домашние задания и дополнительные материалы поддержат тебя на каждом этапе. А ещё... есть кое-что особенное, что я не могу рассказать прямо сейчас, но ты узнаешь об этом в процессе. 🏡✨ Рискни — и увидишь, как твой дом наполняется теплом и энергией!", reply_markup=feedback_keyboard)
        await Form.remind.set()
    elif message.text == "💭 Другой вопрос":
        update_data(user_id, 'cause', 'other')
        await message.answer("🐾Мяу! У тебя возник другой вопрос? Не волнуйся, напиши его моей хозяйке, Валерии Жилич @valeriya_zhilich, и она ответит тебе в ближайшее время. 💬 Просто подожди немного, а пока я буду мурлыкать и ждать вместе с тобой. 😸", reply_markup=feedback_keyboard)
        await Form.remind.set()


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
    def check(id):
        payment = yookassa.Payment.find_one(id)
        if payment.status == 'succeeded':
            return True
        else:
            return False

    def create_payment():
        yookassa.Configuration.account_id = 331223
        yookassa.Configuration.secret_key = 'live_f2-p06BIc-YtxL4AB8nBwaQ0nIN6joAL8NuslxbIAKU'
        payment = yookassa.Payment.create({
            "amount": {
                "value": 2300,
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

    await asyncio.sleep(300)
    user_id = message.from_user.id
    url, id = create_payment()
    link_button = InlineKeyboardButton(text="📱 Ссылка на оплату", url=url)
    keyboard = InlineKeyboardMarkup().add(link_button)
    await bot.send_message(user_id, "🐾Мяу, это снова Бисквитик! 🕰 Прошло немного времени, и я хотел напомнить, что ты ещё можешь сделать важный шаг к уюту в своём доме. 🌟 Практикум 'Чистый дом' всё ещё ждёт тебя! 🏡💙\nПрисоединяйся прямо сейчас, и твой дом станет настоящим местом силы! После оплаты ты сможешь изучать материалы сразу, а доступ будет на 30 дней. Ты можешь пройти практикум даже за неделю, но у тебя будет достаточно времени, чтобы подстроить его под свой график. Стоимость всего лишь 2300 рублей. Не упускай свой шанс начать путь к уюту прямо сегодня! Вот ссылка для оплаты:", reply_markup=keyboard)
    count = 0
    while not check(id):
        count += 1
        await asyncio.sleep(1)
        if count == 600 or check(id):
            break
    if check(id):
        await bot.send_message(message.chat.id, "🐾 Мяу-мяу! Отлично, оплата прошла. Переходи к тетушке Блеск!")
        update_data(user_id, 'status', 'OK')
        await message.answer(
            "🐾Мяу, вижу, что ты оплатил, здорово! Теперь я передам тебя тете Блеск, она у нас главная по выдаче материалов чистоты. Она может быть своевольной, но на самом деле очень милая, она всегда подкармливает меня вкусняшками и гладит за ушком. Надеюсь и ты с ней подружишься! 😸 Вот ссылка для общения с ней: @tetblesk_bot")
        await state.finish()
    else:
        await bot.send_message(user_id,
                               "🐾Мяу, это снова Бисквитик! 🌟 Практикум 'Чистый дом' всё ещё ждёт тебя! 🏡💙\nЕсли передумаешь, нажимай на \start и заполняй анкету заново!",
                               reply_markup=keyboard)

        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)