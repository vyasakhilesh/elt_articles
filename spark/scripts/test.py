from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("SampleDataToMongoDB") \
    .config("spark.mongodb.output.uri", "mongodb://root:example@mongodb:27017/test_db.test_collection") \
    .getOrCreate()

# Create sample data
data = [
    ("Alice", 30),
    ("Bob", 25),
    ("Charlie", 35)
]

# Define schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# Create DataFrame
sample_df = spark.createDataFrame(data, schema)

# Show sample data
sample_df.show()

# Write data to MongoDB
sample_df.write \
    .format("mongo") \
    .mode("overwrite") \
    .save()

# Stop SparkSession
spark.stop()