import json
import dataclasses
from dataclasses import dataclass


@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    tip_amount: float
    total_amount: float
    lpep_pickup_datetime: str  # epoch milliseconds
    lpep_dropoff_datetime: str
    passenger_count: float


def ride_from_row(row):
    return Ride(
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        trip_distance=float(row['trip_distance']),
        tip_amount=float(row['tip_amount']),
        total_amount=float(row['total_amount']),
        lpep_pickup_datetime=str(row['lpep_pickup_datetime'].timestamp() * 1000),
        lpep_dropoff_datetime=str(row['lpep_dropoff_datetime'].timestamp() * 1000),
        passenger_count=float(row['passenger_count'])
    )


def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)

def ride_serializer(ride):
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')