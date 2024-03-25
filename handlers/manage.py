import io

import pandas as pd
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, masters_id
from keyboards.manage_kb import kb_manage_3
from order_DB import Orders, Orders2

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
        await bot.send_message(message.from_user.id, 'Готов к работе, пожалуйста выберите команды на клавиатуре',
                               reply_markup=kb_manage_3)
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()


# @dp.message_handler(commands=['Ученики'])
async def output_users(message: types.Message):
    id_check = message.from_user.id
    if id_check in ID_MASTER:
        orders = Orders2()
        data = []
        for i in orders.get_all_orders():
            print(i)
            data.append([
                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15]
            ])
        df = pd.DataFrame(data, columns=['id', 'user_id', 'username', 'ФИО', 'Номер телефона', 'email', 'контакты',
                                         'С кем работаете?', 'Тема мастер-класса',
                                         'Регалии', 'Сколько по времени длится занятие?', 'Нужны ли инструменты?',
                                         'Инструменты', 'Максимальное количество учеников', 'О себе', 'дата'])
        buffer = io.BytesIO()
        buffer.name = 'Заявки на волонтёрство.xlsx'
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(excel_writer=writer, sheet_name='Заявки на волонтёрство', engine='xlsxwriter')
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
                          columns=['id', 'user_id', 'username', 'ФИО', 'Возраст', 'Желаемая тема мастер-класса',
                                   'Есть ли у Вас дети?', 'Возраст ребенка (детей)',
                                   'дата'])
        buffer = io.BytesIO()
        buffer.name = 'Заявки на мастер-класс.xlsx'
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(excel_writer=writer, sheet_name='Заявки на мастер-класс', engine='xlsxwriter')
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
    dp.register_message_handler(output_users, Text(equals='Заявки на волонтёрство', ignore_case=True))
    dp.register_message_handler(output_pay, Text(equals='Заявки на мастер-класс', ignore_case=True))
    dp.register_message_handler(output_log, Text(equals='Логи', ignore_case=True))
