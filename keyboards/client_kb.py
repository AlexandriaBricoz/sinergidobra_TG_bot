from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки на клавиатуру
button1_start = KeyboardButton(text="Соцсети проекта", callback_data="tariff_1")
button2_start = KeyboardButton(text="Хочу на мастер-класс", callback_data="tariff_2")
button3_start = KeyboardButton(text="Заполнить заявку на волонтерство", callback_data="tariff_3")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_start.add(button1_start)
keyboard_start.add(button2_start)
keyboard_start.add(button3_start)
