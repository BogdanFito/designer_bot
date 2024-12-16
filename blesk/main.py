import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove, InputFile
from aiogram.utils import executor
import asyncio
import csv
import pandas as pd

# Инициализация бота и логирования
API_TOKEN = '7832082508:AAH0oww7qfosltq1bjouXJCNucrHfiCIF70'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
data = 'data.csv'
permission = False
permission2 = False
task = None
first_promo = False
second_promo = False


# Состояния
class Form(StatesGroup):
    promo = State()
    homework = State()
    promo_2 = State()
    quiet = State()
    homework_2 = State()
    homework_3 = State()
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
async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    found = check_user_in_csv(user_id)
    first_button = KeyboardButton(text="Пропустить")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(first_button)
    if found is not None:
        video_path = "blesk/res/приветствие .mp4"  # Замените на путь к вашему видеофайлу
        video = InputFile(video_path)
        await message.answer(
            "👋Приветствую! Меня зовут Тётя Блеск, и я — помощница Валерии Жилич в этом практикуме. Представь меня как свекровь, которая следит за тем, как ты ведешь хозяйство. У меня глаз-алмаз, я вижу все мелочи! 😏",reply_markup=ReplyKeyboardRemove())
        await bot.send_video(user_id, video)
        await asyncio.sleep(180) #180
        await bot.send_message(user_id,'А вот и ссылочка на чат участников. Подключайся, не стесняйся, будем вместе приводить дом в порядок! А ещё, в качестве приветственного подарочка — держи файл "Топ 7 опасных лайфхаков для уборки" (https://disk.yandex.ru/i/pzk7hTT0nfNBrg ). Запомни — уборка требует знаний, не верь всему, что видишь в интернете! 💡 Если возникнут какие-то проблемы, всегда пиши Валерии @valeriya_zhilich')
        await asyncio.sleep(600) #600
        await bot.send_message(user_id, 'Ну, вот и пришло время для первого урока!✨ Посмотри видео, где рассказывается о важности расхламления. Это первый шаг к уюту и порядку в доме.\nтайм-код:\n00:00 приветствие\n00:13 планирование\n07:13 методы расхламления\n12:23 экологический подход\n14:32 эмоциональная привязка\n16:23 поддержание порядка\n18:55 домашнее задание \nhttps://rutube.ru/video/private/1ac8b576d63aa4e5de6162648d423673/?p=afIvmjhRxBXjj1N7dV4THg\nДля вашего удобства есть также конспект урока ( https://zhil-vall.yonote.ru/share/clutter )')
        await asyncio.sleep(180)  # 180
        await bot.send_message(user_id, 'Не забудь ввести промокод для получения подарков!', reply_markup=keyboard)
        await Form.promo.set()
    else:
        await message.answer("К сожалению я не вижу тебя среди списка учеников, обратись к Валерии @valeriya_zhilich для уточнения информации")
        await state.finish()

@dp.message_handler(state=Form.promo)
async def promo(message: types.Message, state: FSMContext):
    global task, first_promo
    user_id = message.from_user.id
    if 'Авито' in message.text or 'авито' in message.text or 'АВИТО' in message.text:
        first_promo = True
        await message.answer("Ого, а ты, оказывается, наблюдательная! 👀 Ладно-ладно, держи свой гайд по продаже на Авито. 💼 Пользуйся с умом и продавай всё ненужное, как пирожки! (https://disk.yandex.ru/i/KGtTm6AiMWN8OA)", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(180)  # 180

    elif 'эко' in message.text or 'Эко' in message.text or 'ЭКО' in message.text:
        first_promo = True
        await message.answer("Ну, надо же, ты не упустила этот момент! 👀 Молодец, держи свой заслуженный гайд по сортировке мусора. ♻️ Узнаешь, как правильно организовать процесс и куда всё это потом деть. Похвально, хозяйка — экологичная и сознательная, это что-то новенькое! 😉 (https://disk.yandex.ru/i/PneskVrmFCewRg)", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(180)  # 180

    else:
        pass
    await asyncio.sleep(1800) #1800
    await bot.send_message(user_id, "Как успехи? Есть вопросы по уроку? Спрашивай, пока я в хорошем настроении, все передам Валерии! 😎 (https://forms.gle/9FyNVDpXjtvAeAcY9 )", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(60) #60
    await bot.send_message(user_id, "Ты же не забыла, что у нас есть чудесный бонус? 💡 Если ты отметишь автора Валерию Жилич в соцсетях “@zhilvall, ты получишь гайд о цифровом расхламлении, пришли скриншот с отметкой в личные смс Валерии, чтобы не потеряться @valeriya_zhilich")
    await asyncio.sleep(180) #180
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Метод KonMari", "Четыре коробки", "Один в один", "15 минут в день", "Метод минимализма", "Правило '20/20'", "Правило “Пяти вещей", "Правило 'один сезон'")
    await bot.send_message(user_id, "И вот тебе 🎁 чек-лист 'Расхламление' (https://disk.yandex.ru/i/PNKG5BmGWku_sA ), чтобы не потеряться в процессе. \nА теперь, важное задание! ⚡Нужно избавиться от 30 ненужных вещей — по 5-10 вещей из каждой комнаты, если комнат больше, вещей тоже может стать больше. Когда всё будет готово, присылай фото с мешками. \nНу, и давай выберем метод расхламления:", reply_markup=keyboard)
    await Form.homework.set()
    task = asyncio.create_task(remind(user_id))
    await task

async def remind(id):
    global permission
    user_id = id
    await asyncio.sleep(172800)
    permission = True
    await bot.send_message(user_id,
                                   "Ну-ну, я так и знала... Домашнее задание-то так и пылится невыполненным, да? 😏 Всё-таки права была — толку от такой хозяйки, как от чайника без воды. Ну, ничего, может, и за уборку когда-нибудь возьмёшься. Хотя сомневаюсь...🧹")
    await asyncio.sleep(259200)
    permission = True
    await bot.send_message(user_id,
                                   "А я-то надеялась, что ты справишься, но, кажется, ошиблась. 😌 С такой-то скоростью можно годами ждать чистоты в доме. Ты ведь не думала, что дом сам по себе уберётся, правда? Ну, я на всякий случай напомню... ⏳")
    await asyncio.sleep(345600)
    permission = True
    await bot.send_message(user_id,
                                   "Как я и думала, опять бардак кругом! Я ведь знала, что ждать чего-то стоящего от такой невестки не приходится. 😒 Ну ничего, хоть напомню — домашнее задание ещё ждёт тебя... если, конечно, решишься.")
    await asyncio.sleep(432000)
    permission = True
    await bot.send_message(user_id,
                                   "Ох-ох-ох... Я ведь сразу поняла, что уборка — не для тебя. 😏 Ну, ничего, мне не привыкать напоминать. Когда соберёшься с духом, вспомни, что задание всё ещё ждёт... вместе с пылью и хаосом.")
    await asyncio.sleep(518400)
    permission = True
    await bot.send_message(user_id,
                                   "Ох, ну что ж... Как я и предполагала, уборка не твой конёк. 🧼 А ведь я так надеялась, что ты хоть чуть-чуть постараешься! Видимо, беспорядок — это твоё естественное состояние, что поделать...")


async def remind2(id):
    global permission, permission2
    user_id = id
    await asyncio.sleep(172800)
    permission2 = True
    if not permission:
        await bot.send_message(user_id,
                                       "Ну что же, дорогая, я так и знала, что сразу ты не справишься... 🙄 Но у тебя есть шанс доказать, что хоть чему-то ты научилась. Жду фото, духовка ведь сама себя не отмоет!")
    else:
        await bot.send_message(user_id,
                                       "Ну что, моя дорогая невестка? 🤔 Как-то я подозреваю, что снова забыла о своём домашнем задании. В прошлый раз ты тоже не спешила его делать. Неужели опять упустишь шанс на чистоту? Помни, духовка ждет!")
    await asyncio.sleep(259200)
    permission2 = True
    if not permission:
        await bot.send_message(user_id,
                                       "Честно говоря, я уже не удивляюсь, что снова ничего не сделано. 😏 Ты, конечно, стала чуть прилежнее, но до настоящей хозяйки тебе ещё далеко. Может, в этот раз получится хотя бы с духовкой?")
    else:
        await bot.send_message(user_id,
                                       "Ох, кажется, у меня звоночек в голове — в прошлый раз ты тоже задерживалась с домашним заданием. 😏 Неужели история повторяется? Надеюсь, что ты не собираешься затягивать с уборкой снова?")
    await asyncio.sleep(345600)
    permission2 = True
    if not permission:
        await bot.send_message(user_id,
                                       "Эх, опять тишина... Неужели даже после всех наших уроков тебе так сложно начать уборку? Ты стала лучше, но до идеала всё ещё далеко. Ну давай, не откладывай вечно!")
    else:
        await bot.send_message(user_id,
                                       "Эх, дорогуша, ты ведь не забыла о нашем договоре, да? 🤭 В прошлый раз ты тоже медлила с домашним заданием. Чего ждёшь на этот раз? Уверена, твоя духовка очень скучает по вниманию!")
    await asyncio.sleep(432000)
    permission2 = True

    if not permission:
        await bot.send_message(user_id,
                                       "Ты мне в прошлый раз показала, что можешь хоть что-то сделать, но вот опять затишье. Неужели духовка такая непосильная задача? Ты ведь уже почти стала хозяйкой, а всё ещё медлишь.")
    else:
        await bot.send_message(user_id,
                                       "Здравствуй, мой милый 'долгожитель'! 🙄 Ну что, опять забыла о домашнем задании? Как в прошлый раз, так и сейчас, оказывается, ты не спешишь! Духовка всё так же грязная, да? Давай, пора уже делать!")
    await asyncio.sleep(518400)
    permission2 = True
    if not permission:
        await bot.send_message(user_id,
                                       "Я знала, что будет задержка. В тебе живёт настоящая ленивица, которая никак не сдаётся. Хотя чуть-чуть лучше ты стала, признай. Но давай уже с духовкой разберёмся!")
    else:
        await bot.send_message(user_id,
                                       "Эй, ты там как? 🕵️‍♀️ Напоминаю, что прошлый раз ты также не спешила с домашним заданием. Хочешь, чтобы твоя духовка оставалась в таком же состоянии? Давай, не медли, я на тебя надеюсь!")


async def remind3(id):
    global permission, permission2
    user_id = id
    await asyncio.sleep(172800)
    if not permission and not permission2:
        await bot.send_message(user_id,
                                   "Ну что, решила меня удивить молчанием? 😏 А ведь раньше ты была такой ответственной. Надеюсь, просто дела задержали тебя. Жду твоё домашнее задание, не разочаровывай меня!")
    else:
        await bot.send_message(user_id,
                                   "Ну вот, снова тишина… 🤔 В прошлый раз ты задержала задание, но я простила. А сейчас ведь финал! Неужели ты снова меня огорчишь? Я уже начала привыкать к твоим успехам, не разочаровывай меня в последний момент!")
    await asyncio.sleep(259200)
    if not permission and not permission2:
        await bot.send_message(user_id,
                                   "Эй, ты обычно не заставляешь долго ждать! Всё хорошо? Я верю, что ты справишься, как и с предыдущими заданиями. Но мне пора увидеть твои результаты. 😉")
    else:
        await bot.send_message(user_id,
                                   "Опять задержка? Ты и в прошлый раз тянула до последнего... Но это же последнее задание, дорогая! Я уже почти привязалась к тебе, не заставляй сомневаться в твоей ответственности. Жду фото, я верю в тебя!")
    await asyncio.sleep(345600)
    if not permission and not permission2:
        await bot.send_message(user_id,
                                   "Неужели решила сбавить обороты? 🤔 А ведь до этого ты была просто на высоте! Не подведи меня, я знаю, что ты способна на большее!")
    else:
        await bot.send_message(user_id,
                                   "Ты в прошлый раз чуть не заставила меня нервничать, и вот опять тишина. А ведь это последнее задание, давай не будем всё портить на финише. Я начала доверять тебе, не подведи!")
    await asyncio.sleep(432000)
    if not permission and not permission2:
        await bot.send_message(user_id,
                                   "Что-то тишина... Я уж привыкла получать от тебя отличные результаты. Неужели ты остановилась на полпути? Не разочаровывай меня, жду фото!")
    else:
        await bot.send_message(user_id,
                                   "Ну что же ты снова молчишь? 😔 В прошлый раз я уже переживала, и сейчас не хочу разочаровываться. Это финал! Я привыкла ждать твоих стараний, не давай мне повода усомниться в тебе.")
    await asyncio.sleep(518400)
    if not permission and not permission2:
        await bot.send_message(user_id,
                                   "Ты ведь всегда справлялась так быстро! Где же твои фото? 🙃 Я жду твоего очередного успеха, не подведи меня!")
    else:
        await bot.send_message(user_id,
                                   "Кажется, ты снова откладываешь… А ведь это последнее задание, и в прошлый раз ты заставила меня ждать дольше, чем нужно. Я начала к тебе привыкать, так что давай, не подведи меня на финише! Я верю, ты справишься.")


@dp.message_handler(content_types=[types.ContentType.PHOTO], state=Form.homework)
async def homework(message: types.Message, state: FSMContext):
    global task
    user_id = message.from_user.id
    first_button = KeyboardButton(text="Пропустить")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(first_button)
    if message.photo:
        try:
            task.cancel(msg='cancel task')
        except asyncio.CancelledError as e:
            print("CancelledError raised:", e)
        task = None
        await message.answer("🌟Ну, можно было и быстрее! Но что сделано, то сделано. Переходим ко второму уроку!", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(20) #20
        await bot.send_message(user_id, "Посмотри видео про уборку. Это ключ к уюту и гармонии в доме. \nhttps://rutube.ru/video/private/26ec79e61bd28a25c15d2ee05822b622/?p=EB8H4G8SYn0Ml1nuXxQucA\nтайм-код:\n00:00 приветствие\n00:17 психологический аспект\n01:25 планирование и организация\n02:09 распределение задач\n02:50 этапы уборки\n03:21 инструменты и средства\n05:19 чистящие средства\n09:21 регулярность\n10:20 экономия времени\n11:12 забота о мебели и поверхностях\n17:12 меры предосторожности \n17:38 экологическая уборка\n18:18 мотивация\n19:24 домашнее задание \nКонспект тоже прилагается (https://zhil-vall.yonote.ru/share/cleaning )")
        await asyncio.sleep(1)
        await bot.send_message(user_id, 'Не забудь ввести промокод для получения подарков!' ,reply_markup=keyboard)
        await Form.promo_2.set()
    else:
        await Form.homework.set()

@dp.message_handler(state=Form.promo_2)
async def promo_2(message: types.Message, state: FSMContext):
    global task, second_promo
    user_id = message.from_user.id
    if 'хаос' in message.text or 'Хаос' in message.text or 'ХАОС' in message.text:
        second_promo = True
        await message.answer(
            "Хмм, ты всё-таки внимательна! 😏 Кодовое слово найдено, а это значит, что держи гайд по уборке в условиях полного хаоса с детьми и животными. 🐾👶 Узнаешь, как навести порядок там, где его, кажется, невозможно поддерживать. Справишься ли ты? Ну, посмотрим! 😉 (https://disk.yandex.ru/i/D7OqtB5LyILp0g )", reply_markup=ReplyKeyboardRemove())
    else:
        pass
    await asyncio.sleep(1800) #1800
    await bot.send_message(user_id, "Как всегда, есть вопросы?📋 Спрашивай, не стесняйся! ( https://forms.gle/TWGfvvezADkkvh7y9 )", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(180) #180
    await bot.send_message(user_id, "Дарю тебе 🎁 подборку средств и оборудования для уборки (https://zhil-vall.yonote.ru/share/tools ). А вот и чек-лист для уборки (https://disk.yandex.ru/i/nXh1z42RIfHkdQ ). Не забывай, дисциплина — путь к успеху! 💪")
    await asyncio.sleep(120) #120
    await bot.send_message(user_id, "Ой, чуть не забыла! 😅 Теперь твоё задание — отмыть духовку или другой предмет, который ты редко чистишь. Жду два фото: до и после. И, конечно, не забуду напоминать тебе, пока не увижу результат! 🕵️‍♀️")
    await Form.homework_2.set()
    task = asyncio.create_task(remind2(user_id))
    await task

@dp.message_handler(state=Form.homework_2, content_types=types.ContentType.PHOTO)
async def homework_2(message: types.Message, state: FSMContext):
    global task
    user_id = message.from_user.id
    if message.photo:
        try:
            task.cancel(msg='cancel task')
        except asyncio.CancelledError as e:
            print("CancelledError raised:", e)
        task = None
        await message.answer("Наконец-то я вижу прогресс! 👀 Молодец, действительно справилась. Старалась, а ведь я думала, что ты не осилишь! Теперь уже чуть больше уважаю тебя как хозяйку. 😌")
        await asyncio.sleep(20) #20
        await bot.send_message(user_id, "Теперь время для организации пространства. Посмотри видео, где ты узнаешь, как убрать визуальный шум. \nhttps://rutube.ru/video/private/c1478c0b7cdd62d934a8dc56469e54fe/?p=FgO-zgTt-nOCwGvWqNAmbw\nтайм-код:\n00:00 вступление\n00:27 определение функциональных зон\n00:50 сортировка\n01:32 системы хранения\n02:47 вертикальное пространство\n05:14 хранение внизу\n06:23 хранение вещей\n08:48 организация кухни\n12:26 ваннаяn\n14:33 рабочий стол\n18:06 детские вещиn\n21:01 поддержка порядкаn\n25:54 визуальный шумn\n26:13 домашнее задание\nКонспект тут ( https://zhil-vall.yonote.ru/share/organization )")

        await asyncio.sleep(1800) #1800
        await bot.send_message(user_id, "Вопросы по уроку? Спрашивай! ( https://forms.gle/kDuRu2DcDYUhd2J99 )")
        await asyncio.sleep(180) #180
        await bot.send_message(user_id, "А вот тебе 🎁чек-лист по организации (https://disk.yandex.ru/i/Z6eTVJZ3rCLzUQ )  и гайд: 7 лайфхаков для наведения порядка (https://disk.yandex.ru/i/eLohQGncEL7Tww ).")
        await asyncio.sleep(180) #180
        await bot.send_message(user_id, "И ещё подарочек — подборка органайзеров и коробочек. Запомни: квадратные формы для хранения круп — лучший выбор, ведь они экономят место! 📦 (https://zhil-vall.yonote.ru/share/organizers )")
        await asyncio.sleep(180) #180
        await bot.send_message(user_id, "Ну что, настало время поговорить о визуальном шуме. 🎬 Посмотри видео Валерии📽️ (далее ссылка на YouTube, будет чуть позже), смотри внимательно и запоминай, что мешает твоему дому дышать свободно. 💨 Визуальный шум — это скрытый враг уюта, так что избавляемся от него как можно скорее! 💡")
        # await bot.send_video(user_id, video2)
        await asyncio.sleep(180) #180
        await bot.send_message(user_id, "📌 Пришло время взяться за дело! Выбирай одну часто используемую зону и наводит там порядок! ⚖️ Никакого визуального шума и разбросанных вещей. Всё должно быть организованно и аккуратно. 📸 Жду два фото: до и после, чтобы оценить твои старания. Ну-ка, покажи, как ты умеешь! 😉")
        await Form.homework_3.set()
        task = asyncio.create_task(remind3(user_id))
        await task
    else:
        await Form.homework_2.set()

@dp.message_handler(state=Form.homework_3, content_types=types.ContentType.PHOTO)
async def homework_3(message: types.Message, state: FSMContext):
    global task, first_promo, second_promo
    video_path_2 = "blesk/res/презентация декора (1).mp4"  # Замените на путь к вашему видеофайлу 2
    video_path = "blesk/res/поздравление (1).mp4"  # Замените на путь к вашему видеофайлу 2
    photo_path = "blesk/res/сертификат.jpg"
    sert = InputFile(photo_path)
    video = InputFile(video_path)
    video2 = InputFile(video_path_2)
    user_id = message.from_user.id
    if message.photo:
        try:
            task.cancel(msg='cancel task')
        except asyncio.CancelledError as e:
            print("CancelledError raised:", e)
        task = None
        await message.answer("Ты меня поразила, дорогая! 💐 Всё так аккуратно и организованно, как будто это сделал профессионал. Я так рада за тебя, как за свою любимую невестушку! Такие фото можно не стыдиться и повесить на стенку!")
        await asyncio.sleep(60) #60
        if not first_promo:
            await message.answer(
                "👀 Ладно-ладно, держи свой гайд по продаже на Авито. 💼 Пользуйся с умом и продавай всё ненужное, как пирожки! (https://disk.yandex.ru/i/KGtTm6AiMWN8OA)")
            await asyncio.sleep(180)  # 180
            await message.answer(
                "👀 Молодец, держи свой заслуженный гайд по сортировке мусора. ♻️ Узнаешь, как правильно организовать процесс и куда всё это потом деть. Похвально, хозяйка — экологичная и сознательная, это что-то новенькое! 😉 (https://disk.yandex.ru/i/PneskVrmFCewRg)")

        await asyncio.sleep(1)
        if not second_promo:
            await message.answer(
                "Держи гайд по уборке в условиях полного хаоса с детьми и животными. 🐾👶 Узнаешь, как навести порядок там, где его, кажется, невозможно поддерживать. Справишься ли ты? Ну, посмотрим! 😉 (https://disk.yandex.ru/i/D7OqtB5LyILp0g )")

        await asyncio.sleep(1)
        await bot.send_message(user_id, "Дарю тебе гайд о энергетическом очищении дома (https://disk.yandex.ru/i/I_qvFK4nZ0Q_Xw ). И знаешь что? Если отметишь автора Валерию Жилич @zhilvall в соцсетях, получишь женскую практику 'Я дома' в подарок! 💙, пришли скриншот с отметкой в личные смс Валерии, чтобы не потеряться @valeriya_zhilich")
        await bot.send_message(user_id, "Не забудь заполнить анкету для участия в конкурсе на самый активный участник. Победитель получит подарок от Валерии! 🎁 (https://forms.yandex.ru/u/6707c380d04688f31d0bf87f/ )")
        await asyncio.sleep(300) #300
        await bot.send_photo(user_id, sert)
        await bot.send_message(user_id, "Моя дорогая невестка! 🎉\nПоздравляю тебя с успешным завершением нашего практикума! 🌟 Я так горжусь тобой и твоими достижениями! Ты прошла этот путь с настоящей решимостью и упорством, и теперь я вижу, как ты стала прекрасной хозяйкой. Каждый шаг, который ты сделала, каждое домашнее задание, которое выполнила, помогли тебе не только преобразить свой дом, но и улучшить себя.\nТеперь твой дом — это не просто место, где ты живешь, а настоящий уголок уюта и гармонии, где царит порядок и красота. 🏡💙 Я знаю, что это было не всегда легко, но ты справилась! Ты показала, что можешь организовать пространство, освободить его от ненужного и создать атмосферу, в которой хочется находиться.\nТы — моя любимая ученица, и мне было очень приятно видеть, как ты меняешься и растешь. Я не только горжусь тем, что стала твоим наставником, но и искренне радуюсь твоим успехам. Теперь ты не просто хозяйка, а настоящая хранительница уюта! 🌺✨\nС любовью, твоя Тетя Блеск!")
        await asyncio.sleep(60) #60
        await bot.send_message(user_id, "Это поздравление от Валерии Жилич, которая тоже очень гордится твоими успехами! 💙 Ты действительно сделала невероятный путь, и каждый шаг приближал тебя к тому, чтобы стать отличной хозяйкой.\nТы вложила много сил и стараний, и это не осталось незамеченным. Продолжай в том же духе, и впереди тебя ждёт ещё больше успехов и достижений!")
        await bot.send_video(user_id, video)
        await asyncio.sleep(180) #180
        await bot.send_message(user_id, "🌼 Мне и Валерии очень важно узнать, как прошёл твой опыт в нашем практикуме. Пожалуйста, заполни анкету по ссылке и расскажи, что тебе особенно понравилось, а что можно было бы улучшить. Твои мысли помогут нам сделать программу ещё лучше! 💙 После заполнения анкеты ты получишь небольшой бонус от нас в знак благодарности. Жду с нетерпением твоих ответов!\n( https://forms.gle/DqBNKZMoFbZKWR4n7 )")
        await asyncio.sleep(900) #900
        await bot.send_message(user_id, "🌟Дорогая моя невестка! У меня для тебя потрясающая новость! 🎉 Валерия готовит новый практикум, где ты узнаешь, как сделать свой интерьер красивым и эстетичным, словно с картинок из Pinterest, и все это без ремонта и за небольшую сумму! 💙\nВ этом практикуме Валерия подробно расскажет о том, как выбрать правильные акценты, сочетать цвета и создавать уют, не тратя целое состояние. Я уверена, что тебе это будет интересно!")
        await bot.send_video(user_id, video2)
        await asyncio.sleep(60) #60
        await bot.send_message(user_id, "Дорогая моя, я хочу предложить тебе стать одной из первых, кто узнает о его старте! 🌟\nЗаполни анкету предзаписи, и ты получишь эксклюзивный промокод на скидку, чтобы начать свой путь к созданию идеального интерьера! ✨ Не упусти такую возможность — вместе мы сделаем твой дом по-настоящему красивым и уютным!  https://forms.yandex.ru/u/6707ca3ac417f356b666f41a/")
        await state.finish()
    else:
        await Form.homework_3.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)