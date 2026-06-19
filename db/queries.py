create_products_table = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        bought INTEGER NOT NULL DEFAULT 0
    );
"""

insert_product = "INSERT INTO products (name, quantity) VALUES (?, ?)"

select_all = "SELECT id, name, quantity, bought FROM products ORDER BY id"
select_bought = "SELECT id, name, quantity, bought FROM products WHERE bought = 1 ORDER BY id"
select_unbought = "SELECT id, name, quantity, bought FROM products WHERE bought = 0 ORDER BY id"

update_bought = "UPDATE products SET bought = ? WHERE id = ?"

delete_product = "DELETE FROM products WHERE id = ?"

count_total = "SELECT COUNT(*) FROM products"
count_bought = "SELECT COUNT(*) FROM products WHERE bought = 1"