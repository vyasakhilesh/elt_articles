from pyspark.sql import SparkSession
from delta.tables import *
from delta import *
import argparse
import os


def find_json_files(extract_path):
    json_files = []
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

# Function to read JSON files and create DataFrame
def read_json_files_to_df(spark, extract_path):
    json_files = find_json_files(extract_path)
    df = spark.read.format('json').load(json_files)
    return df

 # Function to get last ingestion time from Delta Lake
def get_last_ingestion_time(spark, delta_table_path):
    if not DeltaTable.isDeltaTable(spark, delta_table_path):
        # If the table does not exist, return a default value
        return "2025-01-01 00:00:00"
    df = spark.read.format("delta").load(delta_table_path)
    last_ingestion_time = df.agg({"last_updated": "max"}).collect()[0][0]
    return last_ingestion_time

def transform_data(df):
    # df.select("field1", "field2", "field3")
    pass

def write_to_delta(df, delta_table_path):
    df.write.format("delta").mode("append").save(delta_table_path)
    print("Data written to Delta Lake successfully") 

def json_to_deltalake(delta_table_path, extract_path):
    # Initialize Spark session with Delta Lake support
    spark = SparkSession.builder \
        .appName("ProcessJSONToDelta") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.3.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    # Get last ingestion time from Delta Lake
    # last_ingestion_time = get_last_ingestion_time(spark, delta_table_path)

    # Read JSON files and filter incremental data
    json_df = read_json_files_to_df(spark, extract_path)
    # incremental_data = json_df.filter(json_df["last_updated"] > last_ingestion_time)

    # Write incremental data to Delta Lake
    write_to_delta(json_df, delta_table_path)

    # Perform any necessary transformations
    # df_transformed =   transform_data(df) # Example transformation

    # Write data to Delta Lake
    json_df.write.format("delta").mode("overwrite").save(delta_table_path)
    
    spark.stop()

def main(delta_table_path, extract_path):
    json_to_deltalake(delta_table_path, extract_path)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON from zip and incrementally load into Delta Lake")
    parser.add_argument("extract_path", help="Folder to extract JSON files")
    parser.add_argument("delta_table_path", help="Delta Lake table path")

    # args = parser.parse_args()

    # main(args.zip_file_path, args.extract_to_folder, args.delta_table_path)
    main("/opt/spark/data/delta_table/core_data",
         "/opt/spark/data/raw_data/extracted_data/resync_datadump_sample220218/", 
         )
