from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but1 = KeyboardButton('Контакты')
but2 = KeyboardButton('Режим работы')
but3 = KeyboardButton('Тренировки')
but4 = KeyboardButton('Преподаватели')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(but1).add(but2).insert(but3).add(but4)

but1 = KeyboardButton('Супер')

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
