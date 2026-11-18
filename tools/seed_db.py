import sqlite3

conn = sqlite3.connect("streets.db")

cursor = conn.cursor()

streets = [
    ("Cedergrensvägen",),
    ("Kransbindarvägen",),
    ("Bäckvägen",),
    ("Fastlagsvägen",)
]

cursor.executemany(
    "INSERT OR IGNORE INTO street_names (street_name) VALUES (?)",
    streets
)

conn.commit()
conn.close()

print("Klart")