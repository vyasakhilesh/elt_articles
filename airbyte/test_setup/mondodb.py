
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# mongodb+srv://akhvyas:tqs1VstkJX8KdAQl@cluster0.ay0tl.mongodb.net/

uri = "mongodb+srv://akhvyas:a5T83xYNvCfxynwC@cluster0.ay0tl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Select the database and collection
db = client['article_db']
collection = db['article_collection']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)