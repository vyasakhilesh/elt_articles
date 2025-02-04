from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('extract_transform_load_delta_mongodb', default_args=default_args, schedule_interval=None)


spark_process_delta_to_mongodb_task = BashOperator(
    task_id='spark_process_delta_to_mongodb',
    bash_command='sh -c "docker exec spark-master-con spark-submit \
                  --packages io.delta:delta-spark_2.12:3.3.0 \
                  --master spark://spark-master:7077 \
                  --deploy-mode client ./scripts/process_delta_to_mongodb.py"',  # Replace with the batch command you want to run
    dag=dag,
)

spark_process_delta_to_mongodb_task