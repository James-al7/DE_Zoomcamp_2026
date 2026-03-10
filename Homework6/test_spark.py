import pyspark
from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("test") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
print("Spark UI:", spark.sparkContext.uiWebUrl)

df = spark.range(10)
df.show()
time.sleep(600)


#spark.stop()