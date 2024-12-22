# Домашнее задание по теме "Выбор элементов и функции в SQL запросах"
# Если вы решали старую версию задачи, проверка будет производиться по ней.
# Ссылка на старую версию тут.
# Цель: научится использовать функции внутри запросов языка SQL и использовать их в решении задачи.
#
# Задача "Средний баланс пользователя":
# Для решения этой задачи вам понадобится решение предыдущей.
# Для решения необходимо дополнить существующий код:
#
#     Удалите из базы данных not_telegram.db запись с id = 6.
#     Подсчитать общее количество записей.
#     Посчитать сумму всех балансов.
#     Вывести в консоль средний баланс всех пользователей.
#
#
#
# Пример результата выполнения программы:
# Выполняемый код:
# # Код из предыдущего задания
# # Удаление пользователя с id=6
# # Подсчёт кол-ва всех пользователей
# # Подсчёт суммы всех балансов
# print(all_balances / total_users)
# connection.close()
#
# Вывод на консоль:
# 700.0

import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)    
''')

for i in range(1,11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (f"User{i}", f"example{i}@gmail.com", i*10, 1000))
connection.commit()
# Обновите balance у каждой 2ой записи начиная с 1ой на 500:
for i in range(1,11,2):
    cursor.execute("UPDATE Users SET balance=? WHERE username=?",(500, f"User{i}"))
connection.commit()
# Удалите каждую 3ую запись в таблице начиная с 1ой:
for i in range(1,11,3):
    cursor.execute("DELETE FROM Users WHERE username=?", (f"User{i}",))
connection.commit()
cursor.execute("SELECT * FROM Users WHERE age<>?", (60,))
users = cursor.fetchall()
#for user in users:
#    print(f"Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}")

#     Удалите из базы данных not_telegram.db запись с id = 6.
cursor.execute("DELETE FROM Users WHERE id=?", (6,))
#     Подсчитать общее количество записей.
res_ex = cursor.execute("SELECT COUNT(*) FROM Users")
total_users = res_ex.fetchone()[0]
#     Посчитать сумму всех балансов.
res_ex = cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = res_ex.fetchone()[0]
#     Вывести в консоль средний баланс всех пользователей.
res_ex = cursor.execute("SELECT AVG(balance) FROM Users")
avg_balance = res_ex.fetchone()[0]

print(f"avg_balance={avg_balance}\nall_balances / total_users={all_balances / total_users}")


connection.commit()
connection.close()