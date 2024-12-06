import sqlite3

connection = sqlite3.connect('database2.db')
cursor = connection.cursor()

def initiate_db():
    connection = sqlite3.connect('database2.db')
    cursor = connection.cursor()


    # Создать базу продуктов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products
    (id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL)''')

    # Создать базу клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users
    (id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL)''')


    # Очистить базу продуктов
    cursor.execute('DELETE FROM Products')

    # Заполнить базу продуктами
    fruit = ['apple','banana', 'peach', 'garnet']
    for i in range(4):
        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"Product{i+1}", fruit[i], (i+1)*20))
    connection.commit()
    connection.close()


# Заполняем базу клиентов
def add_user(username, email, age):
    connection = sqlite3.connect('database2.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                  (username, email, age, 1000))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('database2.db')
    cursor = connection.cursor()

    user = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if user.fetchone() is None:
        return True
    else:
        return False


# Выбрать продукты из базы
def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products
