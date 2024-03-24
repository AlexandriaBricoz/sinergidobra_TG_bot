import sqlite3
from datetime import datetime


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
            children TEXT,
            children_age TEXT,
            date TEXT
        )
        ''')
        self.connection.commit()

    def save_answer(self, user_id, username, name, age, theme, children, children_age):
        self.connection = sqlite3.connect("my_db_path.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "INSERT INTO answers (user_id, username, name, age, theme, children, children_age, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, name, age, theme, children, children_age, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_all_orders(self):
        self.cursor.execute("SELECT * FROM answers")
        return self.cursor.fetchall()


class Orders2:

    # Функция для создания нового заказа
    def __init__(self):
        # Создание подключения к базе данных
        self.connection = sqlite3.connect("my_db_path_2.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS answers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id TEXT,
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
             about TEXT,
             date)''')
        self.connection.commit()

    def save_answer(self, user_id, username, name, number, email, network, human, theme, achievements, time, tool,
                    tools,
                    quantity, about):
        self.connection = sqlite3.connect("my_db_path_2.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''INSERT INTO answers (user_id, username, name, number, email, network, human, theme, achievements, time, tool, tools, quantity, about, date)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, username, name, number, email, network, human, theme, achievements, time, tool, tools, quantity,
             about, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_all_orders(self):
        self.cursor.execute("SELECT * FROM answers")
        return self.cursor.fetchall()


Orders()
Orders2()
