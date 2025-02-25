#!/bin/bash
# sudo chmod 666 /var/run/docker.sock
# sudo chmod -R 777 ./data
# sudo chmod -R 777 ./airflow
# curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'
# docker compose up -d --
# spark-submit --packages io.delta:delta-spark_2.12:3.3.0  /opt/spark/scripts/process_json_to_delta.py
# docker exec spark_new /opt/bitnami/spark/bin/spark-submit --package io.delta:delta-spark_2.12:3.3.0 /opt/spark/scripts/process_json_to_delta.py
# spark-submit --packages io.delta:delta-spark_2.12:3.3.0  /opt/spark/scripts/process_delta_to_mongodb.py
docker compose -f docker-compose_db.yaml up -d --build --force-recreate
docker compose -f docker-compose_spark.yaml up -d --build --force-recreate --scale spark-worker=3
docker compose -f docker-compose_airflow.yaml up -d --build --force-recreate
docker compose -f docker-compose_airbyte.yaml up -d --build --force-recreate
docker compose -f docker-compose_qdrant.yaml up -d --build --force-recreate
docker compose -f docker-compose_sftp.yaml up -d --build ----force-recreate
# mongodb://root:example@localhost:27017/

docker compose -f docker-compose_db.yaml -f docker-compose_spark.yaml -f docker-compose_airflow.yaml up -d --build --force-recreate
# mongodb://root:example@localhost:27017/
docker exec spark-master-container spark-submit --packages io.delta:delta-spark_2.12:3.3.0 --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)
# echo "172.22.0.2 spark-master" >> /etc/hosts
docker exec spark-master-con spark-submit --packages io.delta:delta-spark_2.12:3.3.0 --master spark://spark-master:7077 --deploy-mode client ./scripts/process_json_to_delta.py

# Airbyte
ip addr show eth0 | grep inet | awk '{ print $2 }' | cut -d/ -f1
host.docker.internal

curl  -u 'airbyte:password' -X POST "http://localhost:8000/api/v1/connections/sync" \
 -H "Accept: application/json"\
 -H "Content-Type: application/json" \
 -d '{"connectionId":"[99e4ec1b-b607-43e7-a89b-b73aa6e34857]"}' 

 curl  -u 'akh.vyas@gmail.com:XOwgHUkY0jPjVduuQEW6i1slXz2ogCFI' -X POST "http://localhost:8000/api/v1/connections/sync" \
 -H "Accept: application/json"\
 -H "Content-Type: application/json" \
 -d '{"connectionId":"99e4ec1b-b607-43e7-a89b-b73aa6e34857"}'

Email: akh.vyas@gmail.com
Password: XOwgHUkY0jPjVduuQEW6i1slXz2ogCFI
Client-Id: 06421598-74d3-48bd-a34a-e54fcbc6d85b
Client-Secret: 5EvUgmLnANfQlkraCbsp5iXvou2G0NKV

curl -X POST http://localhost:8000/api/v1/applications/token \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_access_token" \
     -d '{"client_id": "06421598-74d3-48bd-a34a-e54fcbc6d85b", "client_secret": "5EvUgmLnANfQlkraCbsp5iXvou2G0NKV"}'

# sftp
ssh-keygen -f "/home/avyas/.ssh/known_hosts" -R "[127.0.0.1]:2222"
sftp -oPort=2222 foo@127.0.0.1
https://charts.mongodb.com/charts-project-0-xzlesxv/data-sources
https://cloud.qdrant.io/accounts/bad6e7b1-95fa-41cd-ac89-3bace33f3bae/clusters/e918655e-5705-4103-9dab-4e053444e94c/overview

