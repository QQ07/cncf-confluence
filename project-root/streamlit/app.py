import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Commodity Dashboard", layout="wide")
st.title("🌾 Commodity Price & Weather Dashboard")

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv("D:/COLLEGE/Hackathon/CNCF/cncf-confluence/project-root/scripts/combined_data.csv")
    df["arrival_date"] = pd.to_datetime(df["arrival_date"], format="%d/%m/%Y")
    return df

df = load_data()

# Filters
st.sidebar.header("🔍 Filter Data")

districts = sorted(df["district"].unique())
selected_district = st.sidebar.selectbox("Select District", ["All"] + districts)

commodities = sorted(df["commodity"].unique())
selected_commodity = st.sidebar.selectbox("Select Commodity", ["All"] + commodities)

min_date, max_date = df["arrival_date"].min(), df["arrival_date"].max()
selected_range = st.sidebar.date_input("Select Date Range", (min_date, max_date), min_value=min_date, max_value=max_date)

# Apply filters
filtered_df = df.copy()
if selected_district != "All":
    filtered_df = filtered_df[filtered_df["district"] == selected_district]
if selected_commodity != "All":
    filtered_df = filtered_df[filtered_df["commodity"] == selected_commodity]
if len(selected_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["arrival_date"] >= pd.to_datetime(selected_range[0])) &
        (filtered_df["arrival_date"] <= pd.to_datetime(selected_range[1]))
    ]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Overview Metrics
st.header("📊 Key Indicators")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Avg Temp (°C)", f"{filtered_df['temperature_c'].mean():.1f}")
col2.metric("🧪 Avg PM2.5", f"{filtered_df['pm2_5'].mean():.1f}")
col3.metric("💧 Avg Humidity (%)", f"{filtered_df['humidity'].mean():.1f}")
col4.metric("💰 Avg Modal Price (₹)", f"{filtered_df['modal_price'].mean():.0f}")

# Chart: Temp vs Modal Price
st.subheader("📈 Temperature vs Modal Price")
fig1 = px.scatter(
    filtered_df,
    x="temperature_c",
    y="modal_price",
    color="district",
    hover_data=["commodity", "arrival_date"],
    title="Impact of Temperature on Modal Price"
)
st.plotly_chart(fig1, use_container_width=True)

# Chart: PM2.5 vs Modal Price
st.subheader("🧪 PM2.5 vs Modal Price")
fig2 = px.scatter(
    filtered_df,
    x="pm2_5",
    y="modal_price",
    color="commodity",
    hover_data=["district", "arrival_date"],
    title="Impact of Air Pollution (PM2.5) on Prices"
)
st.plotly_chart(fig2, use_container_width=True)

# District Heatmap
st.subheader("📍 District-wise Price Distribution")
heat_df = filtered_df.groupby("district")["modal_price"].mean().reset_index()
fig4 = px.bar(
    heat_df,
    x="district",
    y="modal_price",
    color="modal_price",
    title="Avg Modal Price by District"
)
st.plotly_chart(fig4, use_container_width=True)

# Data Table
st.subheader("📋 Raw Data Table")
st.dataframe(
    filtered_df[[
        "district", "market", "commodity", "arrival_date", 
        "modal_price", "temperature_c", "pm2_5", "humidity", "condition"
    ]].sort_values("arrival_date", ascending=False),
    use_container_width=True
)

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — This dashboard empowers farmers and policymakers to understand how weather affects food prices.")

