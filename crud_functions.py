#База продуктов

import sqlite3

def initiate_db():
    connection = sqlite3.connect('database2.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products
                 (id INTEGER PRIMARY KEY, 
                 title TEXT NOT NULL, 
                 description TEXT NOT NULL, 
                 price INTEGER NOT NULL)''')

    # Очистить базу
    cursor.execute('DELETE FROM Products')

    # Заполнить базу продуктами
    fruit = ['apple','banana', 'peach', 'garnet']
    for i in range(4):
        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"Product{i+1}", fruit[i], (i+1)*20))
    connection.commit()
    connection.close()

# Выбрать продукты из базы
def get_all_products():
    connection = sqlite3.connect('database2.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products




