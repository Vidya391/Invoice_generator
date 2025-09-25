import sqlite3

# Connect to the database (creates file if it doesn’t exist)
conn = sqlite3.connect("invoices.db")
cursor = conn.cursor()

# Example: create tables if not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    product_name TEXT,
    quantity INTEGER,
    price REAL,
    tax REAL,
    total REAL
)
''')

conn.commit()
