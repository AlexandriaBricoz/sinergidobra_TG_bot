import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from create_bot import bot, bot_address, dp
from keyboards.client_kb import keyboard, kb_client, kb_client_1, back_keyboard
from school_database import sqlite_db

"""Хендлеры для взаимодействия с клиентом
"""


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    bot_home = bot_address  # можно указать адрес бота в телеграм строкой 't.me/bot'

    await bot.send_message(message.from_user.id,
                           f'Приветствуем вас, {message.from_user.full_name} 👋',
                           reply_markup=kb_client
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
        await callback_query.message.reply("Бесплатный урок - это отличная возможность познакомиться с моим "
                                           "стилем ведения занятий и убедиться, что йога подходит именно вам!")
    elif data == "button2":
        await callback_query.message.reply("Курс для новичков - идеальный выбор для тех, кто только начинает "
                                           "свой путь в йоге. Мы погружаемся в основы практики и сосредотачиваемся"
                                           " на укреплении основ.",
                                           reply_markup=back_keyboard)
    elif data == "button3":
        await callback_query.message.reply("Онлайн-клуб - это возможность участвовать в онлайн-тренировках, "
                                           "получать доступ к эксклюзивным материалам и общаться с другими"
                                           " участниками виртуального сообщества.")
    elif data == "button4":
        await callback_query.message.reply("Офлайн-клуб - для тех, кто предпочитает живые занятия. Присоединяйтесь "
                                           "к нашему клубу и наслаждайтесь занятиями в атмосфере"
                                           " спокойствия и гармонии.")
    elif data == "button5":
        await callback_query.message.reply(
                               f'🗓 Выберите свой тарифный план👇👋',
                               reply_markup=keyboard)
    elif data == "button6":
        await callback_query.message.reply("Отличный выбор, переходим к оплате", reply_markup=kb_client_1)       # ЛЮТЫЙ БАГ
    else:
        await callback_query.message.reply("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


@dp.message_handler(Text(equals='Помощь', ignore_case=True))
async def get_contacts(message: types.Message):
    address = "lt.oren@mail.ru"
    phones = '+7 903 360-69-03'
    await bot.send_message(message.from_user.id, f'Почта:: {address} \nКонтактный номер: {phones}')


@dp.message_handler(Text(equals='Курс для новичков', ignore_case=True))
async def get_contacts(message: types.Message):
    address = "lt.oren@mail.ru"
    phones = '+7 903 360-69-03'
    await bot.send_message(message.from_user.id, f'1 Урок. Общая мобилизация.\n\n'
                                                 f'https://youtu.be/wPY_pjVaCPw\n\n'
                                                 f'2 Урок. Продольное направление. Подготовка к продольному шпагату.\n\n'
                                                 f'https://youtu.be/Bg8UdyWs25Q\n\n'
                                                 f'3 Урок. Поперечное направление. Подготовка к поперечному шпагату.\n\n'
                                                 f'https://youtu.be/LvVoG9Eprb8\n\n'
                                                 f'4 Урок. Проработка тазобедренных суставов.\n\n'
                                                 f'https://youtu.be/1RwMGYVDGS8\n\n'
                                                 f'Уроки необходимо чередовать, делая между ними равные по времени перерывы. Например, через день.\n'
                                                 f'Не забывайте, что занимаясь по видео, вы всегда можете поставить запись на паузу, '
                                                 f'чтобы уделить большее внимание отдельным упражнениям, прислушивайтесь к себе и будьте осознанны в своей практике.\n'
                                                 f'Впоследствие буду рада обратной связи 🌷')


@dp.message_handler(Text(equals='Оплатить', ignore_case=True))
async def set_tariff(message: types.Message,):
    sqlite_db.add_subscription(str(message.from_user.id), str(message.from_user.username),
                               str(message.from_user.full_name),
                               datetime.datetime.now().date(),
                               datetime.datetime.now().date() + datetime.timedelta(days=31))


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, Text(equals='Помощь', ignore_case=True))
    dp.register_message_handler(set_tariff, Text(equals='Оплатить', ignore_case=True))
