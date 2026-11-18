import requests
import sqlite3

url = "https://openparking.stockholm.se/LTF-Tolken/v1/servicedagar/all?outputFormat=json"

response = requests.get(url)

data = response.json()

conn = sqlite3.connect("streets.db")
cursor = conn.cursor()

street_names = set()

for feature in data["features"]:

    properties = feature["properties"]

    if "STREET_NAME" in properties:

        street_name = properties["STREET_NAME"]

        if street_name:
            street_names.add(street_name)

print(f"Hittade {len(street_names)} gator")

for street in street_names:

    cursor.execute(
        """
        INSERT OR IGNORE INTO street_names(street_name)
        VALUES (?)
        """,
        (street,)
    )

conn.commit()
conn.close()

print("Import klar!")