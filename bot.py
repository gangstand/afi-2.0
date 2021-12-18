import logging
import sqlite3
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN

# Подключаем БД
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


def db_table_val(user_id: int, user_name: str, username: str, groupa: str):
    cursor.execute('INSERT INTO Aristotle (user_id, user_name, username, groupa) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, username, groupa))
    conn.commit()


# Создаём кнопки
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Домашнее задание", "Авторы", "Библиотека", "Новости"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


# Меню
@dp.message_handler(lambda message: message.text == "Меню")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Домашнее задание", "Авторы", "Библиотека", "Новости"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


# Используем кнопку 1
@dp.message_handler(lambda message: message.text == "Домашнее задание")
async def without_puree(message: types.Message):
    # Используем кнопку 1.1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Смотреть дз", "Поменять группу", "Меню"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


# Проверка на грруппу и добавление данных в бд
@dp.message_handler(lambda message: message.text.isupper())
async def get_name(message: types.Message):
    global action
    action = message.text
    if (action.isdigit() == False) and (action.isupper() == True):
        await message.answer('Группа установлена')
        # переменные бд

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        usernames = message.from_user.username
        group = message.text

        db_table_val(user_id=us_id, user_name=us_name, username=usernames, groupa=group)


# Используем кнопки 2
@dp.message_handler(lambda message: message.text == "Авторы")
async def without_puree(message: types.Message):
    await message.answer("---Аристотель---\nСоздатели проекта:\nБойко Артём\nСбоев Артём\nКульпинов Никита")


# Используем кнопки 3
@dp.message_handler(lambda message: message.text == "Библиотека")
async def without_puree(message: types.Message):
    # Используем кнопку 3.1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["По автору", "По названию", "Каталог", "Меню"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


# Используем кнопки 4
@dp.message_handler(lambda message: message.text == "Новости")
async def without_puree(message: types.Message):
    URL = 'https://www.rksi.ru/news'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
    }

    resource = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(resource.content, "html.parser")
    items = soup.find_all('div', class_='flexnews')

    for item in items:
        item = item.find("div")
        await message.answer(item.text[10:])


# Замена неправильной группы
@dp.message_handler(lambda message: message.text == "Поменять группу")
async def cmd_start(message: types.Message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    people_id = message.from_user.id
    cursor.execute(f"DELETE FROM Aristotle WHERE user_id = {people_id}")
    conn.commit()
    await message.answer("Введите свою группу")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
