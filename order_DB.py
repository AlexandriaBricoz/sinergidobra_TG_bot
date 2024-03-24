import sqlite3


class Orders:

    # Функция для создания нового заказа
    def __init__(self):
        # Создание подключения к базе данных
        self.connection = sqlite3.connect("my_db_path.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            name TEXT,
            age INTEGER,
            theme TEXT,
            children BOOLEAN,
            children_age INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.connection.commit()

    def save_answer(self, user_id, username, name, age, theme, children, children_age):
        self.connection = sqlite3.connect("my_db_path.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "INSERT INTO answers (user_id, username, name, age, theme, children, children_age) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, name, age, theme, children, children_age))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


class Orders2:

    # Функция для создания нового заказа
    def __init__(self):
        # Создание подключения к базе данных
        self.connection = sqlite3.connect("my_db_path_2.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS answers
             (user_id INTEGER PRIMARY KEY,
             username TEXT,
             name TEXT,
             number TEXT,
             email TEXT,
             network TEXT,
             human TEXT,
             theme TEXT,
             achievements TEXT,
             time TEXT,
             tool TEXT,
             tools TEXT,
             quantity TEXT,
             about TEXT)''')
        self.connection.commit()

    def save_answer(self, user_id, username, name, number, email, network, human, theme, achievements, time, tool,
                    tools,
                    quantity, about):
        self.connection = sqlite3.connect("my_db_path_2.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''INSERT INTO answers (user_id, username, name, number, email, network, human, theme, achievements, time, tool, tools, quantity, about)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, username, name, number, email, network, human, theme, achievements, time, tool, tools, quantity,
             about))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


Orders2()
