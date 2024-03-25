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
            id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            svr_participation TEXT,
            svr_phone TEXT,
            svr_email TEXT,
            svr_telegram TEXT,
            svr_social TEXT,
            children TEXT,
            children_number TEXT,
            children_age TEXT
        )
        ''')
        self.connection.commit()

    def save_answer(self, user_id, username, name, age, theme, children, children_age):
        self.connection = sqlite3.connect("my_db_path.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "INSERT INTO answers (user_id, username, name, theme, children, children_age, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, name, theme, children, children_age, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def save_answers(self, user_id, username, name, age, theme, children, children_age):
        self.connection = sqlite3.connect("my_db_path.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "INSERT INTO answers (user_id, username, name, children, children_age, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            svr_phone TEXT,
            svr_email TEXT,
            svr_telegram TEXT,
            svr_social TEXT,
            activity TEXT,
            master_class_description TEXT,
            age_category TEXT,
            group_type TEXT,
            participant_count TEXT,
            free_classes_count TEXT)''')
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


Orders2()
