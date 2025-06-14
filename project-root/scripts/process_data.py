import json
import csv
from datetime import datetime

# Load JSON files
with open('weather.json', 'r', encoding='utf-8') as f:
    weather_data = json.load(f)

with open('commodities.json', 'r', encoding='utf-8') as f:
    commodities_data = json.load(f)

# Prepare CSV
csv_fields = [
    "state", "district", "market", "commodity", "variety", "grade", "arrival_date",
    "min_price", "max_price", "modal_price",
    "temperature_c", "uv_index", "pm2_5", "humidity", "condition"
]

rows = []

for district, comm_info in commodities_data.items():
    # Get weather info for this district
    weather_info = weather_data.get(district)
    if not weather_info or "location" not in weather_info or "current" not in weather_info:
        continue  # skip if no valid weather data

    # Extract weather fields
    w_loc = weather_info["location"]
    w_cur = weather_info["current"]
    state = w_loc["region"]
    district_name = w_loc["name"]
    # Use date in dd/mm/yyyy format to match arrival_date
    weather_date = datetime.strptime(w_cur["last_updated"], "%Y-%m-%d %H:%M").strftime("%d/%m/%Y")

    temperature_c = w_cur.get("temp_c")
    uv_index = w_cur.get("uv")
    pm2_5 = w_cur.get("air_quality", {}).get("pm2_5")
    humidity = w_cur.get("humidity")
    condition = w_cur.get("condition", {}).get("text")

    # For each commodity record in this district
    for record in comm_info.get("records", []):
        # Only keep if arrival_date matches weather_date
        if record["arrival_date"] != weather_date:
            continue

        row = {
            "state": record["state"],
            "district": record["district"],
            "market": record["market"],
            "commodity": record["commodity"],
            "variety": record["variety"],
            "grade": record["grade"],
            "arrival_date": record["arrival_date"],
            "min_price": record["min_price"],
            "max_price": record["max_price"],
            "modal_price": record["modal_price"],
            "temperature_c": temperature_c,
            "uv_index": uv_index,
            "pm2_5": pm2_5,
            "humidity": humidity,
            "condition": condition
        }
        rows.append(row)

# Write to CSV
with open('combined_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=csv_fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} rows to combined_data.csv")