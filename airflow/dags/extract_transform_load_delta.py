from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import zipfile

def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('extract_transform_load_delta', default_args=default_args, schedule_interval=None)

# download zipped files

unzip_task = PythonOperator(
    task_id='unzip_file',
    python_callable=unzip_file,
    op_kwargs={
        'zip_path':"/opt/airflow/data/raw_data/sample_data/resync_datadump_sample220218.zip", 
        'extract_path':"/opt/airflow/data/raw_data/extracted_data/resync_datadump_sample220218/", 
        },
    dag=dag,
)

spark_process_json_to_delta_task = BashOperator(
    task_id='spark_process_json_to_delta',
    bash_command='sh -c "docker exec spark-master-con spark-submit \
                  --packages io.delta:delta-spark_2.12:3.3.0 \
                  --master spark://spark-master:7077 \
                  --deploy-mode client ./scripts/process_json_to_delta.py"',  
                  # Replace with the batch command you want to run
    dag=dag,
)

unzip_task >> spark_process_json_to_delta_task
