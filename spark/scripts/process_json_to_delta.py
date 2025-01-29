from pyspark.sql import SparkSession
from delta.tables import *

# Initialize Spark session with Delta Lake support
spark = SparkSession.builder \
    .appName("ProcessJSONToDelta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Read JSON file
json_path = "/path/to/data/large_file.json"
df = spark.read.json(json_path)

# Perform any necessary transformations
df_transformed = df.select("field1", "field2", "field3")  # Example transformation

# Write data to Delta Lake
delta_path = "/path/to/delta/table"
df_transformed.write.format("delta").mode("overwrite").save(delta_path)
