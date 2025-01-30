#!/bin/bash

# curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'
# docker compose up -d --
# spark-submit --packages io.delta:delta-spark_2.12:3.3.0  /opt/spark/scripts/process_json_to_delta.py
# docker exec spark_new /opt/bitnami/spark/bin/spark-submit --package io.delta:delta-spark_2.12:3.3.0 /opt/spark/scripts/process_json_to_delta.py
docker compose -f docker-compose_db.yaml -f docker-compose_spark.yaml -f docker-compose_airflow.yaml up -d --build --force-recreate
