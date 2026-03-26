import sys
from datetime import datetime
from pathlib import Path
import psycopg2
sys.path.insert(0, str(Path(__file__).parent.parent))
import json
from kafka import KafkaConsumer
from homework_models import ride_deserializer
from dataclasses import dataclass


@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    tip_amount: float
    total_amount: float
    lpep_pickup_datetime: int  # epoch milliseconds
    lpep_dropoff_datetime: int  # epoch milliseconds
    passenger_count: int



server = 'localhost:9092'
topic_name = 'green-rides'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='rides-console',
    value_deserializer=ride_deserializer
)

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres'
)
conn.autocommit = True
cur = conn.cursor()

print(f"Listening to {topic_name}...")

count = 0
for message in consumer:
    ride = message.value
    pickup_dt = datetime.fromtimestamp(float(ride.lpep_pickup_datetime) / 1000)
    dropoff_dt = datetime.fromtimestamp(float(ride.lpep_dropoff_datetime) / 1000)
    print(f"Received: PU={ride.PULocationID}, DO={ride.DOLocationID}, "
          f"distance={ride.trip_distance}, tip={ride.tip_amount}, amount=${ride.total_amount:.2f}, "
          f"pickup={pickup_dt}, dropoff={dropoff_dt}")
    cur.execute(
        """INSERT INTO homework_greentrip_events
           (PULocationID, DOLocationID, trip_distance, tip_amount, total_amount, lpep_pickup_datetime, lpep_dropoff_datetime, passenger_count)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (ride.PULocationID, ride.DOLocationID,
         ride.trip_distance, ride.tip_amount, ride.total_amount, pickup_dt, dropoff_dt, ride.passenger_count)
    )
    #count += 1
    #if count >= 10:
        #print(f"\n... received {count} messages so far (stopping after 10 for demo)")
        #break

consumer.close()