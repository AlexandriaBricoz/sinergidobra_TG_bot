import sqlite3
from datetime import datetime


class Orders:

    # Функция для создания нового заказа
    def __init__(self):
        # Создание подключения к базе данных
        self.conn = sqlite3.connect('orders.db')
        # Создание подключения к базе данных
        self.conn = sqlite3.connect('orders.db')
        self.cursor = self.conn.cursor()

        # Создание таблицы заказов
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            order_id TEXT PRIMARY KEY,
                            user_id INTEGER,
                            username TEXT,
                            full_name TEXT,
                            creation_date TEXT,
                            confirmation_date TEXT,
                            status TEXT,
                            article TEXT,
                            price INTEGER
                            )''')
        self.conn.commit()

    def create_order(self, order_id, user_id, username, full_name, article, price):
        self.conn = sqlite3.connect('orders.db')
        self.cursor = self.conn.cursor()

        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''INSERT INTO orders (order_id, user_id, username, full_name, creation_date, status, article, price)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
            order_id, user_id, username, full_name, creation_date, 'created', article, price))
        self.conn.commit()
        return self.cursor.lastrowid

    def check_order_payment(self, order_id):
        self.cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
        order_status = self.cursor.fetchone()

        if order_status[0] == "confirmed":
            return True
        else:
            return False

    # Функция для получения заказов одного пользователя
    def get_user_orders(self, user_id):
        self.cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    # Функция для получения всех заказов
    def get_all_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        return self.cursor.fetchall()

    # Функция для удаления заказа по его ID
    def delete_order(self, order_id):
        self.cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        self.conn.commit()

    # Функция для удаления всех заказов одного пользователя
    def delete_all_user_orders(self, user_id):
        self.cursor.execute("DELETE FROM orders WHERE user_id = ?", (user_id,))
        self.conn.commit()

    # Функция для подтверждения заказа по его ID
    def confirm_order(self, order_id):
        print('conf ',order_id)
        confirmation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''UPDATE orders SET confirmation_date = ?, status = ? WHERE order_id = ?''',
                            (confirmation_date, 'confirmed', order_id))
        self.conn.commit()

    def get_unconfirmed_orders(self):
        self.cursor.execute("SELECT * FROM orders WHERE status != 'confirmed'")
        return self.cursor.fetchall()


# orders = Orders()

# orders.create_order('wwedwerceed322', 122133, '@example_user', 'John Doe', 'ART123', 100.0)
# print(orders.get_all_orders())
# print(orders.get_unconfirmed_orders())

# # Пример использования функций
# order_id = orders.create_order(122133, '@example_user', 'John Doe', 'ART123', 100.0, 110.0,
#                                'http://example.com/product123')
# print("Создан новый заказ с ID:", order_id)
#
# # Получение заказов одного пользователя
# user_orders = orders.get_user_orders(123)
# print("Заказы пользователя с ID 123:", user_orders)
#
# # Получение всех заказов
# all_orders = orders.get_all_orders()
# print("Все заказы:", all_orders)
#
# # Удаление заказа
# orders.delete_order(order_id)
# print("Заказ с ID", order_id, "удален.")
#
# # Удаление всех заказов одного пользователя
# orders.delete_all_user_orders(122133)
# print("Все заказы пользователя с ID 123 удалены.")
#
# # Закрытие соединения с базой данных
# orders.conn.close()
