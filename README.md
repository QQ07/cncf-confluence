# 🌤️ Commodity & Weather Data Pipeline with Dashboard

This project implements a **cloud-native ETL pipeline** using **Apache Airflow** and **Streamlit**. It fetches daily **commodity prices** and **weather data** for selected districts, processes them into a combined CSV, and visualizes the results on a web dashboard — all containerized via **Docker Compose**.

---

## 📁 Project Structure

```
project-root/
├── airflow/
│   ├── dag/
│   │   ├── commodity_injection_dag.py
│   │   ├── weather_injection_dag.py
│   │   └── process_pipeline_dag.py
│   └── requirements.txt
|── db/
|    └── init.sql
├── scripts/
│   ├── fetch_commodities_data.py
│   ├── fetch_weather_data.py
│   └── process_data.py
├── streamlit/
│   ├── app.py
│   └── Dockerfile
├── .env
└── docker-compose.yml
```

---

## 🚀 Features

* ✅ **Apache Airflow** orchestrates:

  * Fetching commodity data
  * Fetching weather data
  * Processing and combining both into a CSV
* 📊 **Dashboard** visualizes the final processed data.
* 🐳 Fully **Dockerized** with a shared volume for inter-process communication.

---

## 🔧 Tech Stack

* **Apache Airflow**
* **Streamlit**
* **PostgreSQL** (for Airflow metadata DB)
* **Docker**
* **Python 3.9+**

---

## ⚙️ Setup & Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create `.env` File (if needed)

If your APIs require keys, create a `.env` file at the root level:

```
WEATHER_API_KEY=your_key
COMMODITY_API_KEY=your_key
```

### 3. Start the Application

```bash
docker-compose up --build
```

### 4. Run the Dashboard

```bash
streamlit run app.py
```

This will spin up:

* Postgres
* Airflow Webserver (localhost:8080)
* Airflow Scheduler
* Streamlit Dashboard (localhost:8501)

### 4. Access Services

* 🌐 Airflow UI: [http://localhost:8080](http://localhost:8080)

  * Username: `admin`
  * Password: `admin`
* 📊 Streamlit Dashboard: [http://localhost:8501](http://localhost:8501)

---

## 📂 DAG Overview

| DAG Name                     | Description                                 |
| ---------------------------- | ------------------------------------------- |
| `commodity_injection_dag.py` | Fetches commodity pricing from Public API   |
| `weather_injection_dag.py`   | Fetches weather data from weather API       |
| `process_pipeline_dag.py`    | Merges both JSONs and writes to CSV file    |

---

## 📈 Data Flow

1. **Extract**: API data is fetched and saved as `commodities_data.json` and `weather_data.json`.
2. **Transform**: These are merged by `process_data.py` into `combined_data.csv`.
3. **Load**: `app.py` in Streamlit reads the CSV and shows it via charts/tables.

---

## 📦 Volumes and Shared Data

Airflow DAGs and the Streamlit app use a **shared `/data` volume** to exchange `.json` and `.csv` files between containers.

---

## 🧪 Development & Testing

To test individual scripts locally:

```bash
python scripts/fetch_commodities_data.py
python scripts/fetch_weather_data.py
python scripts/process_data.py
```

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

* [Commodities API](https://www.data.gov.in/)
* [Weather API](http://api.openweathermap.org/data/2.5/weather?q={city}&appid=API_KEY)
