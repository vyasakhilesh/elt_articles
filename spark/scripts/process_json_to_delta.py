from pyspark.sql import SparkSession
from delta.tables import *
import pyspark.sql.functions as F
from pyspark.sql.window import Window
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

def deduplicate_source_data(df):
    window_spec = Window.partitionBy("doi").orderBy(F.col("coreId").desc())
    deduplicated_df = df.withColumn("row_number", F.row_number().over(window_spec)).filter(F.col("row_number") == 1).drop("row_number")
    return deduplicated_df

def upsert_to_delta(spark, new_data):
    new_data = deduplicate_source_data(new_data)
    new_data.createOrReplaceTempView("new_data")
    
    # Merge new data with Delta table
    merge_query = """
        MERGE INTO old_data
        USING new_data
        ON old_data.coreId = new_data.coreId or old_data.doi = new_data.doi AND old_data.doi is not NULL
        WHEN MATCHED THEN
            UPDATE SET *
        WHEN NOT MATCHED THEN
            INSERT *
    """
    spark.sql(merge_query)

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
    # Check if Delta table exists
    if os.path.exists(delta_table_path):
        delta_table = DeltaTable.forPath(spark, delta_table_path)
    else:
        # If Delta table does not exist, create it from the initial JSON data
        df = spark.read.json(extract_path)
        df.write.format("delta").mode("overwrite").save(delta_table_path)
        delta_table = DeltaTable.forPath(spark, delta_table_path)

    # Read JSON files and filter incremental data
    json_df = read_json_files_to_df(spark, extract_path)
    json_df = json_df.repartition(10)
    # incremental_data = json_df.filter(json_df["last_updated"] > last_ingestion_time)

    # Write incremental data to Delta Lake
    # write_to_delta(json_df, delta_table_path)
    batch_size = 10000
    old_data = delta_table.toDF()
    old_data.createOrReplaceTempView("old_data")
    # Process data in batches
    for i in range(0, json_df.count(), batch_size):
        batch = json_df.limit(batch_size).offset(i)
        upsert_to_delta(spark, batch)

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
