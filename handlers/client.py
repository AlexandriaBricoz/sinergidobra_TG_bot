import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from create_bot import bot, bot_address, dp
from keyboards.client_kb import keyboard, kb_client, kb_client_1, back_keyboard_1, back_keyboard_2, back_keyboard_3, \
    back_keyboard_0
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


@dp.callback_query_handler(lambda c: c.data.startswith('tariff'))
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    if data == "tariff_1":

        await callback_query.message.reply("Бесплатный урок - это отличная возможность познакомиться с моим "
                                           "стилем ведения занятий и убедиться, что йога подходит именно вам!",
                                           reply_markup=back_keyboard_1)
    elif data == "tariff_2":
        await callback_query.message.reply("Курс для новичков - идеальный выбор для тех, кто только начинает "
                                           "свой путь в йоге. Мы погружаемся в основы практики и сосредотачиваемся"
                                           " на укреплении основ.",
                                           reply_markup=back_keyboard_2)
    elif data == "tariff_3":
        await callback_query.message.reply("Клуб - это возможность участвовать в онлайн-тренировках, "
                                           "получать доступ к эксклюзивным материалам и общаться с другими"
                                           " участниками виртуального сообщества.",
                                           reply_markup=back_keyboard_3)
    if data == "tariff_1_1":
        await callback_query.message.reply("https://www.youtube.com/watch?v=Q8axQa1QSCI",
                                           reply_markup=back_keyboard_0)
    elif data == "tariff_2_1":
        await callback_query.message.reply("Отличный выбор, переходим к оплате", reply_markup=kb_client_1)
    elif data == "tariff_3_1":
        await callback_query.message.reply("Отличный выбор, переходим к оплате", reply_markup=kb_client_1)
    elif data == "tariff_3_2":
        await callback_query.message.reply("Отличный выбор, переходим к оплате", reply_markup=kb_client_1)
    elif data == "tariff_0":
        await callback_query.message.reply(
            f'🗓 Выберите свой тарифный план👇👋',
            reply_markup=keyboard)
    # else:
    #     await callback_query.message.reply("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


@dp.message_handler(Text(equals='Помощь', ignore_case=True))
async def get_contacts(message: types.Message):
    address = "lt.oren@mail.ru"
    phones = '+7 903 360-69-03'
    telegram = '@russian_yoga_girl'
    await bot.send_message(message.from_user.id, f'Почта:: {address} \nКонтактный номер: {phones}'
                                                 f'\nТелеграмм: {telegram}', )


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
async def set_tariff(message: types.Message, ):
    sqlite_db.add_subscription(str(message.from_user.id), str(message.from_user.username),
                               str(message.from_user.full_name),
                               datetime.datetime.now().date(),
                               datetime.datetime.now().date() + datetime.timedelta(days=31))
    await bot.send_message(message.from_user.id,
                           f'Оплата прошла успешно', reply_markup=kb_client)


@dp.message_handler(Text(equals='Моя подписка', ignore_case=True))
async def my_tariff(message: types.Message, ):
    await bot.send_message(message.from_user.id,
                           f'Ваша подписка действует до {sqlite_db.get_subscriptions_by_user_id(message.from_user.id)[0][5]}')


@dp.message_handler(Text(equals='Тарифные планы', ignore_case=True))
async def tariffs(message: types.Message, ):
    await bot.send_message(message.from_user.id,
                           f'🗓 Выберите свой тарифный план👇👋',
                           reply_markup=keyboard)

def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, Text(equals='Помощь', ignore_case=True))
    dp.register_message_handler(set_tariff, Text(equals='Оплатить', ignore_case=True))
    dp.register_message_handler(my_tariff, Text(equals='Моя подписка', ignore_case=True))
    dp.register_message_handler(tariffs, Text(equals='Тарифные планы', ignore_case=True))