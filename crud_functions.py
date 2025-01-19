import sqlite3

def initiate_db():
    connection = sqlite3.connect('list_price.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    # for i in range(1, 5):
    #     cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", (f"Продукт{i}", f"Описание {i}", f"{100*i}"))

    conn = sqlite3.connect('list_users.db')
    cursor_1 = conn.cursor()
    cursor_1.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    """)


    connection.commit()
    connection.close()
    conn.commit()
    conn.close()


def get_all_products():
    connection = sqlite3.connect('list_price.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    for product in products:
        print(product)

def add_user(username, email, age):
    conn = sqlite3.connect('list_users.db')
    cursor_1 = conn.cursor()
    cursor_1.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)", (f'{username}', f'{email}', f'{age}', f'{1000}'))
    conn.commit()
    conn.close()

def is_included(username):
    conn = sqlite3.connect('list_users.db')
    cursor_1 = conn.cursor()
    check_user = cursor_1.execute("SELECT * FROM Users WHERE username=?", (username,))
    if check_user.fetchone() is None:
        return True
    else:
        return False



