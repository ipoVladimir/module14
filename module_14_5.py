# Домашнее задание по теме "Написание примитивной ORM"
# Если вы решали старую версию задачи, проверка будет производиться по ней.
# Ссылка на старую версию тут.
# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.
#
# Задача "Регистрация покупателей":
# Подготовка:
# Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.
#
# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
# initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
#
#     id - целое число, первичный ключ
#     username - текст (не пустой)
#     email - текст (не пустой)
#     age - целое число (не пустой)
#     balance - целое число (не пустой)
#
# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст. Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
# is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.
#
# Изменения в Telegram-бот:
#
#     Кнопки главного меню дополните кнопкой "Регистрация".
#     Напишите новый класс состояний RegistrationState с следующими объектами класса State: username, email, age, balance(по умолчанию 1000).
#     Создайте цепочку изменений состояний RegistrationState.
#
# Фукнции цепочки состояний RegistrationState:
# sing_up(message):
#
#     Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
#     Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
#     После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
#
# set_username(message, state):
#
#     Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
#     Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
#     Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.
#
# set_email(message, state):
#
#     Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
#     Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
#     Далее выводить сообщение "Введите свой возраст:":
#     После ожидать ввода возраста в атрибут RegistrationState.age.
#
# set_age(message, state):
#
#     Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
#     Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
#     Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
#     В конце завершать приём состояний при помощи метода finish().
#
# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
#
# Пример результата выполнения программы:
# Машина состояний и таблица Users в Telegram-bot:
# Результат в таблице Users:

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

CATALOG_PRODUCT = crud_functions.get_all_products()

start_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация'),
        ],
        [
            KeyboardButton(text='Регистрация'),
            KeyboardButton(text='Купить')
        ]
    ], resize_keyboard= True
)

kb_calories = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas'),
        ]
    ], resize_keyboard= True
)

# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
kb_catalog_product = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text=CATALOG_PRODUCT[0]['label'], callback_data='product_buying'),
            InlineKeyboardButton(text=CATALOG_PRODUCT[1]['label'], callback_data='product_buying'),
            InlineKeyboardButton(text=CATALOG_PRODUCT[2]['label'], callback_data='product_buying'),
            InlineKeyboardButton(text=CATALOG_PRODUCT[3]['label'], callback_data='product_buying')
        ]
    ], resize_keyboard= True
)

class RegistrationState(StatesGroup):
    # username, email, age, balance(по умолчанию 1000)
    username = State()
    email = State()
    age = State()
    balance = 1000
    #state = dp.get_current().current_state()
    #state.update_data(balance=1000)


@dp.message_handler(text=['Регистрация', 'регистрация'])
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not crud_functions.is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'], RegistrationState.balance)
    await message.answer("Регистрация прошла успешно!")
    await state.finish()


class UserState(StatesGroup):
    age = State()       # (возраст, рост, вес)
    growth = State()
    weight = State()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for prod in CATALOG_PRODUCT:
        await message.answer(f"Название: {prod['title']} | Описание: {prod['description']} | Цена: {prod['price']}")
        with open(prod['file'], 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_catalog_product)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_calories)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора:\n'
                              'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    #data = await state.get_data()
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    #data = await state.get_data()
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # Упрощенный вариант формулы Миффлина-Сан Жеора:
    # https://www.calc.ru/Formula-Mifflinasan-Zheora.html
    #     для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
    #     для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
    try:
        cal_men = 10 * int(data['weight']) + 6.25 * float(data['growth']) - 5 * int(data['age']) + 5
    except Exception as ex:
        await message.answer(f"Похоже вы допустили ошибку в данных: возраст={data['age']} лет, "
                             f"рост={data['growth']} см., вес={data['weight']} кг.")
    else:
        await message.answer(f"В сутки для вас необходимо {cal_men} (ккал) килокалорий.")

    await state.finish()

@dp.message_handler(commands=['start'])
async def start_message(message):
    #print("Привет! Я бот помогающий твоему здоровью.")
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=start_menu)

@dp.message_handler()
async def all_message(message):
    #print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
