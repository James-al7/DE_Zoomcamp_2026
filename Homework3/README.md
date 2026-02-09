# create external table from parquet files stored in gcs bucket
CREATE OR REPLACE EXTERNAL TABLE `zoom26_module3_yellowtaxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://zoomcamp_module3_yellowtaxi/yellow_tripdata_2024-*.parquet']
);


# create nonpartitioned materialized table from external table 
CREATE OR REPLACE TABLE zoom26_module3_yellowtaxi.yellow_tripdata_nonpartitioned
AS
SELECT * FROM de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.external_yellow_tripdata

# create partitioned table from external table 

CREATE OR REPLACE TABLE zoom26_module3_yellowtaxi.yellow_tripdata_partitioned
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID 
AS
SELECT * FROM de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.external_yellow_tripdata


# Homework Questions

# Question 1:
SELECT COUNT(1) FROM `de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.yellow_tripdata_nonpartitioned` 


# Question 2:
SELECT COUNT(DISTINCT PULocationID) FROM `de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.yellow_tripdata_nonpartitioned` 
SELECT COUNT(DISTINCT PULocationID) FROM `de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.external_yellow_tripdata` 

# Question 3:
SELECT PULocationID FROM `de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.yellow_tripdata_nonpartitioned` 

SELECT PULocationID, DOLocationID FROM `de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.yellow_tripdata_nonpartitioned` 

# Question 4:
SELECT COUNT(1) FROM `de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.yellow_tripdata_nonpartitioned` WHERE fare_amount = 0; 


# Question 5:
CREATE OR REPLACE TABLE zoom26_module3_yellowtaxi.yellow_tripdata_partitioned
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID 
AS
SELECT * FROM de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.external_yellow_tripdata

# Question 6:
SELECT DISTINCT(VendorID) FROM de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.yellow_tripdata_partitioned
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'

SELECT DISTINCT(VendorID) FROM de-zoomcamp2026-486215.zoom26_module3_yellowtaxi.yellow_tripdata_nonpartitioned
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'

