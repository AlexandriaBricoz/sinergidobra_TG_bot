from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but1 = KeyboardButton('Ученики')

kb_manage_3 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manage_3.add(but1)
