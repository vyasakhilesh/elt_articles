from pyspark.sql import SparkSession
from pymongo import MongoClient
import argparse

# Initialize Spark session with Delta Lake support

def delta_to_mongodb(delta_table_path, uri):
    spark = SparkSession.builder \
        .appName("ProcessDeltaToMongoDB") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.3.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    # Read data from Delta Lake
    df = spark.read.format("delta").load(delta_table_path)

    # Perform any necessary transformations
    # df_transformed = df.select("field1", "field2", "field3")  # Example transformation

    # Convert DataFrame to Pandas for MongoDB insertion
    pandas_df = df.toPandas()

    # Insert data into MongoDB
    client = MongoClient(uri)
    db = client.my_database
    collection = db.my_collection
    collection.insert_many(pandas_df.to_dict("records"))

def main(uri, delta_table_path):
    delta_to_mongodb(delta_table_path, uri)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON from zip and incrementally load into Delta Lake")
    parser.add_argument("extract_path", help="Folder to extract JSON files")
    parser.add_argument("delta_table_path", help="Delta Lake table path")

    # args = parser.parse_args()

    # main(args.zip_file_path, args.extract_to_folder, args.delta_table_path)
    main("mongodb://localhost:27017/",
        "/opt/spark/data/delta_table/core_data")
