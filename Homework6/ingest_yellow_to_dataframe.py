import pyspark
from pyspark.sql import SparkSession
import urllib.request

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet"
urllib.request.urlretrieve(url, "yellow_tripdata_2025-11.parquet")

df = spark.read.parquet("yellow_tripdata_2025-11.parquet")

df.show()
df.printSchema()

df.repartition(4).write.mode("overwrite").parquet("yellowtrip_data_parquet_partitioned")