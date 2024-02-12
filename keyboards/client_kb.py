from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but1 = KeyboardButton('Помощь')
but2 = KeyboardButton('Моя подписка')
but3 = KeyboardButton('3')
but4 = KeyboardButton('4')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(but1).add(but2).insert(but3).add(but4)

but1 = KeyboardButton('Оплатить')

kb_client_1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_1.add(but1)

keyboard = types.InlineKeyboardMarkup()

# Добавляем кнопки на клавиатуру
button1 = types.InlineKeyboardButton(text="Бесплатный урок", callback_data="button1")
button2 = types.InlineKeyboardButton(text="Курс для новичков", callback_data="button2")
button3 = types.InlineKeyboardButton(text="Онлайн-клуб", callback_data="button3")
button4 = types.InlineKeyboardButton(text="Офлайн-клуб", callback_data="button4")
# Добавляем кнопки на клавиатуру в виде списка
keyboard.add(button1)
keyboard.add(button2)
keyboard.add(button3)
keyboard.add(button4)


back_keyboard = types.InlineKeyboardMarkup()
back_button = types.InlineKeyboardButton(text="Назад", callback_data="button5")
back_button_1 = types.InlineKeyboardButton(text="Купить подписку на месяц", callback_data="button6")
# Добавляем кнопки на клавиатуру в виде списка
back_keyboard.add(back_button).add(back_button_1)

