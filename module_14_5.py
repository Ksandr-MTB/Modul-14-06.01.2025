from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

from crud_functions import initiate_db
from crud_functions import get_all_products
from crud_functions import add_user
from crud_functions import is_included
import sqlite3

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kd = ReplyKeyboardMarkup()
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kd.add(button1)
kd.add(button2)
kd.add(button3)
kd.add(button4)

kd_i = InlineKeyboardMarkup()
button1_I = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2_I = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kd_i.add(button1_I)
kd_i.add(button2_I)
kd_i_2 = InlineKeyboardMarkup()
button3_I = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button4_I = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button5_I = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button6_I = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kd_i_2.add(button3_I)
kd_i_2.add(button4_I)
kd_i_2.add(button5_I)
kd_i_2.add(button6_I)
resize_keyboard=True

initiate_db()

@dp.message_handler(commands=['start'])
async def _2start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kd)


@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup = kd_i)


class UserState(StatesGroup):

    age =State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text = ['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(thrist=message.text)
    date = await state.get_data()
    await message.answer(f'Ваша суточная норма калорий'
                         f' {10 * float(date["thrist"]) + 6.25 * float(date["second"]) - 5 * float(date["first"]) + 5}')
    await state.finish()


@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Расчет калорий происходит по формуле Миффлина-Сан Жеора: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;')
    await call.answer()

@dp.message_handler(text = 'Информация')
async def info(message):
    await message.answer('Я умею расчитывать среднесуточное количество калорий')



# Доработка бота согласно заданию 14_4 идет ниже этой строчки

@dp.message_handler(text = "Купить")
async def get_buying_list(message):
    connection = sqlite3.connect('list_price.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products_1 = cursor.fetchall()
    for product in products_1:
        await message.answer(f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}\n")
        with open(f'variant_{product[0]}.PNG', 'rb') as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kd_i_2)

@dp.callback_query_handler(text = ['product_buying'])
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# Доработка бота согласно заданию 14_5 идет ниже этой строчки (Регистрация пользователя в базе данных)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text ='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(first=message.text)
    date = await state.get_data()
    user_exists = is_included((date['first']))
    if user_exists:
        await state.update_data(username=(date['first']))
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя:")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(thrist=message.text)
    date = await state.get_data()
    add_user((date['first']), (date['second']), (date['thrist']))
    await message.answer('Регистрация прошла успешно!')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)