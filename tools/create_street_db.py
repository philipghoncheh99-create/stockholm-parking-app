import sqlite3

conn = sqlite3.connect("streets.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS street_names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street_name TEXT UNIQUE
)
""")

conn.commit()
conn.close()

print("Databas skapad")