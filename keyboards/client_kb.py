from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки на клавиатуру
button1_start = KeyboardButton(text="Соцсети проекта")
button2_start = KeyboardButton(text="Хочу на мастер-класс")
button3_start = KeyboardButton(text="Заполнить заявку на волонтерство")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_start.add(button1_start)
keyboard_start.add(button2_start)
keyboard_start.add(button3_start)

keyboard_next = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки на клавиатуру
button1_next = KeyboardButton(text="Продолжить")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_next.add(button1_next)
