from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from create_bot import bot, dp
from keyboards.client_kb import keyboard_next, keyboard_start_2, keyboard_start, keyboard_cancel, keyboard_cancel_age
from loging import printl
from order_DB import Orders, Orders2

"""Хендлеры для взаимодействия с клиентом

    group_id:-1002030571529
    
    Иван Неретин 1085385124
"""

from aiogram.dispatcher.filters.state import StatesGroup, State


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    print(message.from_user.id, message.from_user.full_name, message.from_user.username)
    printl(message.from_user.id, message.from_user.full_name, message.from_user.username)
    photo = open('photo_2024-03-23 20.04.59.jpeg', 'rb')
    await bot.send_photo(message.from_user.id, photo=photo, caption=f'''Наш проект «Содружество Сердец»🇷🇺 направлен на создание общественной поддержки жен военнослужащих, участников СВО, создание условий для повышения социально-психологической поддержки семей участников СВО и вовлечение их на мастер-классы, кураторство, психологические консультации.

Сайт: https://sinergidobra.ru/

Инстаграм проекта «Синергия Добра»: https://www.instagram.com/sinergidobra?igsh=NDUyb3AwbGYyOXFq

Телеграм-канал проекта «Синергия Добра»: https://t.me/sinergidobra''')

    await bot.send_message(message.from_user.id,
                           f'''Приветствуем вас! Пожалуйста, ознакомьтесь с нашими правилами использования перед тем, как продолжить:
https://sinergidobra.ru/privacy
                           
Если вы продолжаете, вы подтверждаете, что ознакомились с нашим пользовательским соглашением и согласны с его условиями.''',
                           reply_markup=keyboard_next)


@dp.message_handler(Text(equals='🔝 Главное Меню', ignore_case=True))
async def main(message: types.Message):
    photo = open('photo_2024-03-23 20.04.59.jpeg', 'rb')
    await bot.send_photo(message.from_user.id, photo=photo, caption=f'''Наш проект «Содружество Сердец»🇷🇺 направлен на создание общественной поддержки жен военнослужащих, участников СВО, создание условий для повышения социально-психологической поддержки семей участников СВО и вовлечение их на мастер-классы, кураторство, психологические консультации.

Сайт: https://sinergidobra.ru/

Инстаграм проекта «Синергия Добра»: https://www.instagram.com/sinergidobra?igsh=NDUyb3AwbGYyOXFq

Телеграм-канал проекта «Синергия Добра»: https://t.me/sinergidobra''', reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id,
                           f'''Если Вы хотите заполнить заявку на волонтерство, напишите боту - заполнить заявку на волонтерство

Если Вы хотели бы участвовать в мастер классе, напишите боту - хочу на мастер-класс''',
                           reply_markup=keyboard_start_2)


@dp.message_handler(Text(equals='🔙 Назад', ignore_case=True))
async def back(message: types.Message):
    await main(message)


@dp.message_handler(Text(equals='Продолжить', ignore_case=True))
async def get_contacts(message: types.Message):
    sent_message = await bot.send_message(message.from_user.id,'Супер', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, sent_message.message_id)
    await bot.send_message(message.from_user.id,
                           f'''Если Вы хотите заполнить заявку на волонтерство, напишите боту - заполнить заявку на волонтерство

Если Вы хотели бы участвовать в мастер классе, напишите боту - хочу на мастер-класс''',
                           reply_markup=keyboard_start_2)
    printl(message.from_user.id, message.from_user.username, message.from_user.full_name)


@dp.message_handler(Text(equals='Соцсети проекта', ignore_case=True))
async def get_contacts(message: types.Message):
    await bot.send_message(message.from_user.id, f'''Познакомиться с проектом «Синергия Добра »🫶🏻🇷🇺

Сайт: https://sinergidobra.ru/

Телеграм-канал проекта «Синергия Добра»: https://t.me/sinergidobra''', )


@dp.message_handler(Text(equals='Служба заботы', ignore_case=True))
async def get_contact(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '''Если у Вас возникли вопросы, напишите, пожалуйста, администратору''')
    await bot.send_message(message.from_user.id,
                           f'@darezeda')


@dp.callback_query_handler(lambda c: c.data.startswith(''))
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    if data == "Соцсети проекта":
        await get_contacts(callback_query)
    elif data == "Хочу на мастер-класс":
        await course_for_beginners(callback_query)
    elif data == "Заполнить заявку на волонтерство":
        await start_survey(callback_query)


class AnketForm(StatesGroup):
    name = State()
    age = State()
    theme = State()
    children = State()
    children_age = State()


@dp.message_handler(Text(equals='Хочу на мастер-класс', ignore_case=True))
async def course_for_beginners(message: types.Message):
    await bot.send_message(message.from_user.id, f'ФИО', reply_markup=keyboard_cancel)
    await AnketForm.name.set()


@dp.message_handler(Text(equals='хочу на мастер-класс', ignore_case=True))
async def course_for_beginners_2(message: types.Message):
    await bot.send_message(message.from_user.id, f'ФИО', reply_markup=keyboard_cancel)
    await AnketForm.name.set()


@dp.message_handler(state=AnketForm.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Возраст", reply_markup=keyboard_cancel)
    await AnketForm.next()


@dp.message_handler(state=AnketForm.age)
async def process_age(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer("Желаемая тема мастер-класса", reply_markup=keyboard_cancel)
    await AnketForm.next()


@dp.message_handler(state=AnketForm.theme)
async def process_theme(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    async with state.proxy() as data:
        data['theme'] = message.text
    await message.answer("Есть ли у Вас дети?", reply_markup=keyboard_cancel)
    await AnketForm.next()


@dp.message_handler(state=AnketForm.children)
async def process_children(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    async with state.proxy() as data:
        data['children'] = message.text
    if data['children'].lower() != 'нет':
        await message.answer("Возраст ребенка (детей)", reply_markup=keyboard_cancel)
        await AnketForm.next()
    else:
        await message.answer("Благодарим за заявку🌸")
        await state.finish()


@dp.message_handler(state=AnketForm.children_age)
async def process_children_age(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    async with state.proxy() as data:
        data['children_age'] = message.text
        print(data)
    orders = Orders()
    orders.save_answer(message.from_user.id, message.from_user.username, data['name'], data['age'], data['theme'],
                       data['children'], data['children_age'])
    await message.answer("Спасибо за ответы!", reply_markup=keyboard_start)
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
async def start_survey(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Для начала давайте познакомимся немного поближе, как Вас зовут? (ФИО)',
                           reply_markup=keyboard_cancel)
    await AnketForm_2.name.set()


@dp.message_handler(Text(equals='заполнить заявку на волонтерство', ignore_case=True))
async def start_survey_2(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Для начала давайте познакомимся немного поближе, как Вас зовут? (ФИО)',
                           reply_markup=keyboard_cancel)
    await AnketForm_2.name.set()


@dp.message_handler(state=AnketForm_2.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('''Вау, какое красивое имя!🤍

Очень приятно познакомиться🤝

Ответьте пожалуйста всего на 10 вопросов для дальнейшего знакомства!🙏🏻''')
    await message.answer('''Ваш номер телефона для связи (формат: +79030000009)''', reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.number)
async def process_number(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['number'] = message.text
    await message.answer("Электронная почта (формат почты: example@gmail.com)", reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.email)
async def process_email(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer("Ссылки на Ваши соцсети (ник в телеграм, инстаграм, вк, сайт (если есть))",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.network)
async def process_network(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['network'] = message.text
    await message.answer("Вы работаете  со  взрослыми  или  детьми?", reply_markup=keyboard_cancel_age)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.human)
async def process_human(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return

    if message.text.lower() not in ["взрослые", "дети"]:
        await message.answer("❌ Ответ не из списка.\n\n🔄 Попробуйте еще раз…", reply_markup=keyboard_cancel_age)
        await state.set_state(AnketForm_2.human)
        return

    async with state.proxy() as data:
        data['human'] = message.text
    await message.answer('''Каким мастерством Вы владеете? (изобразительное искусство,  психология,  музыка, работа  с телом,   образование, анимация,  живопись,  музыка, произвольный ответ)
✨
Какие мастер-классы Вы предлагаете провести?''', reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.theme_2)
async def process_theme(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['theme'] = message.text
    await message.answer("Ваши регалии (при возможности прикрепите в сообщении дипломы, сертификаты, образование)",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.achievements)
async def process_achievements(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['achievements'] = message.text
    await message.answer("Сколько по времени длится Ваше занятие?", reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.time)
async def process_time(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['time'] = message.text
    await message.answer("Нужны ли какие либо материалы или инструменты для проведения мастер-класса?",
                         reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.tool)
async def process_tool(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['tool'] = message.text
    await message.answer('''Если Вам необходимы материалы с нашей стороны для проведения мастер-класса, напишите, какие материалы и инструменты нужны для работы✨
Если нет нужды - ставьте «-»''', reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.tools)
async def process_tools(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['tools'] = message.text
    await message.answer('''Сколько участников может принять ваш мастер-класс?''', reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['quantity'] = message.text
    await message.answer("О себе:", reply_markup=keyboard_cancel)
    await AnketForm_2.next()


@dp.message_handler(state=AnketForm_2.about)
async def process_about(message: types.Message, state: FSMContext):
    if message.text.lower() == "🚫 отмена":
        await state.finish()
        await main(message)
        return
    async with state.proxy() as data:
        data['about'] = message.text
        print(data)
    orders = Orders2()
    # user_id, username, name, number, email, network, theme, achievements, time, tool, tools, quantity, additional_info
    orders.save_answer(message.from_user.id, message.from_user.username, data['name'], data['number'], data['email'],
                       data['network'], data['human'], data['theme'], data['achievements'], data['time'], data['tool'],
                       data['tools'],
                       data['quantity'], data['about'])
    await message.answer('''Благодарим за заявку🙏🏻
Будем рады сотрудничеству🤝
С Вами свяжется администратор💟''', reply_markup=keyboard_start)
    await state.finish()


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(start_survey, commands=['volunteering'])
    dp.register_message_handler(course_for_beginners, commands=['master_class'])
    dp.register_message_handler(get_contacts, commands=['networks'])
