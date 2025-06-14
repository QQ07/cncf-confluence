from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime
import sys

sys.path.append("/opt/airflow/scripts")
from process_data import process_and_store

default_args = {"start_date": datetime(2025, 6, 14), "owner": "airflow"}

dag = DAG(
    "process_pipeline_dag",
    default_args=default_args,
    schedule_interval="*/5 * * * *",
    catchup=False,
)

wait_for_weather = ExternalTaskSensor(
    task_id="wait_for_weather_dag",
    external_dag_id="weather_ingestion_dag",
    external_task_id="fetch_weather_data",
    mode="reschedule",
    timeout=300,
    poke_interval=30,
    dag=dag,
)

wait_for_commodity = ExternalTaskSensor(
    task_id="wait_for_commodity_dag",
    external_dag_id="commodity_ingestion_dag",
    external_task_id="fetch_commodity_data",
    mode="reschedule",
    timeout=300,
    poke_interval=30,
    dag=dag,
)

process_task = PythonOperator(
    task_id="process_and_store", python_callable=process_and_store, dag=dag
)
