import pyspark
from pyspark.sql import SparkSession
import urllib.request

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
urllib.request.urlretrieve(url, "taxi_zone_lookup.csv")

df = spark.read \
    .option("header", "true") \
    .csv("taxi_zone_lookup.csv")

df.show()

df.write.parquet("zones")