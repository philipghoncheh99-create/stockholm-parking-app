import sqlite3

conn = sqlite3.connect("streets.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS streets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street_name TEXT NOT NULL,
    cleaning_day INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Databas skapad!")
