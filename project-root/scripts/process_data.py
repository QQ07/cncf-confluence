import json
import psycopg2
import pandas as pd

def process_and_store():
    with open("/opt/airflow/scripts/weather.json") as f:
        weather = json.load(f)

    with open("/opt/airflow/scripts/commodities.json") as f:
        commodities = json.load(f)["records"]

    df = pd.DataFrame(commodities)
    df["modal_price"] = pd.to_numeric(df["modal_price"], errors="coerce")
    df["pm2_5"] = weather["current"]["air_quality"]["pm2_5"]
    df["temperature"] = weather["current"]["temp_c"]
    df["aqi"] = weather["current"]["air_quality"]["us-epa-index"]

    conn = psycopg2.connect(
        dbname="airflow", user="airflow", password="airflow", host="postgres")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS compatible_data (
            id SERIAL PRIMARY KEY,
            commodity TEXT,
            state TEXT,
            market TEXT,
            arrival_date TEXT,
            modal_price NUMERIC,
            temperature NUMERIC,
            pm2_5 NUMERIC,
            aqi INTEGER
        )
    """)
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO compatible_data (commodity, state, market, arrival_date, modal_price, temperature, pm2_5, aqi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (row["commodity"], row["state"], row["market"], row["arrival_date"], row["modal_price"], row["temperature"], row["pm2_5"], row["aqi"]))
    conn.commit()
    cur.close()
    conn.close()