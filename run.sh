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
docker compose -f docker-compose_sftp.yaml up -d --build --force-recreate
docker compose -f docker-compose_postgresql.yaml up -d --build --force-recreate
docker compose -f docker-compose_dbt.yaml up -d --build --force-recreate

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

curl -u 'akh.vyas@gmail.com:XOwgHUkY0jPjVduuQEW6i1slXz2ogCFI' -X GET \
     --url http://localhost:8000/api/public/v1/workspaces \
     --header 'accept: application/json'

curl -u 'akh.vyas@gmail.com:XOwgHUkY0jPjVduuQEW6i1slXz2ogCFI' -X GET \
     --url http://172.18.0.2/api/public/v1/workspaces \
     --header 'accept: application/json'

curl -u 'akh.vyas@gmail.com:XOwgHUkY0jPjVduuQEW6i1slXz2ogCFI' -X GET \
     --url http://airbyte-abctl-control-plane:80/api/public/v1/workspaces \
     --header 'accept: application/json'

{
  "2b04e86a-aec6-4aff-b053-e7a238dd976e": {
    "conn_type": "airbyte",
    "description": "",
    "login": "akh.vyas@gmail.com",
    "password": "vyas1234",
    "host": "airbyte-abctl-control-plane",
    "port": 80,
    "schema": "",
    "extra": "{}"
  }

import json
from airflow.models.connection import Connection

c = Connection(
     conn_id='2b04e86a-aec6-4aff-b053-e7a238dd976e',
     conn_type='airbyte',
     description='connection description',
     host='airbyte-abctl-control-plane',
     login='akh.vyas@gmail.com',
     password='XOwgHUkY0jPjVduuQEW6i1slXz2ogCFI',
     extra=json.dumps(dict(this_param='some val', that_param='other val*')), )
print(f"AIRFLOW_CONN_{c.conn_id.upper()}='{c.get_uri()}'")
AIRFLOW_CONN_SOME_CONN='mysql://myname:mypassword@myhost.com?this_param=some+val&that_param=other+val%2A'

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

# MongoDB cluster
docker exec -it mongo1 mongosh --eval "rs.initiate({
 _id: \"myReplicaSet\",
 members: [
   {_id: 0, host: \"mongo1\"},
   {_id: 1, host: \"mongo2\"},
   {_id: 2, host: \"mongo3\"}
 ]
})"

# Qdrant Certification
mkcert -install
mkcert localhost 127.0.0.1 ::1

# Create a collection with default dense vector
curl  -X PUT \
  'http://localhost:6333/collections/collection_name' \
  --header 'api-key: <api-key-value>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "vectors": {
    "size": 384,
    "distance": "Cosine"
  }
}'

# Create a collection with named dense and sparse vectors
curl  -X PUT \
  'https://localhost:6333/collections/article_collection' \
  --header 'api-key: Test1234567890' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "vectors": {
    "dense-vector-name": {
      "size": 1536,
      "distance": "Cosine"
    },
    "sparse_vectors": {
      "sparse-vector-name": {
        "index": {
          "on_disk": true
        }
      }
    }
  }
}'

## DBT setup
docker pull ghcr.io/dbt-labs/<db_adapter_name>:<version_tag>
docker run \
--network=host \
--mount type=bind,source=path/to/project,target=/usr/app \
--mount type=bind,source=path/to/profiles.yml,target=/root/.dbt/profiles.yml \
<dbt_image_name> \
ls
