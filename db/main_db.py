import sqlite3
from config import path_db
from db import queries


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.create_products_table)
    print('БД подключена!')
    conn.commit()
    conn.close()


def add_product(name, quantity):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.insert_product, (name, quantity))
        product_id = cursor.lastrowid
    return product_id


def get_products(filter_type='all'):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == 'bought':
        cursor.execute(queries.select_bought)
    elif filter_type == 'unbought':
        cursor.execute(queries.select_unbought)
    else:
        cursor.execute(queries.select_all)

    products = cursor.fetchall()
    conn.close()
    return products


def set_bought(product_id, is_bought):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.update_bought, (int(is_bought), product_id))
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_product, (product_id,))
    conn.commit()
    conn.close()


def count_products():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    total = cursor.execute(queries.count_total).fetchone()[0]
    bought = cursor.execute(queries.count_bought).fetchone()[0]
    conn.close()
    return bought, total