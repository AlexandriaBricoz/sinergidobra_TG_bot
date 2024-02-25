from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but1 = KeyboardButton('Помощь')
but2 = KeyboardButton('Моя подписка')
but3 = KeyboardButton('Тарифные планы')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(but1).add(but2).insert(but3)

but1 = KeyboardButton('Оплатить')

kb_client_1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_1.add(but1)

keyboard = types.InlineKeyboardMarkup()

# Добавляем кнопки на клавиатуру
button1 = types.InlineKeyboardButton(text="Бесплатный урок", callback_data="tariff_1")
button2 = types.InlineKeyboardButton(text="Курс для новичков", callback_data="tariff_2")
button3 = types.InlineKeyboardButton(text="Вступить в клуб", callback_data="tariff_3")
# Добавляем кнопки на клавиатуру в виде списка
keyboard.add(button1)
keyboard.add(button2)
keyboard.add(button3)

#######################################################################################################
back_keyboard_0 = types.InlineKeyboardMarkup()
back_button = types.InlineKeyboardButton(text="Назад", callback_data="tariff_0")
back_keyboard_0.add(back_button)

back_keyboard_1 = types.InlineKeyboardMarkup()
back_button_1 = types.InlineKeyboardButton(text="Познакомиться с курсом", callback_data="tariff_1_1")
# Добавляем кнопки на клавиатуру в виде списка
back_keyboard_1.add(back_button).add(back_button_1)

back_keyboard_2 = types.InlineKeyboardMarkup()
back_button_2_1 = types.InlineKeyboardButton(text="Купить курс за 1490", callback_data="tariff_2_1")
# Добавляем кнопки на клавиатуру в виде списка
back_keyboard_2.add(back_button).add(back_button_2_1)

back_keyboard_3 = types.InlineKeyboardMarkup()
back_button_3_1 = types.InlineKeyboardButton(text="Оплатить онлайн клуб на месяц 2800₽", callback_data="tariff_3_1")
back_button_3_2 = types.InlineKeyboardButton(text="Вступить в офлайн клуб", callback_data="tariff_3_2")
# Добавляем кнопки на клавиатуру в виде списка
back_keyboard_3.add(back_button).add(back_button_3_1).add(back_button_3_2)

pay_2 = types.InlineKeyboardMarkup()
pay_button_2 = types.InlineKeyboardButton(text="Оплатить 1490₽", callback_data="tariff_3_2_1")
# Добавляем кнопки на клавиатуру в виде списка
pay_2.add(pay_button_2)


pay_3_1 = types.InlineKeyboardMarkup()
pay_button_3_1 = types.InlineKeyboardButton(text="Оплатить", callback_data="tariff_3_1_1")
# Добавляем кнопки на клавиатуру в виде списка
pay_3_1.add(pay_button_3_1)

pay_3_2 = types.InlineKeyboardMarkup()
pay_button_3_2 = types.InlineKeyboardButton(text="Получить контакты", callback_data="tariff_3_2_1")
# Добавляем кнопки на клавиатуру в виде списка
pay_3_2.add(pay_button_3_2)
