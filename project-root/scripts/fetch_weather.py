import requests
import json
from datetime import datetime

def fetch_weather_data():
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": "8ed720fd610444ce8e455110251406",
        "q": "Pune",
        "aqi": "yes"
    }
    res = requests.get(url, params=params)
    with open("/opt/airflow/scripts/weather.json", "w") as f:
        json.dump(res.json(), f)