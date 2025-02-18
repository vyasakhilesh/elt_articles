from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue

def collection_exists(client, collection_name):
    collections = client.get_collections()
    return any(collection.name == collection_name for collection in collections.collections)


def create_collection_if_not_exists(client, collection_name):
    if not collection_exists(client, collection_name):
        client.create_collection(collection_name=collection_name,
                                 vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),)
        print(f'Collection "{collection_name}" created successfully.')
    else:
        print(f'Collection "{collection_name}" already exists.')

qdrant_client = QdrantClient(
    url="https://e918655e-5705-4103-9dab-4e053444e94c.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzQ3NjUzODg1fQ.TsIAOsbkDhAT3rEUOeOEUkigw_-dI1Si0ugw8Jv4x2s",
)

qdrant_collection_name = "article_collection"
# Create the collection if it doesn't exist
create_collection_if_not_exists(qdrant_client, qdrant_collection_name)
print(qdrant_client.get_collections())