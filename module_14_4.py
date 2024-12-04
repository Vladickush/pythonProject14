# Тема "План написания админ панели"
# Задача Задача "Продуктовая база"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
from crud_functions import initiate_db, get_all_products

api = "7487519575:AAEal-5CylTeImVLBt1zXEWDpfHEuNg1MG4"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
info = KeyboardButton(text='Информация')
calc = KeyboardButton(text='Рассчитать')
buy = KeyboardButton(text='Купить')
finish = KeyboardButton(text='Выход')
kb.add(info, calc, buy, finish)

ikb = InlineKeyboardMarkup(row_width=2)
calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb.add(calories, formulas)

fruit_menu = InlineKeyboardMarkup(row_width=4)
product1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
product2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
product3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
product4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
fruit_menu.add(product1, product2, product3, product4)

initiate_db()


# Запуск клавиатуры при старте.
@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in get_all_products():
        title = i[1]
        description = i[2]
        price = i[3]
        with open(f'{description + ".png"}', 'rb') as png:
            await message.answer_photo(png, caption=f'{title} | {description} | price: {price}')

    await message.answer(text='Выберите продукт для покупки: ', reply_markup=fruit_menu)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text='back_to_catalog')
async def back(call):
    await call.message.answer("Тест закончен")


# Создание Inline меню
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


# Показать формулу
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора:\n'
                              'Для мужчин: 10 * вес + 6.25 * рост - 5 * возраст + 5\n'
                              'Для женщин: 10 * вес + 6.25 * рост - 5 * возраст - 161')


# Запуск клавиатуры при старте.
@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Начало диалога через вызов call
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = float(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])

    man = 10 * weight + 6.25 * growth - 5 * age + 5
    woman = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f"Норма калорий для мужчин: {man}\n"
                         f"Норма калорий для женщин: {woman}")

    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


# =================================================================================================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
