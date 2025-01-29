from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

def spark_process_to_mongodb():
    script_path = '/path/to/spark/scripts/process_delta_to_mongodb.py'
    subprocess.run(['spark-submit', script_path])

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('extract_transform_load_mongodb', default_args=default_args, schedule_interval=None)

spark_task = PythonOperator(
    task_id='spark_process_to_mongodb',
    python_callable=spark_process_to_mongodb,
    dag=dag,
)
