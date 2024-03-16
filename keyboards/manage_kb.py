from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but1 = KeyboardButton('Ученики')
but2 = KeyboardButton('Платежи')
but3 = KeyboardButton('Логи')

kb_manage_3 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manage_3.add(but1).add(but2).add(but3)