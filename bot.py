import logging
import time
import os
from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import requests
from bs4 import BeautifulSoup
from config import BOT_TOKEN

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
# Объект бота
bot = Bot(BOT_TOKEN)
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
    buttons = ["Домашнее задание", "Авторы", "Библиотека", "Новости", "Для преподавателей"]
    keyboard.add(*buttons)
    await message.answer("Введите свою группу, чтобы добавить вас в базу данных.\nНапример: ИС-15 \nВыберите кнопку",
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Меню")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Домашнее задание", "Авторы", "Библиотека", "Новости", "Для преподавателей"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Для преподавателей")
async def without_pur1(message: types.Message):
    await message.answer('Введите пароль')


@dp.message_handler(lambda message: message.text == "8767")
async def without_pur1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Выслать домашнее задание", "Меню"]
    keyboard.add(*buttons)
    await message.answer('Успешно, выберите кнопку', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Выслать домашнее задание")
async def without_pur1(message: types.Message):
    with open('instr.jpg', 'rb') as photo:
        await message.reply_photo(photo=photo,
                                  caption='Должно быть только 2 пробела!!!\nДомашнее задание отправляем на примере команды:\n "/dz Русский_язык_стр_34_№2 ИС-15"')


# Используем кнопку 1
@dp.message_handler(lambda message: message.text == "Домашнее задание")
async def without_puree(message: types.Message):
    # Используем кнопку 1.1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Смотреть дз", "Поменять группу", "Меню"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)

    # Используем кнопки dz для преподов


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


@dp.message_handler(commands="dz")
async def without_puree(message: types.Message):
    try:
        dz = message.text
        list_message = dz.split(' ')
        print(list_message, file=open("output3.txt", "a"))
        cursor.execute("SELECT * FROM Aristotle")
        records = cursor.fetchall()
        for row in records:
            print(row, file=open("output.txt", "a"))
        group_1 = list_message[2]
        with open('output.txt') as file:
            for line in file:
                if group_1 in line:
                    lines = line.replace('\n', '')
                    print(lines, file=open("output1.txt", "a"))
        time.sleep(1)
        with open('output1.txt', 'r') as f:
            for line in f:
                text1 = list(line)
                text2 = ' '.join(text1)
                text3 = text2.replace(' ', '')
                text4 = text3.split(',')
                id = text4[1]
                domzad = list_message[1]
                await bot.send_message(chat_id=id, text=domzad)
        path = "output.txt"
        os.remove(path)
        path = "output3.txt"
        os.remove(path)
        path = "output1.txt"
        os.remove(path)
    except:
        await message.answer('Пользователи из данной группы не зарегестрированы/Домашнее задание неправильного формата')


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


@dp.message_handler(lambda message: message.text == "По автору")
async def without_puree(message: types.Message):
    # Используем кнопку 3.1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Меню"]
    keyboard.add(*buttons)
    await message.answer("Введите интересующего автора", reply_markup=keyboard)
    a = input()
    superhero_dict = {'Никита Кульпинов': 'Рекомендации по налаживанию бизнеса',
                      'Артём Бойко': '5 шагов к счастью',
                      'Артём Сбоев': 'Танцевальный успех или как танцами покорить сердце девушке'}
    if a in superhero_dict:
        print(superhero_dict.get(a))
    else:
        print("Такой автор не найден")


# Используем кнопки 3
@dp.message_handler(lambda message: message.text == "По названию")
async def without_puree(message: types.Message):
    # Используем кнопку 3.1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Меню"]
    keyboard.add(*buttons)
    await message.answer("Введите название книги", reply_markup=keyboard)
    b = input()
    superhero_dict = {'Рекомендации по налаживанию бизнеса': 'Никита Кульпинов',
                      '5 шагов к счастью': 'Артём Бойко',
                      'Танцевальный успех или как танцами покорить сердце девушке': 'Артём Сбоев'}
    if b in superhero_dict:
        print(superhero_dict.get(b))
    else:
        print("Такое название не найдено")


@dp.message_handler(lambda message: message.text == "Каталог")
async def without_puree(message: types.Message):
    # Используем кнопку 3.1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Меню"]
    keyboard.add(*buttons)
    await message.answer("Введите каталог", reply_markup=keyboard)
    superhero_dict = {'[0] Никита Кульпинов': 'Рекомендации по налаживанию бизнеса',
                      '[1] Артём Бойко': '5 шагов к счастью',
                      '[2] Артём Сбоев': 'Танцевальный успех или как танцами покорить сердце девушке'}
    print(superhero_dict)
    a = input()
    print(superhero_dict[a])


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
    items1 = soup.select("img")[3].attrs["src"]
    i = 2
    for item in items:
        i += 1
        await message.answer(item.text[11:] + "\nhttps://www.rksi.ru/" + soup.select("img")[i].attrs["src"])


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
