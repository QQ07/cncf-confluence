from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append("/opt/airflow/scripts")
from fetch_weather import fetch_weather_data

default_args = {
    'start_date': datetime(2025, 6, 14),
    'owner': 'airflow'
}

dag = DAG(
    'weather_ingestion_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

fetch_weather_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag
)