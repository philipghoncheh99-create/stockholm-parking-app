from datetime import datetime, timedelta

import requests
import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

now = datetime.now()

today_weekday = now.weekday() + 1
current_hour = now.hour


weekday_map = {
    "måndag": 1,
    "tisdag": 2,
    "onsdag": 3,
    "torsdag": 4,
    "fredag": 5
}

def get_street_info(street_name):

    url = f"https://openparking.stockholm.se/LTF-Tolken/v1/servicedagar/street/{street_name}?outputFormat=json"

    response = requests.get(url)

    print(response.status_code)

    data = response.json()


    if not data["features"]:
        return None

    feature = data["features"][0]
    print("Antal segment:", len(data["features"]))

    return {
    "properties": feature["properties"],
    "coordinates": feature["geometry"]["coordinates"], 
    "all_features": data["features"]
}



def get_parking_info(cleaning_day, start_hour, end_hour):

    today = datetime.today()

    today_weekday = today.weekday() + 1

    current_hour = today.hour

    days_until = (cleaning_day - today_weekday) % 7 

    next_cleaning = today + timedelta(days=days_until)

    move_date = next_cleaning - timedelta(days=1)

    status = "🟢 Parkering tillåten"
    status_class = "green"

    if days_until == 0:

        if start_hour <= current_hour < end_hour:
            status = "🔴 Parkeringsförbud idag"
            status_class = "red"

        else:
            next_cleaning = today + timedelta(days=7)
            move_date = next_cleaning - timedelta(days=1)

    elif days_until == 1:

        status = "🟠 Städning imorgon"
        status_class = "orange"

    print(days_until)
    print(status)
    return {
        "status": status,
        "status_class": status_class,
        "cleaning_date": next_cleaning.strftime("%d/%m/%Y"),
        "move_date": move_date.strftime("%d/%m/%Y")
    }

@app.route("/", methods=["GET", "POST"])
def home():
    

    result = None
    street_name = None

    if request.method == "POST":

        street_name = request.form["street"].title()

        street_info = get_street_info(street_name)
        props = street_info["properties"]
        coords = street_info["coordinates"]
        all_features = street_info["all_features"]

    
        if street_info:

            props = street_info["properties"]
            coords = street_info["coordinates"]

            weekday_text = props["START_WEEKDAY"].lower()
            cleaning_day = weekday_map[weekday_text]

            start_hour = props["START_TIME"] // 100
            end_hour = props["END_TIME"] // 100

            result = get_parking_info(
            cleaning_day,
            start_hour,
            end_hour
            )

            result["street"] = props["STREET_NAME"]

            start_time = str(props["START_TIME"]).zfill(4)
            end_time = str(props["END_TIME"]).zfill(4)

            result["start_time"] = f"{start_time[:2]}:{start_time[2:]}"
            result["end_time"] = f"{end_time[:2]}:{end_time[2:]}"

            result["lat"] = coords[0][1]
            result["lng"] = coords[0][0]

            result["coordinates"] = [
                [coord[1], coord[0]]
                for coord in coords
            ]

            result["all_segments"] = []

            for feature in all_features:

                segment = [
                [coord[1], coord[0]]
                for coord in feature["geometry"]["coordinates"]
    ]
                result["all_segments"].append(segment)
        else:

            result = {
        "status": "❌ Gatan hittades inte",
        "status_class": "red",
        "street": street_name,
        "start_time": "-",
        "end_time": "-",
        "cleaning_date": "-",
        "move_date": "-"
    }
            print(result)
    return render_template(
        "index.html",
        result=result
    )

@app.route("/autocomplete")
def autocomplete():

    query = request.args.get("q", "")

    matches = search_streets(query)

    return jsonify(matches)

def search_streets(query):

    conn = sqlite3.connect("streets.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT street_name
        FROM street_names
        WHERE street_name LIKE ?
        ORDER BY street_name
        LIMIT 5
        """,
        (f"%{query}%",)
    )

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]

if __name__ == "__main__":
    app.run(debug=True)