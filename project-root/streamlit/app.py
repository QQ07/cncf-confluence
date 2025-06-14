import streamlit as st
import pandas as pd
import psycopg2

st.title("🌤️ Weather + Commodity Dashboard")

conn = psycopg2.connect(host="postgres", dbname="airflow", user="airflow", password="airflow")
df = pd.read_sql("SELECT * FROM compatible_data ORDER BY arrival_date DESC", conn)

commodity = st.selectbox("Choose commodity", sorted(df["commodity"].unique()))
filtered = df[df["commodity"] == commodity]

st.metric("Average Price", round(filtered["modal_price"].mean(), 2))
st.metric("Average PM2.5", round(filtered["pm2_5"].mean(), 2))
st.metric("Average Temp (°C)", round(filtered["temperature"].mean(), 2))

st.bar_chart(filtered[["arrival_date", "modal_price"]].set_index("arrival_date"))