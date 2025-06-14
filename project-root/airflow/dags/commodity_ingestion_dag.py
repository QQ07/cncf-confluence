from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append("/opt/airflow/scripts")
from fetch_commodity import fetch_commodity_data

default_args = {
    'start_date': datetime(2025, 6, 14),
    'owner': 'airflow'
}

dag = DAG(
    'commodity_ingestion_dag',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
)

fetch_commodity_task = PythonOperator(
    task_id='fetch_commodity_data',
    python_callable=fetch_commodity_data,
    dag=dag
)