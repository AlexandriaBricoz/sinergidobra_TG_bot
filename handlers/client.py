import asyncio
import sqlite3
from datetime import datetime, date, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatPermissions

import payment
from create_bot import bot, bot_address, dp
from keyboards.client_kb import keyboard, kb_client, back_keyboard_1, back_keyboard_0, pay_3_1, pay_3_2, pay_2
from order_DB import Orders
from school_database import sqlite_db
from school_database.sqlite_db import get_all_subscriptions

"""Хендлеры для взаимодействия с клиентом

    group_id:-1002030571529
    
    Иван Неретин 1085385124
"""


def start():
    loop = asyncio.get_event_loop()
    loop.create_task(remind_subscriptions())
    loop1 = asyncio.get_event_loop()
    loop1.create_task(remove_expired_subscriptions())


async def remove_expired_subscriptions():
    while True:
        # Ваш код удаления пользователей с истекшим сроком подписки
        conn = sqlite3.connect('bot_sql.db')
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE end_date < date('now')")
        expired_users = cur.fetchall()  # Получаем список пользователей с истекшим сроком подписки
        cur.execute("DELETE FROM users WHERE end_date < date('now')")
        conn.commit()
        conn.close()

        # Удаление пользователей из группы
        for user_id in expired_users:
            try:
                # Указываете идентификатор группы, из которой нужно удалить пользователя
                group_id = -1002030571529
                await bot.restrict_chat_member(group_id, user_id, ChatPermissions(can_send_messages=False))
                await bot.kick_chat_member(group_id, user_id)
                print(f"Пользователь {user_id} исключен из группы.")
            except Exception as e:
                print(f"Ошибка при удалении пользователя из группы: {e}")

        # Пауза на один день перед следующей проверкой
        await asyncio.sleep(86400)  # 86400 секунд = 24 часа


async def remind_subscriptions():
    print(1)
    while True:
        try:
            # Получаем список подписок из базы данных
            subscriptions = get_all_subscriptions()

            # Получаем текущую дату
            current_date = date.today()

            # Перебираем подписки
            for subscription in subscriptions:
                id, user_id, username, full_name, start_date, end_date = subscription

                # Проверяем, сколько дней осталось до окончания подписки
                days_left = (datetime.strptime(end_date, '%Y-%m-%d').date() - current_date).days

                # Если остался ровно один день до окончания подписки, отправляем уведомление
                if days_left == 1:
                    message = f"{full_name}!Ваша подписка закончится завтра. Пожалуйста, продлите её!"
                    await bot.send_message(user_id, message)

        except Exception as e:
            print(f"Произошла ошибка при отправке уведомлений: {e}")

        # Пауза на один день перед следующей проверкой
        await asyncio.sleep(86400)  # 86400 секунд = 24 часа


# Обработчик команды /groupid
@dp.message_handler(commands=['groupid'])
async def show_group_id(message: types.Message):
    # Проверяем, является ли сообщение отправленным в группу
    if message.chat.type != types.ChatType.PRIVATE:
        # Отправляем идентификатор группы
        await message.reply(f"ID этой группы: {message.chat.id}")
    else:
        await message.reply("Эта команда работает только в группах.")


# Обработчик команды /kick
async def kick_user(message: types.Message, user_id, group_id):
    # Проверяем, является ли сообщение отправленным в личные сообщения боту
    if message.chat.type == types.ChatType.PRIVATE:
        # Проверяем, что отправитель команды указал идентификатор группы
        if 1:
            try:
                # Получаем идентификатор группы из аргументов команды
                group_id = -1002030571529
                # Проверяем, является ли отправитель команды администратором указанной группы
                if message.from_user.id in [admin.user.id for admin in await bot.get_chat_administrators(group_id)]:
                    # Получаем идентификатор пользователя, которого нужно исключить
                    user_id = 1085385124
                    # Передаем права, запрещающие пользователю отправлять сообщения в группе
                    await bot.restrict_chat_member(group_id, user_id, ChatPermissions(can_send_messages=False))
                    # Исключаем пользователя из группы
                    await bot.kick_chat_member(group_id, user_id)
                    await message.reply(
                        f"Пользователь {message.reply_to_message.from_user.full_name} исключен из группы.")
                else:
                    await message.reply("Вы не являетесь администратором указанной группы.")
            except ValueError:
                await message.reply("Идентификатор группы должен быть числом.")
        else:
            await message.reply("Вы должны указать идентификатор группы вместе с командой.")
    else:
        await message.reply("Команда /kick должна быть использована в личных сообщениях боту.")


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    bot_home = bot_address  # можно указать адрес бота в телеграм строкой 't.me/bot'
    print(message.from_user.id, message.from_user.full_name)

    await bot.send_message(message.from_user.id,
                           f'Приветствуем вас, {message.from_user.full_name} 👋',
                           reply_markup=kb_client
                           )
    await bot.send_message(message.from_user.id,
                           f'🗓 Выберите свой тарифный план👇👋',
                           reply_markup=keyboard)

    # await message.reply(f'Пожалуйста напишите боту в ЛС: {bot_home}')


def create_pay_button(message: types.Message, amount, description):
    pay = payment.create_payment(full_name=message.from_user.full_name, amount=amount, description=description)
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=description, callback_data="tariff_3_1",
                                        url=pay.confirmation.confirmation_url)
    print(pay.id)
    # Добавляем кнопки на клавиатуру в виде списка
    orders = Orders()
    orders.create_order(pay.id, message.from_user.id, message.from_user.username,
                        message.from_user.full_name, pay.description, amount)
    keyboard.add(button)
    confirm_keyboard = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton(text='Проверить', callback_data=f"order {pay.id}")
    # Добавляем кнопки на клавиатуру в виде списка
    confirm_keyboard.add(confirm_button)
    return keyboard, confirm_keyboard


@dp.callback_query_handler(lambda c: c.data.startswith('tariff'))
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    if data == "tariff_1":
        await callback_query.message.reply("Бесплатный урок - попробуйте мой стиль ведения занятий.",
                                           reply_markup=back_keyboard_1)
    elif data == "tariff_2":
        keybourd, confirm_keybourd = create_pay_button(callback_query, 1.00,
                                                       "Купить курс за 1490")
        await callback_query.message.reply("Курс для новичков - 4 практики на основные направления "
                                           "подвижности с подробными инструкциями и отстройками.",
                                           reply_markup=keybourd)
        await callback_query.message.reply("Отличный выбор", reply_markup=confirm_keybourd)
    elif data == "tariff_3":
        keybourd, confirm_keybourd = create_pay_button(callback_query, 2.00, "Оплатить онлайн клуб на месяц 2800₽")
        await callback_query.message.reply("Клуб - это возможность участвовать в онлайн-тренировках "
                                           "и получать доступ к записям занятий.",
                                           reply_markup=keybourd)
        await callback_query.message.reply("Отличный выбор", reply_markup=confirm_keybourd)
    if data == "tariff_1_1":
        await callback_query.message.reply("https://www.youtube.com/watch?v=Q8axQa1QSCI",
                                           reply_markup=back_keyboard_0)
    elif data == "tariff_2_1":
        await callback_query.message.reply("Отличный выбор, переходим к оплате", reply_markup=pay_2)
    elif data == "tariff_3_1":
        await callback_query.message.reply("Отличный выбор, переходим к оплате", reply_markup=pay_3_1)
    elif data == "tariff_3_2":
        await callback_query.message.reply("Для того чтобы заниматься в клубе офлайн свяжитесь с куратором",
                                           reply_markup=pay_3_2)
    elif data == "tariff_3_2_1":
        await get_contacts(callback_query)
    elif data == "tariff_0":
        await callback_query.message.reply(
            f'🗓 Выберите свой тарифный план👇👋',
            reply_markup=keyboard)
    # else:о
    #     await callback_query.message.reply("Произошла ошибка. Пжалуйста, попробуйте еще раз.")


@dp.callback_query_handler(lambda c: c.data.startswith('order'))
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()

    data = callback_query.data
    if payment.check_payment_status(data[6:]):
        orders = Orders()
        orders.confirm_order(data[6:])
        sqlite_db.add_subscription(str(callback_query.from_user.id), str(callback_query.from_user.username),
                                   str(callback_query.from_user.full_name),
                                   datetime.now().date(),
                                   datetime.now().date() + timedelta(days=31))
        await callback_query.message.reply("Оплата прошла УСПЕШНО")
    else:
        await callback_query.message.reply("Оплата прошла НЕУСПЕШНО")


@dp.message_handler(Text(equals='Помощь', ignore_case=True))
async def get_contacts(message: types.Message):
    address = "lt.oren@mail.ru"
    phones = '+7 903 360-69-03'
    telegram = '@russian_yoga_girl'
    await bot.send_message(message.from_user.id, f'Почта:: {address} \nКонтактный номер: {phones}'
                                                 f'\nТелеграмм: {telegram}', )


@dp.message_handler(Text(equals='Курс для новичков', ignore_case=True))
async def course_for_beginners(message: types.Message):
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
    try:
        await bot.send_message(message.from_user.id,
                               f'Ваша подписка действует до {sqlite_db.get_subscriptions_by_user_id(message.from_user.id)[0][5]}')
    except:
        await bot.send_message(message.from_user.id,
                               f'К сожалению, у вас нет подписки')


@dp.message_handler(Text(equals='Тарифные планы', ignore_case=True))
async def tariffs(message: types.Message, ):
    await bot.send_message(message.from_user.id,
                           f'🗓 Выберите свой тарифный план👇👋',
                           reply_markup=keyboard)


# Обработчик команды /kick
@dp.message_handler(commands=['kick'])
async def kick_user(message: types.Message):
    # Проверяем, что отправитель сообщения является администратором группы
    if message.from_user.id in [admin.user.id for admin in await bot.get_chat_administrators(message.chat.id)]:
        # Идентификатор пользователя, которого нужно исключить
        user_id = message.reply_to_message.from_user.id
        # Передаем права, запрещающие пользователю отправлять сообщения в группе
        await bot.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False))
        # Исключаем пользователя из группы
        await bot.kick_chat_member(message.chat.id, user_id)
        await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} исключен из группы.")
    else:
        await message.reply("Вы не являетесь администратором этой группы.")


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, Text(equals='Помощь', ignore_case=True))
    dp.register_message_handler(set_tariff, Text(equals='Оплатить', ignore_case=True))
    dp.register_message_handler(my_tariff, Text(equals='Моя подписка', ignore_case=True))
    dp.register_message_handler(tariffs, Text(equals='Тарифные планы', ignore_case=True))
