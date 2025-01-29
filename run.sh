#!/bin/bash

# curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'
# docker compose up -d --
docker compose -f docker-compose_db.yaml -f docker-compose_spark.yaml -f docker-compose_airflow.yaml up --build
