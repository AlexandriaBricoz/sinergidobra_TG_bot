import asyncio
import sqlite3
from datetime import datetime, date

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatPermissions

import payment
from create_bot import bot, bot_address, dp
from keyboards.client_kb import keyboard_start
from loging import printl
from order_DB import Orders, Orders2
from school_database.sqlite_db import get_all_subscriptions

"""Хендлеры для взаимодействия с клиентом

    group_id:-1002030571529
    
    Иван Неретин 1085385124
"""

from aiogram.dispatcher.filters.state import StatesGroup, State


def start():
    loop = asyncio.get_event_loop()
    loop.create_task(remind_subscriptions())
    loop1 = asyncio.get_event_loop()
    loop1.create_task(remove_expired_subscriptions())


async def remove_expired_subscriptions():
    print('Запущен сервис для удаления пользователей')
    printl('Запущен сервис для удаления пользователей')
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
                printl(f"Пользователь {user_id} исключен из группы.")
            except Exception as e:
                print(f"Ошибка при удалении пользователя из группы: {e}")
                printl(f"Ошибка при удалении пользователя из группы: {e}")

        # Пауза на один день перед следующей проверкой
        await asyncio.sleep(86400)  # 86400 секунд = 24 часа


async def remind_subscriptions():
    print('Напоминая запущены')
    printl('Напоминая запущены')
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
            printl(f"Произошла ошибка при отправке уведомлений: {e}")

        # Пауза на один день перед следующей проверкой
        await asyncio.sleep(86400)  # 86400 секунд = 24 часа


# Обработчик команды /groupid
# @dp.message_handler(commands=['groupid'])
# async def show_group_id(message: types.Message):
#     # Проверяем, является ли сообщение отправленным в группу
#     if message.chat.type != types.ChatType.PRIVATE:
#         # Отправляем идентификатор группы
#         await message.reply(f"ID этой группы: {message.chat.id}")
#     else:
#         await message.reply("Эта команда работает только в группах.")


# Обработчик команды /kick
# async def kick_user(message: types.Message, user_id, group_id):
#     # Проверяем, является ли сообщение отправленным в личные сообщения боту
#     if message.chat.type == types.ChatType.PRIVATE:
#         # Проверяем, что отправитель команды указал идентификатор группы
#         if 1:
#             try:
#                 # Получаем идентификатор группы из аргументов команды
#                 group_id = -1002030571529
#                 # Проверяем, является ли отправитель команды администратором указанной группы
#                 if message.from_user.id in [admin.user.id for admin in await bot.get_chat_administrators(group_id)]:
#                     # Получаем идентификатор пользователя, которого нужно исключить
#                     user_id = 1085385124
#                     # Передаем права, запрещающие пользователю отправлять сообщения в группе
#                     await bot.restrict_chat_member(group_id, user_id, ChatPermissions(can_send_messages=False))
#                     # Исключаем пользователя из группы
#                     await bot.kick_chat_member(group_id, user_id)
#                     await message.reply(
#                         f"Пользователь {message.reply_to_message.from_user.full_name} исключен из группы.")
#                 else:
#                     await message.reply("Вы не являетесь администратором указанной группы.")
#             except ValueError:
#                 await message.reply("Идентификатор группы должен быть числом.")
#         else:
#             await message.reply("Вы должны указать идентификатор группы вместе с командой.")
#     else:
#         await message.reply("Команда /kick должна быть использована в личных сообщениях боту.")


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    bot_home = bot_address  # можно указать адрес бота в телеграм строкой 't.me/bot'
    print(message.from_user.id, message.from_user.full_name, message.from_user.username)
    printl(message.from_user.id, message.from_user.full_name, message.from_user.username)
    photo = open('photo_2024-03-23 20.04.59.jpeg', 'rb')
    await bot.send_photo(message.from_user.id, photo=photo, caption=f'''Наш проект «Содружество Сердец»🇷🇺 направлен на создание общественной поддержки жен военнослужащих, участников СВО, создание условий для повышения социально-психологической поддержки семей участников СВО и вовлечение их на мастер-классы, кураторство, психологические консультации.

Сайт: https://sinergidobra.ru/

Инстаграм проекта «Синергия Добра»: https://www.instagram.com/sinergidobra?igsh=NDUyb3AwbGYyOXFq

Телеграм-канал проекта «Синергия Добра»: https://t.me/sinergidobra''')

    await bot.send_message(message.from_user.id,
                           f'''Если Вы хотите заполнить заявку на волонтерство, напишите боту - заполнить заявку на волонтерство

Если Вы хотели бы участвовать в мастер классе, напишите боту - хочу на мастер-класс''',
                           reply_markup=keyboard_start)
    # await message.reply(f'Пожалуйста напишите боту в ЛС: {bot_home}')


def create_pay_button(message: types.Message, amount, description):
    pay = payment.create_payment(full_name=message.from_user.full_name, amount=amount, description=description)
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=description,
                                        url=pay.confirmation.confirmation_url)
    print('Создана ссылка для ', message.from_user.id, message.from_user.full_name, message.from_user.username, pay.id,
          'Сумма: ', amount, 'Артикул: ', pay.description)
    printl('Создана ссылка для ', message.from_user.id, message.from_user.full_name, message.from_user.username, pay.id,
           'Сумма: ', amount, 'Артикул: ', pay.description)
    # Добавляем кнопки на клавиатуру в виде списка
    orders = Orders()
    orders.create_order(pay.id, message.from_user.id, message.from_user.username,
                        message.from_user.full_name, pay.description, amount)

    confirm_button = types.InlineKeyboardButton(text='Проверить', callback_data=f"order {pay.id} {description}")
    # Добавляем кнопки на клавиатуру в виде списка
    keyboard.add(button).add(confirm_button)
    return keyboard


@dp.message_handler(Text(equals='Соцсети проекта', ignore_case=True))
async def get_contacts(message: types.Message):
    await bot.send_message(message.from_user.id, f'''Познакомиться с проектом «Содружество Сердец»🫶🏻🇷🇺

Сайт: https://sinergidobra.ru/

Инстаграм проекта «Синергия Добра»: https://www.instagram.com/sinergidobra?igsh=NDUyb3AwbGYyOXFq

Телеграм-канал проекта «Синергия Добра»: https://t.me/sinergidobra''', )


class AnketForm(StatesGroup):
    name = State()
    age = State()
    theme = State()
    children = State()
    children_age = State()


@dp.message_handler(Text(equals='Хочу на мастер-класс', ignore_case=True))
async def course_for_beginners(message: types.Message):
    await bot.send_message(message.from_user.id, f'ФИО')
    await AnketForm.name.set()


@dp.message_handler(state=AnketForm.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Возраст")
    await AnketForm.next()


@dp.message_handler(state=AnketForm.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer("Желаемая тема мастер-класса")
    await AnketForm.next()


@dp.message_handler(state=AnketForm.theme)
async def process_theme(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['theme'] = message.text
    await message.answer("Есть ли у Вас дети?")
    await AnketForm.next()


@dp.message_handler(state=AnketForm.children)
async def process_children(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['children'] = message.text
    if data['children'].lower() != 'нет':
        await message.answer("Возраст ребенка (детей)")
        await AnketForm.next()
    else:
        await message.answer("Благодарим за заявку🌸")
        await state.finish()


@dp.message_handler(state=AnketForm.children_age)
async def process_children_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['children_age'] = message.text
        print(data)
    orders = Orders()
    orders.save_answer(message.from_user.id, message.from_user.username, data['name'], data['age'], data['theme'],
                       data['children'], data['children_age'])
    await message.answer("Спасибо за ответы!")
    await state.finish()


# //////////////////////////////////////////////////////////////////////////////////////

class AnketForm_2(StatesGroup):
    name = State()
    number = State()
    email = State()
    network = State()
    human = State()
    theme_2 = State()
    achievements = State()
    time = State()
    tool = State()
    tools = State()
    quantity = State()
    about = State()


# Обработчики состояний для класса Anket_2Form
@dp.message_handler(Text(equals='Заполнить заявку на волонтерство', ignore_case=True))
async def start_survey_2(message: types.Message):
    await bot.send_message(message.from_user.id, f'Для начала давайте познакомимся немного поближе, как Вас зовут? (ФИО)')
    await AnketForm_2.name.set()


@dp.message_handler(state=AnketForm_2.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('''Вау, какое красивое имя!🤍

Очень приятно познакомиться🤝

Ответьте пожалуйста всего на 10 вопросов для дальнейшего знакомства!🙏🏻''')
    await message.answer('''Ваш номер телефона для связи (формат: +79030000009)''')
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.number)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await message.answer("Электронная почта (формат почты: example@gmail.com)")
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer("Ссылки на Ваши соцсети (ник в телеграм, инстаграм, вк, сайт (если есть))")
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.network)
async def process_network(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['network'] = message.text
    await message.answer("Вы работаете  со  взрослыми  или  детьми?")
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.human)
async def process_human(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['human'] = message.text
    await message.answer('''Каким мастерством Вы владеете? (изобразительное искусство,  психология,  музыка, работа  с телом,   образование, анимация,  живопись,  музыка, произвольный ответ)
✨
Какие мастер-классы Вы предлагаете провести?''')
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.theme_2)
async def process_theme(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['theme'] = message.text
    await message.answer("Ваши регалии (при возможности прикрепите в сообщении дипломы, сертификаты, образование)")
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.achievements)
async def process_achievements(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['achievements'] = message.text
    await message.answer("Сколько по времени длится Ваше занятие?")
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.time)
async def process_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await message.answer("Нужны ли какие либо материалы или инструменты для проведения мастер-класса?")
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.tool)
async def process_tool(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tool'] = message.text
    await message.answer('''Если Вам необходимы материалы с нашей стороны для проведения мастер-класса, напишите, какие материалы и инструменты нужны для работы✨
Если нет нужды - ставьте «-»''')
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.tools)
async def process_tools(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tools'] = message.text
    await message.answer('''Сколько участников может принять ваш мастер-класс?''')
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await message.answer("О себе:")
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.about)
async def process_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text
        print(data)
    orders = Orders2()
    # user_id, username, name, number, email, network, theme, achievements, time, tool, tools, quantity, additional_info
    orders.save_answer(message.from_user.id, message.from_user.username, data['name'], data['number'], data['email'],
                       data['network'], data['human'], data['theme'],data['achievements'], data['time'], data['tool'], data['tools'],
                       data['quantity'], data['about'])
    await message.answer('''Благодарим за заявку🙏🏻
Будем рады сотрудничеству🤝
С Вами свяжется администратор💟''')
    await state.finish()


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, Text(equals='Помощь', ignore_case=True))
