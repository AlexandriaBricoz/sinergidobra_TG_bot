import sqlite3


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
    print(1)
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


def add_subscription(user_id, username, full_name, start_date, end_date):
    try:
        # Подключаемся к базе данных (файлу)
        conn = sqlite3.connect('bot_sql.db')
        cursor = conn.cursor()

        # SQL-запрос для вставки данных в таблицу subscriptions
        insert_query = "INSERT INTO users (user_id, username, full_name, start_date, end_date) VALUES (?, ?, ?, ?, ?);"

        # Выполняем запрос с данными пользователя и датами подписки
        cursor.execute(insert_query, (user_id, username, full_name, start_date, end_date))

        # Подтверждаем изменения в базе данных
        conn.commit()

        print("Запись успешно добавлена в базу данных!")
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
