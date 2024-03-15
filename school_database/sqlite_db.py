import sqlite3
from datetime import datetime, timedelta


def create_table():
    # Подключаемся к базе данных (файлу)
    conn = sqlite3.connect('bot_sql.db')
    cursor = conn.cursor()

    # Создаем таблицу subscriptions
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        username TEXT,
                        full_name TEXT,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL
                      )''')
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


def add_subscription(user_id, username, full_name, start_date, end_date):
    try:
        # Подключаемся к базе данных (файлу)
        conn = sqlite3.connect('bot_sql.db')
        cursor = conn.cursor()

        # Проверяем, есть ли активная подписка для данного пользователя
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        existing_subscription = cursor.fetchone()

        if existing_subscription:
            # Если подписка существует, обновляем дату окончания
            _, _, _, _, current_start_date, current_end_date = existing_subscription
            new_end_date = datetime.strptime(current_end_date, "%Y-%m-%d") + timedelta(days=31)
            update_query = "UPDATE users SET end_date = ? WHERE user_id = ?"
            cursor.execute(update_query, (new_end_date.date(), user_id))
            print("Существующая подписка успешно продлена!")
        else:
            # Если подписка не существует, добавляем новую запись
            insert_query = "INSERT INTO users (user_id, username, full_name, start_date, end_date) VALUES (?, ?, ?, ?, ?);"
            cursor.execute(insert_query, (user_id, username, full_name, start_date, end_date))
            print("Новая подписка успешно добавлена в базу данных!")

        # Подтверждаем изменения в базе данных
        conn.commit()

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрываем соединение с базой данных
        conn.close()


def get_all_subscriptions():
    try:
        # Подключаемся к базе данных (файлу)
        conn = sqlite3.connect('bot_sql.db')
        cursor = conn.cursor()

        # SQL-запрос для выборки всех строк из таблицы subscriptions
        select_query = "SELECT * FROM users;"

        # Выполняем запрос
        cursor.execute(select_query)

        # Получаем все строки
        rows = cursor.fetchall()

        # Формируем список в списке для всех строк
        subscriptions_list = [[row[0], row[1], row[2], row[3], row[4], row[5]] for row in rows]

        return subscriptions_list
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрываем соединение с базой данных
        conn.close()


def get_subscriptions_by_user_id(user_id):
    try:
        # Подключаемся к базе данных (файлу)
        conn = sqlite3.connect('bot_sql.db')
        cursor = conn.cursor()

        # SQL-запрос для выборки строк с определенным user_id
        select_query = "SELECT * FROM users WHERE user_id = ?;"

        # Выполняем запрос с указанным user_id
        cursor.execute(select_query, (user_id,))

        # Получаем все строки с этим user_id
        rows = cursor.fetchall()

        # Формируем список в списке для всех строк
        subscriptions_list = [[row[0], row[1], row[2], row[3], row[4], row[5]] for row in rows]

        return subscriptions_list
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрываем соединение с базой данных
        conn.close()
