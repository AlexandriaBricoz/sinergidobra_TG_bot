from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but1 = KeyboardButton('Заявки на волонтёрство')
but2 = KeyboardButton('Заявки на мастер-класс')
but3 = KeyboardButton('Логи')

kb_manage_3 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manage_3.add(but1).add(but2).add(but3)


