import requests
import json

def fetch_commodity_data():
    url = "https://api.data.gov.in/resource/xxx?api-key=your_key&format=json"
    res = requests.get(url)
    with open("/opt/airflow/scripts/commodities.json", "w") as f:
        json.dump(res.json(), f)