import re
import sqlite3

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from create_bot import bot, dp
from keyboards.client_kb import keyboard_next, keyboard_start_2, keyboard_cancel, keyboard_yes_no, \
    keyboard_children_number, keyboard_group_type, keyboard_activity, keyboard_age, keyboard_activity_2, keyboard_young, \
    keyboard_old, keyboard_v
from loging import printl

"""Хендлеры для взаимодействия с клиентом

    group_id:-1002030571529
    
    870903130 Старухина Анна arumitapro
    
    6532995976 Синергия Добра synergidobra
    
    Иван Неретин 1085385124
"""

from aiogram.dispatcher.filters.state import StatesGroup, State


# Функция для проверки валидности ФИО
def is_valid_name(name):
    # Паттерн для проверки ФИО: только буквы и пробелы, как минимум два слова
    pattern = r'^[a-zA-Zа-яА-ЯёЁ]+\s[a-zA-Zа-яА-ЯёЁ]+(\s[a-zA-Zа-яА-ЯёЁ]+)?$'
    return bool(re.match(pattern, name))


# Функция для проверки валидности номера телефона
def is_valid_phone(phone):
    # Паттерн для проверки номера телефона в формате +7XXXXXXXXXX или 8XXXXXXXXXX
    pattern = r'^(?:\+7|8)\d{10}$'
    return bool(re.match(pattern, phone))


# Функция для проверки валидности email
def is_valid_email(email):
    # Паттерн для проверки email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    print(message.from_user.id, message.from_user.full_name, message.from_user.username)
    printl(message.from_user.id, message.from_user.full_name, message.from_user.username)
    photo = open('photo_2024-03-23 20.04.59.jpeg', 'rb')
    await bot.send_photo(message.from_user.id, photo=photo, caption=f'''<b>Синергия добра</b> приветствует Вас. 
Мы создаем сообщество, в котором объединяем людей, желающих поддержать женщин и детей наших бойцов.
''', parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.from_user.id,
                           f'''Я виртуальный помощник <b>Синергии добра</b>! Чтобы добавить Вас в наше сообщество, задам несколько вопросов, это займет у вас не более 5 минут. ''',
                           parse_mode=types.ParseMode.HTML,
                           reply_markup=keyboard_next)  # ReplyKeyboardRemove


#     await bot.send_message(message.from_user.id,
#                            f'''Пожалуйста, ознакомьтесь с нашими правилами использования перед тем, как продолжить:
# https://sinergidobra.ru/privacy
#
# Если вы продолжаете, вы подтверждаете, что ознакомились с нашим пользовательским соглашением и согласны с его условиями.''',
#                            parse_mode=types.ParseMode.HTML,
#                            reply_markup=keyboard_next)


@dp.message_handler(Text(equals='🔝 Главное Меню', ignore_case=True))
async def main(message: types.Message):
    photo = open('photo_2024-03-23 20.04.59.jpeg', 'rb')
    await bot.send_photo(message.from_user.id, photo=photo,
                         caption='''Я виртуальный помощник <b>Синергии добра</b>! Чтобы добавить Вас в наше сообщество, задам несколько вопросов, это займет у вас не более 5 минут. ''',
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id,
                           f'''Если Вы хотите заполнить заявку на волонтерство, напишите боту - заполнить заявку на волонтерство.

Если Вы хотели бы участвовать в мастер классе, напишите боту - хочу на мастер-класс.''',
                           reply_markup=keyboard_start_2)


@dp.message_handler(Text(equals='🔙 Назад', ignore_case=True))
async def back(message: types.Message):
    await main(message)


@dp.message_handler(Text(equals='Продолжить', ignore_case=True))
async def get_contacts(message: types.Message):
    sent_message = await bot.send_message(message.from_user.id, 'Супер', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, sent_message.message_id)
    await bot.send_message(message.from_user.id,
                           f'''Если Вы хотите заполнить заявку на волонтерство, напишите боту - заполнить заявку на волонтерство.

Если Вы хотели бы участвовать в мастер классе, напишите боту - хочу на мастер-класс.''',
                           reply_markup=keyboard_start_2)
    printl(message.from_user.id, message.from_user.username, message.from_user.full_name)


@dp.message_handler(Text(equals='Соцсети проекта', ignore_case=True))
async def get_contacts(message: types.Message):
    await bot.send_message(message.from_user.id, f'''Познакомиться с проектом «<b>Синергия Добра</b>»🫶🏻🇷🇺

Сайт: https://sinergidobra.ru/

Телеграм-канал проекта «<b>Синергия Добра</b>»: https://t.me/sinergidobra''', parse_mode=types.ParseMode.HTML, )


@dp.message_handler(Text(equals='Служба заботы', ignore_case=True))
async def get_contact(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '''Если у Вас возникли вопросы, напишите, пожалуйста, администратору.''')
    await bot.send_message(message.from_user.id,
                           f'@synergidobra')


@dp.callback_query_handler(lambda c: c.data.startswith(''))
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    if data == "Соцсети проекта":
        await get_contacts(callback_query)
    elif data == "Хочу на мастер-класс":
        await start_survey_22(callback_query)
    elif data == "Заполнить заявку на волонтерство":
        await start_survey(callback_query)


class AnketForm(StatesGroup):
    name = State()
    svr_participation = State()
    svr_phone = State()
    svr_email = State()
    svr_date_born = State()
    svr_address = State()
    svr_social = State()
    children = State()
    children_number = State()
    children_age = State()
    about = State()


@dp.message_handler(Text(equals='Хочу на мастер-класс', ignore_case=True))
async def start_survey_22(message: types.Message):
    await bot.send_message(message.from_user.id, "Давайте знакомиться!\nКак Вас зовут? (ФИО)",
                           reply_markup=keyboard_cancel)
    await AnketForm.name.set()


@dp.message_handler(Text(equals='xочу на мастер-класс', ignore_case=True))
async def start_survey_222(message: types.Message):
    await bot.send_message(message.from_user.id, "Давайте знакомиться!\nКак Вас зовут? (ФИО)",
                           reply_markup=keyboard_cancel)
    await AnketForm.name.set()


# Asking for name
@dp.message_handler(state=AnketForm.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data.update({
            'name': message.text,
            'svr_participation': None,
            'svr_phone': None,
            'svr_email': None,
            'svr_date_born': None,
            'svr_address': None,
            'svr_social': None,
            'children': None,
            'children_number': None,
            'children_age': None,
            'about': None
        })
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    if not is_valid_name(message.text.lower()):
        await message.answer("Вы ввели некорректные данные. Попробуйте снова.", reply_markup=keyboard_cancel)
        await state.set_state(AnketForm.name)
        return

    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id,
                           f"Приятно познакомиться!\n"
                           "Впереди несколько вопросов, они пролетят незаметно. Поехали!")

    await bot.send_message(message.from_user.id, "Участвует ли член вашей семьи в СВО?", reply_markup=keyboard_yes_no)
    await AnketForm.next()


# Asking SVR participation
@dp.message_handler(state=AnketForm.svr_participation)
async def process_svr_participation(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    if message.text.lower() not in ["да", "нет"]:
        await message.answer("❌ Ответ не из списка.\n\n🔄 Попробуйте еще раз…", reply_markup=keyboard_yes_no)
        await state.set_state(AnketForm.svr_participation)
        return

    svr_participation = message.text.lower() == 'да'
    await state.update_data(svr_participation=svr_participation)
    async with state.proxy() as data:
        data['svr_participation'] = message.text
    if svr_participation:

        await message.answer("Ну а теперь несколько вопросов о Вашем участии в благотворительном проекте:")

        await message.answer("Напишите Ваш номер телефона для связи (формат: +79030000009).",
                             reply_markup=keyboard_cancel)
        await AnketForm.svr_phone.set()
    else:
        await save_data_to_database(state, message)
        await message.answer('''Благодарим за заявку! 🌸
В таком случае Вы можете поучаствовать в проекте в качестве волонтера. У Вас есть возможность заполнить заявку на волонтера.''',
                             reply_markup=keyboard_v)
        await state.finish()


# Asking for SVR phone
@dp.message_handler(state=AnketForm.svr_phone)
async def process_svr_phone(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    if not is_valid_phone(message.text.lower()):
        await message.answer("Вы ввели некорректные данные. Попробуйте снова.", reply_markup=keyboard_cancel)
        await state.set_state(AnketForm.svr_phone)
        return
    async with state.proxy() as data:
        data['svr_phone'] = message.text
    await state.update_data(svr_phone=message.text)
    await bot.send_message(message.from_user.id, "А также Вашу электронную почту (Формат почты: example@gmail.com).",
                           reply_markup=keyboard_cancel)
    await AnketForm.svr_email.set()


# Asking for SVR email
@dp.message_handler(state=AnketForm.svr_email)
async def process_svr_email(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    if not is_valid_email(message.text.lower()):
        await message.answer("Вы ввели некорректные данные. Попробуйте снова.", reply_markup=keyboard_cancel)
        await state.set_state(AnketForm.svr_email)
        return
    async with state.proxy() as data:
        data['svr_email'] = message.text
    await state.update_data(svr_email=message.text)
    await bot.send_message(message.from_user.id, "Теперь просим вписать Ваш город проживания.",
                           reply_markup=keyboard_cancel)
    await AnketForm.svr_address.set()


# Asking for SVR telegram
@dp.message_handler(state=AnketForm.svr_address)
async def process_svr_address(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['svr_address'] = message.text
    await state.update_data(svr_address=message.text)
    await bot.send_message(message.from_user.id, "Дата рождения.",
                           reply_markup=keyboard_cancel)
    await AnketForm.svr_date_born.set()


@dp.message_handler(state=AnketForm.svr_date_born)
async def process_svr_date_born(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['svr_date_born'] = message.text
    await state.update_data(svr_date_born=message.text)
    await bot.send_message(message.from_user.id, "По желанию вы можете поделиться ссылками на Ваши соцсети (вк, сайт).",
                           reply_markup=keyboard_cancel)
    await AnketForm.svr_social.set()


# Asking for SVR social
@dp.message_handler(state=AnketForm.svr_social)
async def process_svr_social(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['svr_social'] = message.text
    await state.update_data(svr_social=message.text)
    await message.answer("Есть ли у Вас дети?", reply_markup=keyboard_yes_no)
    await AnketForm.children.set()


# Asking for children
@dp.message_handler(state=AnketForm.children)
async def process_children(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    if message.text.lower() not in ["да", "нет"]:
        await message.answer("❌ Ответ не из списка.\n\n🔄 Попробуйте еще раз…", reply_markup=keyboard_yes_no)
        await state.set_state(AnketForm.children)
        return
    children = message.text.lower() == 'да'

    async with state.proxy() as data:
        data['children'] = message.text
        print(data['children'])
    await state.update_data(children=children)

    if children:
        await message.answer("Сколько у вас детей?", reply_markup=keyboard_children_number)
        await AnketForm.children_number.set()
    else:
        await save_data_to_database(state, message)
        await message.answer("Благодарим за заявку! 🌸")
        await state.finish()

@dp.message_handler(state=AnketForm.children)
async def process_children(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    if message.text.lower() not in ["да", "нет"]:
        await message.answer("❌ Ответ не из списка.\n\n🔄 Попробуйте еще раз…", reply_markup=keyboard_yes_no)
        await state.set_state(AnketForm.children)
        return
    children = message.text.lower() == 'да'

    async with state.proxy() as data:
        data['children'] = message.text
        print(data['children'])
    await state.update_data(children=children)

    if children:
        await message.answer("Сколько у вас детей?", reply_markup=keyboard_children_number)
        await AnketForm.children_number.set()
    else:
        await save_data_to_database(state, message)
        await message.answer("Благодарим за заявку! 🌸")
        await state.finish()


# Asking for children number
@dp.message_handler(state=AnketForm.children_number)
async def process_children_number(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    async with state.proxy() as data:
        data['children_number'] = message.text

    await state.update_data(children_number=message.text)
    await message.answer(
        "Дата рождения детей (пример: ребенок 1: 01.02.2009, ребенок 2: 05.06.2017 последовательно через запятую)")
    await AnketForm.children_age.set()

@dp.message_handler(state=AnketForm.children_age)
async def process_children_age(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    async with state.proxy() as data:
        data['children_age'] = message.text

    await state.update_data(children_number=message.text)
    await message.answer(
        """Последний вопрос
О себе: (Ваша профессия, хобби, увлечения)""")
    await AnketForm.about.set()

# Asking for children age
@dp.message_handler(state=AnketForm.about)
async def process_about(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['about'] = message.text
    await state.update_data(children_age=message.text)
    await message.answer("Благодарим за заявку🙏🏻\n"
                         "Будем рады видеть Вас на мероприятии!\n"
                         "С Вами свяжется администратор💟")

    await save_data_to_database(state, message)
    await state.finish()


# //////////////////////////////////////////////////////////////////////////////////////

class AnketForm_2(StatesGroup):
    name = State()
    svr_phone = State()
    svr_email = State()
    svr_telegram = State()
    svr_social = State()
    activity = State()
    activity_type_adults = State()
    activity_type_children = State()
    master_class_description = State()
    age_category = State()
    group_type = State()
    participant_count = State()
    free_classes_count = State()


# Start conversation
@dp.message_handler(Text(equals='Заполнить заявку на волонтерство', ignore_case=True))
async def start_survey(message: types.Message):
    await bot.send_message(message.from_user.id, "Давайте знакомиться!\nКак Вас зовут? (ФИО)",
                           reply_markup=keyboard_cancel)
    await AnketForm_2.name.set()


@dp.message_handler(Text(equals='заполнить заявку на волонтерство', ignore_case=True))
async def start_survey33(message: types.Message):
    await bot.send_message(message.from_user.id, "Давайте знакомиться!\nКак Вас зовут? (ФИО)",
                           reply_markup=keyboard_cancel)
    await AnketForm_2.name.set()


# Asking for name
@dp.message_handler(state=AnketForm_2.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    if not is_valid_name(message.text.lower()):
        await message.answer("Вы ввели некорректные данные. Попробуйте снова.", reply_markup=keyboard_cancel)
        await state.set_state(AnketForm_2.name)
        return

    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer(f"Приятно познакомиться!\n"
                         "Впереди всего 10 вопросов, они пролетят незаметно. Поехали!")

    await message.answer("Напишите Ваш номер телефона для связи (формат: +79030000009).",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.svr_phone.set()


# Asking for phone number
@dp.message_handler(state=AnketForm_2.svr_phone)
async def process_phone(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)

    if not is_valid_phone(message.text.lower()):
        await message.answer("Вы ввели некорректные данные. Попробуйте снова.", reply_markup=keyboard_cancel)
        await state.set_state(AnketForm_2.svr_phone)
        return

    async with state.proxy() as data:
        data['svr_phone'] = message.text

    await message.answer("А также Вашу электронную почту (Формат почты: example@gmail.com).",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.svr_email.set()


# Asking for email
@dp.message_handler(state=AnketForm_2.svr_email)
async def process_email(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    if not is_valid_email(message.text.lower()):
        await message.answer("Вы ввели некорректные данные. Попробуйте снова.", reply_markup=keyboard_cancel)
        await state.set_state(AnketForm_2.svr_email)
        return
    async with state.proxy() as data:
        data['svr_email'] = message.text

    await message.answer("Тут просим вписать Ваш ник в телеграм.",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.svr_telegram.set()


# Asking for telegram nickname
@dp.message_handler(state=AnketForm_2.svr_telegram)
async def process_telegram(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['svr_telegram'] = message.text

    await message.answer("По желанию вы можете поделиться ссылками на Ваш проект, сайт или соцсети (вк, сайт).",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.svr_social.set()


# Asking for social links
@dp.message_handler(state=AnketForm_2.svr_social)
async def process_social(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['svr_social'] = message.text

    await message.answer("Ну а теперь пять вопросов о Вашем участии в благотворительном проекте:",
                         reply_markup=keyboard_cancel)

    await message.answer("Вы работаете со взрослыми или детьми?", reply_markup=keyboard_age)
    await AnketForm_2.activity.set()


# Asking for activity
@dp.message_handler(state=AnketForm_2.activity)
async def process_activity(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    if message.text.lower() not in ["взрослые", "дети"]:
        await message.answer("❌ Ответ не из списка.\n\n🔄 Попробуйте еще раз…", reply_markup=keyboard_age)
        await state.set_state(AnketForm_2.activity)
        return
    async with state.proxy() as data:
        if message.text.lower() == 'взрослые':
            data['svr_participation'] = 'взрослые'
            await message.answer("Ваш род деятельности (со взрослыми)?", reply_markup=keyboard_activity)
            await AnketForm_2.activity_type_adults.set()
        else:
            data['svr_participation'] = 'дети'
            await message.answer("Ваш род деятельности (с детьми)?", reply_markup=keyboard_activity_2)
            await AnketForm_2.activity_type_children.set()


# Asking for activity type with adults
@dp.message_handler(state=AnketForm_2.activity_type_adults)
async def process_activity_type_adults(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['activity'] = message.text

    await message.answer('''Какие мастер-классы вы предлагаете провести и какие навыки участники смогут получить?
    
Совсем коротко опишите что вы делаете на ваших занятиях. Чтобы нам лучше узнать ваше направление.''',
                         reply_markup=keyboard_cancel)
    await AnketForm_2.master_class_description.set()


# Asking for activity type with children
@dp.message_handler(state=AnketForm_2.activity_type_children)
async def process_activity_type_children(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['activity'] = message.text

    await message.answer("Какие мастер-классы вы предлагаете провести и какие навыки участники смогут получить?",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.master_class_description.set()


# Asking for master class description
@dp.message_handler(state=AnketForm_2.master_class_description)
async def process_master_class_description(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['master_class_description'] = message.text
        if data['svr_participation'] == 'взрослые':
            await message.answer("Возрастная категория участников?",
                                 reply_markup=keyboard_old)
        else:
            await message.answer("Возрастная категория участников?",
                                 reply_markup=keyboard_young)
    await AnketForm_2.age_category.set()


# Asking for age category
@dp.message_handler(state=AnketForm_2.age_category)
async def process_age_category(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['age_category'] = message.text

    await message.answer("Занятия индивидуальные или групповые?", reply_markup=keyboard_group_type)
    await AnketForm_2.group_type.set()


# Asking for group type
@dp.message_handler(state=AnketForm_2.group_type)
async def process_group_type(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['group_type'] = message.text
        if data['group_type'].lower() == 'индивидуальные':
            data['participant_count'] = '1'
            await message.answer("Сколько мастер-классов в месяц вы готовы провести на безвозмездной основе?",
                                 reply_markup=keyboard_cancel)
            await AnketForm_2.free_classes_count.set()
        else:
            await message.answer("Сколько участников может принять ваш мастер-класс?",
                                 reply_markup=keyboard_cancel)
            await AnketForm_2.participant_count.set()


# Asking for participant count
@dp.message_handler(state=AnketForm_2.participant_count)
async def process_participant_count(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['participant_count'] = message.text

    await message.answer("Сколько мастер-классов в месяц вы готовы провести на безвозмездной основе?",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.free_classes_count.set()


# Asking for free classes count
@dp.message_handler(state=AnketForm_2.free_classes_count)
async def process_free_classes_count(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['free_classes_count'] = message.text

    # Saving data to the database
    await save_user_data_2(state, message)

    # Sending completion message
    await message.answer("Благодарим за заявку🙏🏻\n"
                         "Будем рады сотрудничеству🤝\n"
                         "С Вами свяжется администратор💟")
    await state.finish()


async def save_data_to_database(state: FSMContext, message):
    async with state.proxy() as data:
        conn = sqlite3.connect('my_db_path.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO answers (user_id, nik_name, full_name, name, svr_participation, svr_phone, svr_email, svr_address,  svr_date_born,
                           svr_social, children, children_number, children_age, about) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (message.from_user.id, message.from_user.username, message.from_user.full_name, data['name'],
                        data['svr_participation'], data['svr_phone'], data['svr_email'],
                        data['svr_address'], data['svr_date_born'], data['svr_social'], data['children'],
                        data['children_number'],
                        data['children_age'], data['about']))
        conn.commit()
        conn.close()


async def save_user_data_2(state: FSMContext, message):
    async with state.proxy() as data:
        conn = sqlite3.connect('my_db_path_2.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_id, nik_name, full_name, name, svr_phone, svr_email, svr_telegram, svr_social, svr_participation,
                           activity, master_class_description, age_category, group_type,
                           participant_count, free_classes_count) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (message.from_user.id, message.from_user.username, message.from_user.full_name, data['name'],
                        data['svr_phone'], data['svr_email'], data['svr_telegram'], data['svr_social'],
                        data['svr_participation'],
                        data['activity'], data['master_class_description'],
                        data['age_category'], data['group_type'], data['participant_count'],
                        data['free_classes_count']))
        conn.commit()
        conn.close()


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(main, commands=['main'])
    dp.register_message_handler(start_survey, commands=['volunteering'])
    dp.register_message_handler(start_survey_22, commands=['master_class'])
    dp.register_message_handler(get_contacts, commands=['networks'])
    dp.register_message_handler(get_contact, commands=['care_service'])
