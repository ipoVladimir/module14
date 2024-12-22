# Домашнее задание по теме "Доработка бота"
# Если вы решали старую версию задачи, проверка будет производиться по ней.
# Ссылка на старую версию тут.
# Цель: подготовить Telegram-бота для взаимодействия с базой данных.
#
# Задача "Витамины для всех!":
# Подготовка:
# Подготовьте Telegram-бота из последнего домашнего задания 13 модуля сохранив код с ним в файл module_14_3.py.
# Если вы не решали новые задания из предыдущего модуля рекомендуется выполнить их.
#
# Дополните ранее написанный код для Telegram-бота:
# Создайте и дополните клавиатуры:
#
#     В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
#     Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4". У всех кнопок назначьте callback_data="product_buying"
#
# Создайте хэндлеры и функции к ним:
#
#     Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
#     Функция get_buying_list должна выводить надписи 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза. После каждой надписи выводите картинки к продуктам. В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
#     Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
#     Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"
#
#
# Пример результата выполнения программы:
# Обновлённое главное меню:
# Список товаров и меню покупки:
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

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

catalog_product = (
{'Название':'Product1', 'Описание': 'описание 1', 'Цена': 1 * 100, 'file': 'files/1.jpg', 'label':'Продукт 1'},
{'Название':'Product2', 'Описание': 'описание 2', 'Цена': 2 * 100, 'file': 'files/2.jpg', 'label':'Продукт 2'},
{'Название':'Product3', 'Описание': 'описание 3', 'Цена': 3 * 100, 'file': 'files/3.jpg', 'label':'Продукт 3'},
{'Название':'Product4', 'Описание': 'описание 4', 'Цена': 4 * 100, 'file': 'files/4.jpg', 'label':'Продукт 4'},
)

start_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация'),
        ],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard= True
)

kb_calories = InlineKeyboardMarkup()
bt1_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
bt2_calories = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_calories.add(bt1_calories, bt2_calories)

# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
kb_catalog_product = InlineKeyboardMarkup()
bt1_catalog = InlineKeyboardButton(text=catalog_product[0]['label'], callback_data='product_buying')
bt2_catalog = InlineKeyboardButton(text=catalog_product[1]['label'], callback_data='product_buying')
bt3_catalog = InlineKeyboardButton(text=catalog_product[2]['label'], callback_data='product_buying')
bt4_catalog = InlineKeyboardButton(text=catalog_product[3]['label'], callback_data='product_buying')
kb_catalog_product.row(bt1_catalog, bt2_catalog, bt3_catalog, bt4_catalog)


class UserState(StatesGroup):
    age = State()       # (возраст, рост, вес)
    growth = State()
    weight = State()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for prod in catalog_product:
        await message.answer(f"Название: {prod['Название']} | Описание: {prod['Описание']} | Цена: {prod['Цена']}")
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