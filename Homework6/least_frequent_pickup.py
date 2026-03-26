import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import urllib.request

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("test") \
    .getOrCreate()

url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
urllib.request.urlretrieve(url, "taxi_zone_lookup.csv")

df_zonelookup = spark.read.option("header", "true").csv("taxi_zone_lookup.csv")


df_yellowdata = spark.read.parquet("yellowtrip_data_parquet_partitioned")
df_yellowdata.show()
print(df_yellowdata.columns)
df_yellowdata.printSchema()
#df_yellowdata.registerTempTable('Nov2025_Yellow')


df_yellowdata.createOrReplaceTempView('Nov2025_Yellow')
df_zonelookup.createOrReplaceTempView('Zonelookup')
#spark.sql("SELECT * FROM Zonelookup").show()

spark.sql(""" SELECT PULocationID,COUNT(*) FROM Nov2025_Yellow GROUP BY PULocationID ORDER BY COUNT(*) ASC """).show()

spark.sql(""" SELECT PULocationID, LocationID FROM Nov2025_Yellow JOIN Zonelookup ON Nov2025_Yellow.PULocationID = Zonelookup.LocationID GROUP BY PULocationID, LocationID ORDER BY COUNT(*) ASC """).show()

spark.sql("SELECT * FROM Zonelookup WHERE LocationID IN (84,105,5)").show()