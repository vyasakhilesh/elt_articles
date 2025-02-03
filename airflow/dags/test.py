from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'batch_command_dag',
    default_args=default_args,
    schedule_interval=None,
)

run_batch_command = BashOperator(
    task_id='run_batch_command',
    bash_command='sh -c "docker exec spark-master-con spark-submit --packages io.delta:delta-spark_2.12:3.3.0 --master spark://spark-master:7077 --deploy-mode client ./scripts/process_json_to_delta.py"',  # Replace with the batch command you want to run
    dag=dag,
)

run_batch_command
