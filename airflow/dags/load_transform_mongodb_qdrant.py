import uuid
from pymongo import MongoClient
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import numpy as np

# Function to check if a point exists in Qdrant based on coreID or doi
def point_exists(qdrant_client, qdrant_collection_name, coreId, doi):
    
    # Validate coreId and doi
    if coreId is None:
        coreId = ""
    if doi is None:
        doi = ""

    query_filter=models.Filter(
        should=[
            models.FieldCondition(
                key="coreId",
                match=models.MatchValue(
                    value=coreId,
                ),
            ),
            models.FieldCondition(
                key="doi",
                match=models.MatchValue(
                    value=doi,
                ),
            ),
        ]
    )
    
    result = qdrant_client.search(qdrant_collection_name, query_vector=[0.1, 0.2, 0.1, 0.9, 0.7], query_filter=query_filter, limit=1)
    if result:
        return True
    return False

# Function to insert or update data in Qdrant in batches
def upsert_data_in_batches(qdrant_client, qdrant_collection_name, data, batch_size):
    points = []
    for doc in data:
        coreId = doc.get("coreId")
        doi = doc.get("doi")
        vector = np.random.rand(5) # doc["vector"] # fix this
        payload = doc.get("payload", {"coreId":coreId, "doi":doi})

        if not point_exists(qdrant_client, qdrant_collection_name, coreId, doi):
            point_id = str(uuid.uuid4())
            points.append(PointStruct(id=point_id, vector=vector, payload=payload))
    if points:
        qdrant_client.upsert(collection_name=qdrant_collection_name, points=points)
        print(f"Upserted {len(points)} points to Qdrant.") # 21124
    else:
        print(f"Upserted {len(points)} points to Qdrant.")
        
def collection_exists(client, collection_name):
    collections = client.get_collections()
    return any(collection.name == collection_name for collection in collections.collections)


def create_collection_if_not_exists(client, collection_name):
    if not collection_exists(client, collection_name):
        client.create_collection(collection_name=collection_name,
                                 vectors_config=models.VectorParams(size=5, distance=models.Distance.COSINE),)
        print(f'Collection "{collection_name}" created successfully.')
    else:
        print(f'Collection "{collection_name}" already exists.')

# Process data in batches
def load_transform_mongodb_qdrant():
    # Initialize MongoDB client
    mongo_client = MongoClient("mongodb://root:example@mongodb:27017/?directConnection=true")
    mongo_db = mongo_client["article_db"]
    mongo_collection = mongo_db["article_collection"]

    # Initialize Qdrant client
    qdrant_client = QdrantClient("http://qdrant:6333")
    qdrant_collection_name = "article_collection"
    # Create the collection if it doesn't exist
    create_collection_if_not_exists(qdrant_client, qdrant_collection_name)
    batch_size = 10000  # Adjust batch size as needed
    cursor = mongo_collection.find({})
    batch = []
    for doc in cursor:
        batch.append(doc)
        if len(batch) >= batch_size:
            upsert_data_in_batches(qdrant_client, qdrant_collection_name, batch, batch_size)
            batch = []

    # Upsert any remaining documents in the last batch
    if batch:
        upsert_data_in_batches(qdrant_client, qdrant_collection_name,batch, batch_size)
    

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=30),
}

dag = DAG('load_transform_mongodb_qdrant', default_args=default_args, schedule_interval=None)

load_transform_mongodb_qdrant_task = PythonOperator(
    task_id='load_transform_mongodb_qdrant',
    python_callable=load_transform_mongodb_qdrant,
    dag=dag,
)

load_transform_mongodb_qdrant_task




