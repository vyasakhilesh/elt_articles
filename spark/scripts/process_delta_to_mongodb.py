from pyspark.sql import SparkSession
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import argparse

# Initialize Spark session with Delta Lake support

def delta_to_mongodb(uri, delta_table_path):
    spark = SparkSession.builder \
        .appName("ProcessDeltaToMongoDB") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.3.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    # Read data from Delta Lake
    # df = spark.read.format("delta").load(delta_table_path)

    # Perform any necessary transformations
    # df_transformed = df.select("field1", "field2", "field3")  # Example transformation

    # Convert DataFrame to Pandas for MongoDB insertion
    # pandas_df = df.toPandas()
    
    try:
    # Step 1: Establish a connection to the MongoDB server with authentication
        print(uri)
        client = MongoClient(uri)
        # client.admin.command('ping')  # Verify the connection

        # Step 2: Select the database and collection
        db = client['test_db']
        collection = db['test_collection']

        # Step 3: Prepare the data to be inserted
        data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30
        }

        # Step 4: Insert the data into the collection
        result = collection.insert_one(data)
        # collection.insert_many(pandas_df.to_dict("records"))

        # Print the ID of the inserted document
        print(f"Data inserted with id {result.inserted_id}")

        # Fetch all documents
        documents = collection.find()

        for doc in documents:
            print(doc)

    except OperationFailure as e:
        print(f"Operation failed: {e}")
    finally:
        # Step 5: Close the connection
        client.close()

def main(uri, delta_table_path):
    delta_to_mongodb(uri, delta_table_path)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON from zip and incrementally load into Delta Lake")
    parser.add_argument("extract_path", help="Folder to extract JSON files")
    parser.add_argument("delta_table_path", help="Delta Lake table path")

    # args = parser.parse_args()

    # main(args.zip_file_path, args.extract_to_folder, args.delta_table_path)
    main("mongodb://root:example@localhost:27017/?directConnection=true",
        "/opt/spark/data/delta_table/core_data")
    # uri = "mongodb://mongoadmin:password@localhost:27017/?directConnection=true"
