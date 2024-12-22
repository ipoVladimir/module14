# Домашнее задание по теме "План написания админ панели"
# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.
#
# Задача "Продуктовая база":
# Подготовка:
# Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.
#
# Дополните ранее написанный код для Telegram-бота:
# Создайте файл crud_functions.py и напишите там следующие функции:
# initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
#
#     id - целое число, первичный ключ
#     title(название продукта) - текст (не пустой)
#     description(описание) - текст
#     price(цена) - целое число (не пустой)
#
# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
#
# Изменения в Telegram-бот:
#
#     В самом начале запускайте ранее написанную функцию get_all_products.
#     Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов функцию get_all_products. Полученные записи используйте в выводимой надписи: "Название: <title> | Описание: <description> | Цена: <price>"
#
# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
#
# Пример результата выполнения программы:
# Добавленные записи в таблицу Product и их отображение в Telegram-bot:
#
#
# Примечания:
#
#     Название продуктов и картинок к ним можете выбрать самостоятельно. (Минимум 4)

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
        [KeyboardButton(text='Купить')]
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
