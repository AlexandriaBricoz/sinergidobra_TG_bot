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

keyboard_v = InlineKeyboardMarkup()

button_v = InlineKeyboardButton(text="Заполнить заявку на волонтерство",
                                callback_data="Заполнить заявку на волонтерство")
# Добавляем кнопки на клавиатуру в виде списка
keyboard_v.add(button_v)

keyboard_start_2 = InlineKeyboardMarkup()

button2_start_2 = InlineKeyboardButton(text="Хочу на мастер-класс", callback_data="Хочу на мастер-класс")
button3_start_2 = InlineKeyboardButton(text="Заполнить заявку на волонтерство",
                                       callback_data="Заполнить заявку на волонтерство")
# Добавляем кнопки на клавиатуру в виде списка
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

keyboard_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")],
        [KeyboardButton(text="🚫 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
keyboard_age = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Взрослые")],
        [KeyboardButton(text="Дети")],
        [KeyboardButton(text="🚫 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
keyboard_old = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="18-44")],
        [KeyboardButton(text="45-59")],
        [KeyboardButton(text="60-74")],
        [KeyboardButton(text="🚫 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
keyboard_young = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="0-7")],
        [KeyboardButton(text="8-12")],
        [KeyboardButton(text="13-18")],
        [KeyboardButton(text="🚫 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
# Keyboard layout for selecting number of children
keyboard_children_number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1")],
        [KeyboardButton(text="2")],
        [KeyboardButton(text="3")],
        [KeyboardButton(text="4-5")],
        [KeyboardButton(text="🚫 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
keyboard_activity = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Изобразительное искусство"), KeyboardButton(text="Психология")],
        [KeyboardButton(text="Музыка"), KeyboardButton(text="Работа с телом")],
        [KeyboardButton(text="Образование"), KeyboardButton(text="🚫 Отмена")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
keyboard_activity_2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Анимация"), KeyboardButton(text="Живопись")],
        [KeyboardButton(text="Музыка"), KeyboardButton(text="Образование")],
        [KeyboardButton(text="🚫 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_group_type = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Индивидуальные"), KeyboardButton(text="Групповые")],
        [KeyboardButton(text="Индивидуальные и групповые")],
        [KeyboardButton(text="🚫 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
