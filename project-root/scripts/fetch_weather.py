import requests
import json
from datetime import datetime

def fetch_weather_data():
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": "your_weather_api_key",
        "q": "Pune",
        "aqi": "yes"
    }
    res = requests.get(url, params=params)
    with open("/opt/airflow/scripts/weather.json", "w") as f:
        json.dump(res.json(), f)