import requests
import json

def fetch_commodity_data():
    url = "https://api.data.gov.in/resource/xxx?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json"
    res = requests.get(url)
    with open("/opt/airflow/scripts/commodities.json", "w") as f:
        json.dump(res.json(), f)