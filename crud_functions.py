# Создайте файл crud_functions.py и напишите там следующие функции:
# initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
#
#     id - целое число, первичный ключ
#     title(название продукта) - текст (не пустой)
#     description(описание) - текст
#     price(цена) - целое число (не пустой)
#
# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

import sqlite3
DB_FILE = "database.db"

catalog_product = (
{'title':'Витамины A', 'description': 'описание 1', 'price': 1 * 100, 'file': 'files/1.jpg', 'label':'Продукт 1'},
{'title':'Витамины D', 'description': 'описание 2', 'price': 2 * 100, 'file': 'files/2.jpg', 'label':'Продукт 2'},
{'title':'Витамины C', 'description': 'описание 3', 'price': 3 * 100, 'file': 'files/3.jpg', 'label':'Продукт 3'},
{'title':'Витамины F', 'description': 'описание 4', 'price': 4 * 100, 'file': 'files/4.jpg', 'label':'Продукт 4'},
)

class DataBase:

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def execute(self, sql, parameters=(), fetch_type=""):
        if len(parameters) == 0:
            res_ex = self.cursor.execute(sql)
        else:
            res_ex = self.cursor.execute(sql, parameters)
        self.connection.commit()
        return res_ex

    def fetch(self, fetch_type=1):
        if fetch_type == 1:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def drop_table(self, table_name):
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(sql)

    def __del__(self):
        self.connection.commit()
        self.connection.close()



def initiate_db():
    db = DataBase(DB_FILE)
    #     id - целое число, первичный ключ
    #     title(название продукта) - текст (не пустой)
    #     description(описание) - текст
    #     price(цена) - целое число (не пустой)
    db.execute('''
        CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        file TEXT NOT NULL,
        label TEXT NOT NULL
        );
        ''')
    # id - целое число, первичный ключ
    # username - текст (не пустой)
    # email - текст (не пустой)
    # age - целое число (не пустой)
    # balance - целое число (не пустой)
    db.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        );
        ''')

def add_user(username, email, age, balance=1000):
    db = DataBase(DB_FILE)
    if not is_included(username):
        db.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (username, email, age, balance))

def is_included(username):
    db = DataBase(DB_FILE)
    db.execute("SELECT * FROM Users WHERE username=?", (username,))
    is_user_exist = db.fetch(1)
    return is_user_exist is not None

def get_all_products():
    db = DataBase(DB_FILE)
    db.execute("SELECT * FROM Products")
    all_prod = db.fetch("*")
    catalog_prod = []
    for prod in all_prod:
        catalog_prod.append({'title':prod[1], 'description':prod[2], 'price':prod[3], 'file':prod[4], 'label':prod[5]})
    return catalog_prod

def fill_db(catalog_product):
    db = DataBase(DB_FILE)
    db.drop_table("Products")
    initiate_db()
    for prod in catalog_product:
        db.execute("INSERT INTO Products('title', 'description', 'price', 'file', 'label') VALUES (?,?,?,?,?)",
                   (prod['title'], prod['description'], prod['price'], prod['file'], prod['label']))


initiate_db()
fill_db(catalog_product)
#all_prod = get_all_products()
#for prod in all_prod:
#    print(f"Название: {prod['title']} | Описание: {prod['description']}  | Цена: {prod['price']} ")