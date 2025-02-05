from pyspark.sql import SparkSession
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import argparse
from pymongo import UpdateOne
import math

# Initialize Spark session with Delta Lake support

# Function to insert data into MongoDB in batches
def insert_data_in_batches(mongo_collection, dataframe, batch_size):
    for i in range(0, len(dataframe), batch_size):
        batch = dataframe[i:i+batch_size]
        requests = []
        for _, row in batch.iterrows():
            query = {"$or": [{"coreID": row["coreId"]}, {"doi": row["doi"]}]}
            update = {"$set": row.to_dict()}
            requests.append(UpdateOne(query, update, upsert=True))
        mongo_collection.bulk_write(requests)
        # mongo_collection.insert_many(batch.to_dict("records"))

def delta_to_mongodb(uri, delta_table_path):
    spark = SparkSession.builder \
        .appName("ProcessDeltaToMongoDB") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.3.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.sql.shuffle.partitions", 300) \
        .config("spark.databricks.delta.autoCompact.enabled", "true") \
        .config("spark.databricks.delta.autoCompact.maxFileSize", "32MB") \
        .config("spark.databricks.delta.autoCompact.minNumFiles", 3) \
        .getOrCreate()

    # Read data from Delta Lake
    df = spark.read.format("delta").load(delta_table_path)
    
    # Assuming there's a column 'timestamp' for incremental batch
    # latest_timestamp = df.agg(max_("timestamp")).collect()[0][0]

    # Read only new data (assuming timestamp column for incremental load)
    # new_data = df.filter(col("timestamp") > latest_timestamp)
    
    # Repartition to manage memory usage more efficiently
    # Repartition DataFrame based on the number of cores in your cluster
    total_size_in_bytes = df.rdd.map(lambda row: len(str(row))).sum()
    target_partition_size_in_bytes = 128 * 1024 * 1024  # Target partition size of 128 MB
    num_partitions = math.ceil(total_size_in_bytes / target_partition_size_in_bytes)
    df = df.repartition(num_partitions)

    # Perform any necessary transformations
    # df_transformed = df.select("field1", "field2", "field3")  # Example transformation
    
    try:
        # Establish a connection to the MongoDB server with authentication
        client = MongoClient(uri)
        # client.admin.command('ping')  # Verify the connection

        # Select the database and collection
        db = client['article_db']
        collection = db['article_collection']

        # Prepare the data to be inserted
        new_data_pd = df.toPandas()
        batch_size = 10000
        insert_data_in_batches(collection, new_data_pd, batch_size)

        spark.stop()

    except OperationFailure as e:
        print(f"Operation failed: {e}")
    finally:
        # Step 5: Close the connection
        spark.stop()
        client.close()

def main(uri, delta_table_path):
    delta_to_mongodb(uri, delta_table_path)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON from zip and incrementally load into Delta Lake")
    parser.add_argument("extract_path", help="Folder to extract JSON files")
    parser.add_argument("delta_table_path", help="Delta Lake table path")

    # args = parser.parse_args()

    # main(args.zip_file_path, args.extract_to_folder, args.delta_table_path)
    main("mongodb://root:example@mongodb:27017/?directConnection=true",
        "/opt/spark/data/delta_table/core_data")
    # uri = "mongodb://mongoadmin:password@localhost:27017/?directConnection=true"
