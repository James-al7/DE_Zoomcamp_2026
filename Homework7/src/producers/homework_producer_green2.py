import dataclasses
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from kafka import KafkaProducer
from homework_models import Ride, ride_from_row, ride_serializer

# Download NYC green taxi trip data for October 2025
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
columns = ['PULocationID', 'DOLocationID', 'trip_distance', 'tip_amount', 'total_amount', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'passenger_count']
df = pd.read_parquet(url, columns=columns)

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=ride_serializer
)

t0 = time.time()

topic_name = 'greenrides'

for _, row in df.iterrows():
    ride = ride_from_row(row)
    producer.send(topic_name, value=ride)
    #print(f"Sent: {ride}")
    #time.sleep(0.01) Commenting these two lines out reduced the time taken from 547seconds to 6seconds approx.

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')