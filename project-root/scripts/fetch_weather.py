import requests
import json
import os

def fetch_weather_data():
    districts = [
        "Ahmedabad",
        "Amreli", 
        "Anand",
        "Banaskanth",
        "Dahod",
        "Gandhinagar"
    ]
    url = "http://api.weatherapi.com/v1/current.json"
    api_key = "8ed720fd610444ce8e455110251406"
    results = {}

    for district in districts:
        params = {
            "key": api_key,
            "q": district,
            "aqi": "yes"
        }
        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            results[district] = res.json()
        except Exception as e:
            results[district] = {"error": str(e)}

    print(results)
    # Create directory if it doesn't exist
    output_dir = "project-root/scripts"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "weather.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"All district data saved to {file_path}")

if __name__ == "__main__":
    fetch_weather_data()