from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки на клавиатуру
button1_start = KeyboardButton(text="Служба заботы")
button2_start = KeyboardButton(text="🔙 Назад")
button3_start = KeyboardButton(text="🔝 Главное Меню")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_start.add(button1_start)
keyboard_start.add(button2_start, button3_start)

keyboard_next = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки на клавиатуру
button1_next = KeyboardButton(text="Продолжить")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_next.add(button1_next)

keyboard_start_2 = InlineKeyboardMarkup()

button1_start_2 = InlineKeyboardButton(text="Соцсети проекта", callback_data="Соцсети проекта")
button2_start_2 = InlineKeyboardButton(text="Хочу на мастер-класс", callback_data="Хочу на мастер-класс")
button3_start_2 = InlineKeyboardButton(text="Заполнить заявку на волонтерство",
                                       callback_data="Заполнить заявку на волонтерство")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_start_2.add(button1_start_2)
keyboard_start_2.add(button2_start_2)
keyboard_start_2.add(button3_start_2)


keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки на клавиатуру
button1_cancel = KeyboardButton(text="🚫 Отмена")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_cancel.add(button1_cancel)

keyboard_cancel_age = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки на клавиатуру
button1_cancel_age = KeyboardButton(text="Взрослые")
button2_cancel_age = KeyboardButton(text="Дети")
button3_cancel_age = KeyboardButton(text="🚫 Отмена")

# Добавляем кнопки на клавиатуру в виде списка
keyboard_cancel_age.add(button1_cancel_age).add(button2_cancel_age).add(button3_cancel_age)