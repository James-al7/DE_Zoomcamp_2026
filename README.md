# DE_Zoomcamp_2026
Code submissions for homework and other assignments. 

Question 3:

SELECT *
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01' AND trip_distance <= 1.0
-8007

Question 4:

select max(trip_distance) from green_taxi_data where lpep_pickup_datetime >= '2025-11-14' AND lpep_pickup_datetime < '2025-11-15';
-88.03
select max(trip_distance) from green_taxi_data where lpep_pickup_datetime >= '2025-11-20' AND lpep_pickup_datetime < '2025-11-21';

select max(trip_distance) from green_taxi_data where lpep_pickup_datetime >= '2025-11-23' AND lpep_pickup_datetime < '2025-11-24';

select max(trip_distance) from green_taxi_data where lpep_pickup_datetime >= '2025-11-25' AND lpep_pickup_datetime < '2025-11-26';

Question 5:

SELECT
  "PULocationID",
  SUM(total_amount) AS max_total_amount
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-18'
  AND lpep_pickup_datetime <  '2025-11-19'
GROUP BY "PULocationID"
ORDER BY max_total_amount DESC
-East Harlem N

Question 6

SELECT max(tip_amount) as max_tip, "DOLocationID"
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime <  '2025-12-01'
  AND "PULocationID" = 74
 GROUP BY "DOLocationID"
 ORDER BY max_tip DESC
 -Yorkville West








