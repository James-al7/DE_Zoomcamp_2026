Question 2.

Question 3.
select * from homework_greentrip_events WHERE trip_distance > 5;

Question 4.
SELECT PULocationID, num_trips
FROM green_rides
ORDER BY num_trips DESC
LIMIT 3;

Question 5.
SELECT 
     PULocationID,
     window_start,
     window_end,
     num_trips,
     total_revenue
 FROM green_rides_window
 ORDER BY num_trips DESC
 LIMIT 1;


Question 6.
SELECT
    window_start,
    window_end,
    total_tip
FROM green_rides_hourly_tips
WHERE total_tip = (SELECT MAX(total_tip) FROM green_rides_hourly_tips);
