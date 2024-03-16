import io

import pandas as pd
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, masters_id
from handlers.client import remove_expired_subscriptions
from keyboards.manage_kb import kb_manage_3
from order_DB import Orders
from school_database import sqlite_db

"""Администрирование Бота через FSM
Внесение изменений в базу через интерфейс Telegram
Владелец школы сможет сам управлять содержимым курсов/тренировок
и стоимостью в мобильном телефоне.
"""

ID_MASTER = masters_id


class FSMcourses(StatesGroup):
    title = State()
    photo = State()
    description = State()
    timetable = State()
    duration_of_lesson = State()
    price_of_lesson = State()


class FSMteacher(StatesGroup):
    name = State()
    photo = State()
    description = State()
    courses = State()


"""Бот проверяет является ли пользователь хозяином бота.
Проверка ID_MASTER по ID на совпадение
В целях безопасности необходимо установить запрет на добавление Бота в другие группы!
Активация клавиатуры администратора по команде /moderate
"""


# @dp.message_handler(commands=['moderate'])
async def verify_owner(message: types.Message):
    id_check = message.from_user.id
    if id_check in ID_MASTER:
        await bot.send_message(message.from_user.id, 'Готов к работе, пожалуйста выбери команды на клавиатуре',
                               reply_markup=kb_manage_3)
        await remove_expired_subscriptions()
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()


# @dp.message_handler(commands=['Ученики'])
async def output_users(message: types.Message):
    id_check = message.from_user.id
    if id_check in ID_MASTER:
        answer = ''
        for i in sqlite_db.get_all_subscriptions():
            answer = f'{answer}\nusername: {i[2]}, full_name:{i[3]} start: {i[4]} end: {i[5]}'
        data = []
        for i in sqlite_db.get_all_subscriptions():
            data.append([
                i[1], i[2], i[3], i[4], i[5]
            ])
        df = pd.DataFrame(data, columns=['ID пользователя', 'имя пользователя', 'полное имя', 'начало', 'конец'])
        buffer = io.BytesIO()
        buffer.name = 'users.xlsx'
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(excel_writer=writer, sheet_name='Users', engine='xlsxwriter')
        buffer.seek(0)
        await bot.send_document(message.from_user.id, document=buffer)
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()


# @dp.message_handler(commands=['Платежи'])
async def output_pay(message: types.Message):
    id_check = message.from_user.id
    orders = Orders()
    if id_check in ID_MASTER:
        data = []
        for i in orders.get_all_orders():
            data.append([
                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]
            ])
        df = pd.DataFrame(data,
                          columns=['ID заказа', 'ID пользователя', 'имя пользователя', 'полное имя', 'дата создания',
                                   'дата подтверждения',
                                   'статус', 'артикул', 'цена'])
        buffer = io.BytesIO()
        buffer.name = 'orders.xlsx'
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(excel_writer=writer, sheet_name='Orders', engine='xlsxwriter')
        buffer.seek(0)
        await bot.send_document(message.from_user.id, document=buffer)
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()


async def output_log(message: types.Message):
    id_check = message.from_user.id
    orders = Orders()
    if id_check in ID_MASTER:
        with open('log.txt', 'rb') as file:
            await bot.send_document(message.from_user.id, document=file)
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()


"""Регистрируем хендлеры
"""


def handlers_register_manage(dp: Dispatcher):
    # FSM для курсов
    dp.register_message_handler(verify_owner, commands=['moderate'])
    dp.register_message_handler(output_users, Text(equals='Ученики', ignore_case=True))
    dp.register_message_handler(output_pay, Text(equals='Платежи', ignore_case=True))
    dp.register_message_handler(output_log, Text(equals='Логи', ignore_case=True))
