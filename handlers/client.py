from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from create_bot import bot, bot_address, dp
from keyboards.client_kb import keyboard
from school_database import sqlite_db

"""Хендлеры для взаимодействия с клиентом
"""


# @dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    bot_home = bot_address  # можно указать адрес бота в телеграм строкой 't.me/bot'
    await bot.send_message(message.from_user.id,
                           f'Приветствуем вас, {message.from_user.full_name} 👋',
                           )
    await bot.send_message(message.from_user.id,
                           f'🗓 Выберите свой тарифный план👇👋',
                           reply_markup=keyboard)

    # await message.reply(f'Пожалуйста напишите боту в ЛС: {bot_home}')


@dp.callback_query_handler(lambda c: c.data.startswith('button'))
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    if data == "button1":
        await callback_query.message.reply("Бесплатный урок - это отличная возможность познакомиться с моим стилем ведения занятий и убедиться, что йога подходит именно вам!")
    elif data == "button2":
        await callback_query.message.reply("Курс для новичков - идеальный выбор для тех, кто только начинает свой путь в йоге. Мы погружаемся в основы практики и сосредотачиваемся на укреплении основ.")
    elif data == "button3":
        await callback_query.message.reply("Онлайн-клуб - это возможность участвовать в онлайн-тренировках, получать доступ к эксклюзивным материалам и общаться с другими участниками виртуального сообщества.")
    elif data == "button4":
        await callback_query.message.reply("Офлайн-клуб - для тех, кто предпочитает живые занятия. Присоединяйтесь к нашему клубу и наслаждайтесь занятиями в атмосфере спокойствия и гармонии.")
    else:
        await callback_query.message.reply("Произошла ошибка. Пожалуйста, попробуйте еще раз.")



@dp.message_handler(Text(equals='Контакты', ignore_case=True))
async def get_contacts(message: types.Message):
    address = "Yoga's Street, 00/00"
    phones = '+000 000-00-00'
    await bot.send_message(message.from_user.id, f'Адрес школы: {address} \nКонтактные номера: {phones}')


# @dp.message_handler(Text(equals='Режим работы', ignore_case=True))
async def get_work_hours(message: types.Message):
    w_days = 'пн-вс'
    w_hours = '06.30–22.30'
    await bot.send_message(message.from_user.id, f'Время работы: {w_days} {w_hours}')


# @dp.message_handler(Text(equals='Тренировки', ignore_case=True))
async def get_training_courses(message: types.Message):
    await sqlite_db.sql_read_from_courses(message)


# @dp.message_handler(Text(equals='Преподаватели', ignore_case=True))
async def get_trainers_info(message: types.Message):
    await sqlite_db.sql_read_from_teachers(message)


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, Text(equals='Контакты', ignore_case=True))
    dp.register_message_handler(get_work_hours, Text(equals='Режим работы', ignore_case=True))
    dp.register_message_handler(get_training_courses, Text(equals='Тренировки', ignore_case=True))
    dp.register_message_handler(get_trainers_info, Text(equals='Супер', ignore_case=True))
