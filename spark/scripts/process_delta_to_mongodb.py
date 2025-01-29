from pyspark.sql import SparkSession
from pymongo import MongoClient

# Initialize Spark session with Delta Lake support
spark = SparkSession.builder \
    .appName("ProcessDeltaToMongoDB") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Read data from Delta Lake
delta_path = "/path/to/delta/table"
df = spark.read.format("delta").load(delta_path)

# Perform any necessary transformations
df_transformed = df.select("field1", "field2", "field3")  # Example transformation

# Convert DataFrame to Pandas for MongoDB insertion
pandas_df = df_transformed.toPandas()

# Insert data into MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.my_database
collection = db.my_collection
collection.insert_many(pandas_df.to_dict("records"))
