from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, master_id
from keyboards.manage_kb import kb_manage_3
from school_database import sqlite_db
from school_database.sqlite_db import remove_expired_subscriptions

"""Администрирование Бота через FSM
Внесение изменений в базу через интерфейс Telegram
Владелец школы сможет сам управлять содержимым курсов/тренировок
и стоимостью в мобильном телефоне.
"""

ID_MASTER = int(master_id)


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
    if id_check == ID_MASTER:
        await bot.send_message(message.from_user.id, 'Готов к работе, пожалуйста выбери команды на клавиатуре',
                               reply_markup=kb_manage_3)
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()


# @dp.message_handler(commands=['Ученики'])
async def output_users(message: types.Message):
    id_check = message.from_user.id
    print(1)
    await bot.send_message(message.from_user.id, 'Список активных подписчиков:')
    if id_check == ID_MASTER:
        answer = ''
        for i in sqlite_db.get_all_subscriptions():
            answer = f'{answer}\nuser: {i[2]}, full_name:{i[3]} start: {i[4]} end: {i[5]}'

        await bot.send_message(message.from_user.id, answer)
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()


"""Регистрируем хендлеры
"""


def handlers_register_manage(dp: Dispatcher):
    # FSM для курсов
    dp.register_message_handler(verify_owner, commands=['moderate'])
    dp.register_message_handler(output_users, Text(equals='Ученики', ignore_case=True))
