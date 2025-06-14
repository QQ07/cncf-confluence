from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append("/opt/airflow/scripts")
from process_data import process_and_store

default_args = {
    'start_date': datetime(2025, 6, 14),
    'owner': 'airflow'
}

dag = DAG(
    'process_pipeline_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

process_task = PythonOperator(
    task_id='process_and_store',
    python_callable=process_and_store,
    dag=dag
)