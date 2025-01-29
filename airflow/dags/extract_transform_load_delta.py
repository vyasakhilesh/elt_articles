from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import zipfile
import subprocess

def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def spark_process_to_delta(script_path):
    # docker exec spark-container /opt/spark/bin/spark-submit /opt/spark/scripts/process_json_to_delta.py
    # subprocess.run(['spark-submit', script_path])
    result = subprocess.check_output(['docker',\
                    'exec',\
                    'spark_new',\
                    '/opt/bitnami/spark/bin/spark-submit',\
                    '--package',\
                    'io.delta:delta-spark_2.12:3.3.0', \
                     script_path], text=True)
    print(result)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('extract_transform_load_delta', default_args=default_args, schedule_interval=None)

unzip_task = PythonOperator(
    task_id='unzip_file',
    python_callable=unzip_file,
    op_kwargs={
        'zip_path':"/opt/airflow/data/raw_data/sample_data/resync_datadump_sample220218.zip", 
        'extract_path':"/opt/airflow/data/raw_data/extracted_data/resync_datadump_sample220218/", 
        },
    dag=dag,
)

spark_task = PythonOperator(
    task_id='spark_process_to_delta',
    python_callable=spark_process_to_delta,
    op_kwargs={'script_path':"/opt/spark/scripts/process_json_to_delta.py"},
    dag=dag,
)

unzip_task >> spark_task
