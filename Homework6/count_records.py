import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("test") \
    .getOrCreate()

df_yellowdata = spark.read.parquet("yellowtrip_data_parquet_partitioned")

df_yellowdata.show()
print(df_yellowdata.columns)
df_yellowdata.printSchema()
#df_yellowdata.registerTempTable('Nov2025_Yellow')


df_yellowdata.createOrReplaceTempView('Nov2025_Yellow')
spark.sql(""" SELECT COUNT(1) FROM Nov2025_Yellow WHERE DAY(tpep_pickup_datetime) = 15 """).show()