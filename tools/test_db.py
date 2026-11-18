import sqlite3

conn = sqlite3.connect("streets.db")

cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM street_names
""")

print(cursor.fetchone())

conn.close()