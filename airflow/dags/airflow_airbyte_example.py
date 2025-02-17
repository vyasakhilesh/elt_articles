from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow.sensors.filesystem import FileSensor
import pendulum
from datetime import datetime, timedelta

AIRBYTE_CONNECTION_ID = '99e4ec1b-b607-43e7-a89b-b73aa6e34857'
RAW_PRODUCTS_FILE = '/tmp/airbyte_local/json_from_faker/_airbyte_raw_products.jsonl'
COPY_OF_RAW_PRODUCTS = '/tmp/airbyte_local/json_from_faker/moved_raw_products.jsonl'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


with DAG(dag_id='airbyte_example_airflow_dag',
        default_args=default_args,
        schedule_interval=None
   ) as dag:
    
   test_connection_airbyte = BashOperator(
       task_id='test_connection_airbyte',
       bash_command="""curl  -u 'akh.vyas@gmail.com:XOwgHUkY0jPjVduuQEW6i1slXz2ogCFI' -X POST "http://host.docker.internal:8000/api/v1/connections/sync" \
                           -H "Accept: application/json"\
                           -H "Content-Type: application/json" \
                           -d '{"connectionId":"99e4ec1b-b607-43e7-a89b-b73aa6e34857"}'"""
   )

   trigger_airbyte_sync = AirbyteTriggerSyncOperator(
       task_id='airbyte_trigger_sync',
       airbyte_conn_id='airflow-call-to-airbyte-example', #'airbyte_http',#'airflow-call-to-airbyte-example',
       connection_id=AIRBYTE_CONNECTION_ID,
       asynchronous=True
   )

   wait_for_sync_completion = AirbyteJobSensor(
       task_id='airbyte_check_sync',
       airbyte_conn_id= 'airflow-call-to-airbyte-example', #'airbyte_http', #'airflow-call-to-airbyte-example',
       airbyte_job_id=trigger_airbyte_sync.output
   )

   raw_products_file_sensor = FileSensor(
       task_id='check_if_file_exists_task',
       timeout=5,
       filepath=RAW_PRODUCTS_FILE,
       fs_conn_id='airflow-file-connector'
   )

   move_raw_products_file = BashOperator(
       task_id='move_raw_products_file',
       bash_command=f'mv {RAW_PRODUCTS_FILE} {COPY_OF_RAW_PRODUCTS}'
   )

   # test_connection_airbyte >> trigger_airbyte_sync >> wait_for_sync_completion >>  raw_products_file_sensor >> move_raw_products_file
   trigger_airbyte_sync >> wait_for_sync_completion >>  raw_products_file_sensor >> move_raw_products_file