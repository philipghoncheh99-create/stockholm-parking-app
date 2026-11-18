import requests
import json

def get_street_info(street):
    url = f"https://openparking.stockholm.se/LTF-Tolken/v1/servicedagar/street/{street}?outputFormat=json"

    response = requests.get(url)

    data = response.json()

    if not data["features"]:
        return None

    return data["features"][0]["properties"]


