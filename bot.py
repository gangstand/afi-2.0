# -*- coding: utf-8 -*-
import logging
import time
import os
from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import requests
from bs4 import BeautifulSoup
import random
from config import BOT_TOKEN

# Подключаем БД
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
# Объект бота
bot = Bot(BOT_TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Список групп РКСИ
list_group = ["ИС-15", "ИС-16", "ПОКС-32", "4СК-ДО2", "БД-11", "БД-12", "БД-21", "БУ-11", "БУ-21", "БУ-41", "Д-21",
              "Д-31", "Д-41", "ИБА-12", "ИБА-13", "ИБА-14", "ИБА-22", "ИБА-24", "ИБА-25", "ИБА-32", "ИБА-34", "ИБА-34",
              "ИБА-42", "ИБА-44", "ИБТ-11", "ИБТ-12", "ИБТ-13", "ИБТ-14", "ИБТ-21", "ИБТ-23", "ИБТ-31", "ИБТ-33",
              "ИБТ-41", "ИБТ-43", "ИКС-11", "ИКС-12", "ИКС-13", "ИС-11", "ИС-12", "ИС-13", "ИС-14", "ИС-15", "ИС-16",
              "ИС-17", "ИС-18", "ИС-21", "КМ-11", "КМ-12", "КМ-21", "КМ-31", "КС-31", "КС-32", "КС-33", "КС-34",
              "КС-35",
              "КС-36", "КС-41", "КС-41", "КС-42", "КС-43", "КС-44", "КС-45", "МТ-21", "МТ-22", "МТ-23", "МТ-24",
              "МТ-31",
              "МТ-32", "МТ-33", "ПИ-23", "ПИ-31", "ПИ-32", "ПИ-33", "ПИ-41", "ПОКС-21", "ПОКС-22", "ПОКС-23", "ПОКС-24",
              "ПОКС-25", "ПОКС-26", "ПОКС-27", "ПОКС-31w", "ПОКС-32b", "ПОКС-33w", "ПОКС-34b", "ПОКС-35b", "ПОКС-36w",
              "ПОКС-37w", "ПОКС-38b", "ПОКС-41", "ПОКС-42", "ПОКС-43", "ПОКС-44", "ПОКС-45", "ПОКС-46", "ПОКС-47",
              "ПОКС-48",
              "ПОКС-49", "РТ-11", "РТ-21", "РТ-31", "СА-11", "СА-12", "СА-13", "СА-14", "СА-15", "СА-16", "СА-17",
              "СА-21",
              "СА-21", "СА-23", "СА-24", "СА-25", "СА-26", "СК-21", "СК-31", "УП-21", "УП-31", "УП-41"]


# Библиотека
def biblioteka(author: str, name: str, link: str):
    bl = cursor.execute('SELECT * FROM Biblioteka WHERE author=?', (author,))
    bl1 = cursor.execute('SELECT * FROM Biblioteka WHERE name=?', (name,))
    bl2 = cursor.execute('SELECT * FROM Biblioteka WHERE link=?', (link,))
    if (bl2.fetchone()) is None:
        cursor.execute('INSERT INTO Biblioteka (author, name, link) VALUES (?, ?, ?)',
                       (author, name, link))
        conn.commit()
    else:
        pass


# Регистрация пользователя
def db_table_val(user_id: int, user_name: str, username: str, groupa: str):
    info = cursor.execute('SELECT * FROM Aristotle WHERE user_id=?', (user_id,))
    if info.fetchone() is None:
        cursor.execute('INSERT INTO Aristotle (user_id, user_name, username, groupa) VALUES (?, ?, ?, ?)',
                       (user_id, user_name, username, groupa))
        conn.commit()
    else:
        pass


# Старт
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📖Домашнее задание📖", "👨‍💻Авторы👨‍💻", "📚Библиотека📚", "📜Новости📜", "⚙️Аккаунт⚙️",
               "👨‍🏫Для преподавателей👩‍🏫"]
    keyboard.add(*buttons)
    await message.answer(
        "_________🎓Аристотель бот🎓_________\n✅Домашнее задание и библиотека в одном чате. \n✅Введите свою группу, чтобы добавить вас в базу данных.\nНапример: ИС-15 \n✅Выберите кнопку:",
        reply_markup=keyboard)


# Меню
@dp.message_handler(lambda message: message.text == "↪️Меню↩️")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📖Домашнее задание📖", "👨‍💻Авторы👨‍💻", "📚Библиотека📚", "📜Новости📜", "⚙️Аккаунт⚙️",
               "👨‍🏫Для преподавателей👩‍🏫"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


# Новости
@dp.message_handler(lambda message: message.text == "📜Новости📜")
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
    kol = 0
    for item in items:
        i += 1
        kol += 1
        await message.answer("🧾" + item.text[11:] + "\nhttps://www.rksi.ru/" + soup.select("img")[i].attrs["src"])
        if kol == 3:
            break


# Аккаунт
@dp.message_handler(lambda message: message.text == "⚙️Аккаунт⚙️")
async def without_pur1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["💬Поменять группу💬", "❌Удалить аккаунт❌", "↪️Меню↩️"]
    keyboard.add(*buttons)
    await message.answer('Настройки аккаунта', reply_markup=keyboard)


# Замена неправильной группы
@dp.message_handler(lambda message: message.text == "💬Поменять группу💬")
async def cmd_start(message: types.Message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    people_id = message.from_user.id
    cursor.execute(f"DELETE FROM Aristotle WHERE user_id = {people_id}")
    conn.commit()
    await message.answer("Введите свою группу🖋")


# Удалить аккаунт
@dp.message_handler(lambda message: message.text == "❌Удалить аккаунт❌")
async def cmd_start(message: types.Message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    people_id = message.from_user.id
    cursor.execute(f"DELETE FROM Aristotle WHERE user_id = {people_id}")
    conn.commit()
    await message.answer("🚫Аккаунт удалён🚫")


# Для преподавателей
@dp.message_handler(lambda message: message.text == "👨‍🏫Для преподавателей👩‍🏫")
async def without_pur1(message: types.Message):
    await message.answer('Введите пароль')


# Пароль
@dp.message_handler(lambda message: message.text == "8767")
async def without_pur1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📚Добавить книги в библиотеку📚", "📚Удалить книгу из библиотеки📚", "↪️Меню↩️"]
    keyboard.add(*buttons)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="📖Отправить домашнее задание📖", callback_data="instr_dz"))
    keyboard.add(types.InlineKeyboardButton(text="📚Отправить книги📚", callback_data="instr_book"))
    await message.answer('✅Успешно, выберите кнопку', reply_markup=keyboard)


# Инструкция для преподавателей
@dp.callback_query_handler(text="instr_dz")
async def without_pur1(call: types.CallbackQuery):
    with open('instr.jpg', 'rb') as photo:
        await call.message.reply_photo(photo=photo,
                                       caption='❗️Должно быть только 2 пробела!!!❗️\nДомашнее задание отправляем на примере команды:\n "/dz Русский_язык_стр_34_№2 ИС-15"')


# Домашнее задание
@dp.message_handler(lambda message: message.text == "📖Домашнее задание📖")
async def without_puree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📖Смотреть дз📖", "↪️Меню↩️"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "📖Смотреть дз📖")
async def without_puree(message: types.Message):
    people_id = str(message.from_user.id)
    cursor.execute("SELECT * FROM Aristotle")
    uds = cursor.fetchall()
    try:
        for row in uds:
            list = str(row)
            list2 = list.strip("(").strip(")").strip("'").replace(", '", ", ").replace("',", ",").replace(", ", " ")

            list3 = list2.split(' ')

            if people_id == list3[1]:
                gr = list3[4]
                file_id = f'output{gr}.txt'
                print(file=open(file_id, "a"))
                with open(file_id, 'r') as f:
                    fl = f.read()
                    await message.answer(fl)
    except:
        await message.answer("Домашнее задание для вашей группы отсутствует")


# Проверка на грруппу и добавление данных в БД
@dp.message_handler(lambda message: message.text in list_group)
async def get_name(message: types.Message):
    await message.answer(
        '✅Группа изменена. Чтобы поменять группу, перейдите в "Аккаунт"->"Поменять группу", или введите свою группу')
    # переменные бд
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    people_id = message.from_user.id
    cursor.execute(f"DELETE FROM Aristotle WHERE user_id = {people_id}")
    conn.commit()

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    usernames = message.from_user.username
    group = message.text

    db_table_val(user_id=us_id, user_name=us_name, username=usernames, groupa=group)


# Добавление Д/З
@dp.message_handler(commands="dz")
async def without_puree(message: types.Message):
    global domzad
    global list_message
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
                group = list_message[2]
                domzad = list_message[1]
                await bot.send_message(chat_id=id, text="📖" + domzad)
        file_id = f'output{group}.txt'
        print(domzad, file=open(file_id, "a"))
        domzad = list_message[1]

        await message.answer("📖✅" + "Домашнее задание успешно отправлено" + "✅📖")
        path = "output.txt"
        os.remove(path)
        path = "output3.txt"
        os.remove(path)
        path = "output1.txt"
        os.remove(path)
    except:
        await message.answer('Пользователи из данной группы не зарегестрированы/Домашнее задание неправильного формата')


# Авторы
@dp.message_handler(lambda message: message.text == "👨‍💻Авторы👨‍💻")
async def without_puree(message: types.Message):
    await message.answer(
        "_________🎓Аристотель бот🎓_________\n👨‍💻Создатели проекта:\n🥇Бойко Артём🥇\n🥇Сбоев Артём🥇\n🥇Кульпинов Никита🥇")


# Библиотека
# Всё по библиотеке
# Всё по библиотеке
# Всё по библиотеке
@dp.callback_query_handler(text="instr_book")
async def without_pur1(call: types.CallbackQuery):
    with open('instr_book.jpg', 'rb') as photo:
        await call.message.reply_photo(photo=photo,
                                       caption='❗️Должно быть только 3 пробела!!!❗️\nДомашнее задание отправляем на примере команды:\n "/book Алимов Математика_10-11_класс https://clck.ru/ZPfE3"')


@dp.message_handler(commands="book")
async def without_puree(message: types.Message):
    book = message.text
    book_list = book.split(' ')
    try:
        author = book_list[1]
        name = book_list[2]
        link = book_list[3]

        biblioteka(author=author, name=name, link=link)
        await message.answer("📚Книга успешно добавлена в Базу данных📚")
    except IndexError:
        await message.answer("Неверный формат")


# Авторы
@dp.message_handler(lambda message: message.text == "👨‍💻Авторы👨‍💻")
async def without_puree(message: types.Message):
    await message.answer("---Аристотель---\nСоздатели проекта:\nБойко Артём\nСбоев Артём\nКульпинов Никита")


# Библиотека
@dp.message_handler(lambda message: message.text == "📚Библиотека📚")
async def without_puree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["🧑‍💻По автору🧑‍💻", "📣По названию📣", "🗓Каталог🗓", "↪️Меню↩️"]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


# По автору
@dp.message_handler(lambda message: message.text == "🧑‍💻По автору🧑‍💻")
async def without_puree(message: types.Message):
    await message.answer("🧑‍💻Введите интересующего автора:")


# По названию
@dp.message_handler(lambda message: message.text == "📣По названию📣")
async def without_puree(message: types.Message):
    await message.answer("📣Введите название книги:\n❗️Пробелов быть не должно❗️")


# Каталог
@dp.message_handler(lambda message: message.text == "🗓Каталог🗓")
async def without_puree(message: types.Message):
    cursor.execute("SELECT * FROM biblioteka")
    uds = cursor.fetchall()
    for row in uds:
        list = str(row)
        list2 = list.strip("(").strip(")").strip("'").replace("', '", " ")
        list3 = list2.split(' ')
        list4 = list3[:2]
        list5 = str(list4)
        list6 = list5.strip("[").strip("]").strip("'").replace("', '", " --- ")
        await bot.send_message(chat_id=message.chat.id, text=random.choice(["📕", "📗", "📘", "📙"]) + list6)


@dp.message_handler(lambda message: message.text)
async def without_puree(message: types.Message):
    a = message.text
    cursor.execute("SELECT * FROM biblioteka")
    uds = cursor.fetchall()

    for row in uds:
        list = str(row)
        list2 = list.strip("(").strip(")").strip("'").replace("', '", " --- ")
        if a in row:
            await message.answer(random.choice(["📕", "📗", "📘", "📙"]) + list2)
            result = 1
        else:
            result = 0
    if result == 0:
        await message.answer("Такой фичи мы ещё не добавили:(\n🏆Первое обновление после первого места в хакатоне🏆")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
