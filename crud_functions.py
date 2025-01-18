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


    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('list_price.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    for product in products:
        print(product)



