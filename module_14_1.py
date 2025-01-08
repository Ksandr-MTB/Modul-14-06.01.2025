import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')



# for i in range(1, 11):
#     cursor.execute("INSERT INTO Users(id, username, email, age, balance) VALUES(?, ?, ?, ?, ?)", (f"{i}", f"User{i}", f"example{i}@gmail.com", f"{10*i}", f"{1000}"))

# cursor.execute("UPDATE Users SET balance = ? WHERE id % 2 = 1", (500,))
# cursor.execute("DELETE FROM Users WHERE id = ?", (1,))
# for i in range(10):
#     if i % 3 == 0:
#         cursor.execute("DELETE FROM Users WHERE id = ?", (i+1,))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()
for user in users:
    print(user)


connection.commit()
connection.close()

