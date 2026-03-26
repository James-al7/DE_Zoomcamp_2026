from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_events_source_kafka(t_env):
    table_name = "source_events"

    source_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            lpep_pickup_datetime STRING,
            lpep_dropoff_datetime STRING,
            passenger_count DOUBLE,

            -- Proper event time parsing
            event_timestamp AS TO_TIMESTAMP_LTZ(CAST(lpep_pickup_datetime AS DOUBLE),3),

            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '10' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'green-rides',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json',
            'json.ignore-parse-errors' = 'true'
        );
    """

    t_env.execute_sql(source_ddl)
    return table_name


def create_events_sink(t_env):
    table_name = 'processed_events_homework'

    sink_ddl = f"""
        CREATE TABLE {table_name} (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            PULocationID INT,
            DOLocationID INT,

            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            passenger_count DOUBLE,

            PRIMARY KEY (window_start, window_end, PULocationID, DOLocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """

    t_env.execute_sql(sink_ddl)
    return table_name


def log_aggregation():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        source_table = create_events_source_kafka(t_env)
        sink_table = create_events_sink(t_env)

        t_env.execute_sql(f"""
            INSERT INTO {sink_table}
            SELECT
                window_start,
                window_end,
                PULocationID,
                DOLocationID,

                SUM(trip_distance) AS trip_distance,
                SUM(tip_amount) AS tip_amount,
                SUM(total_amount) AS total_amount,
                SUM(passenger_count) AS passenger_count

            FROM TABLE(
                TUMBLE(TABLE {source_table}, DESCRIPTOR(event_timestamp), INTERVAL '1' HOUR)
            )
            GROUP BY
                window_start,
                window_end,
                PULocationID,
                DOLocationID
        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))


if __name__ == '__main__':
    log_aggregation()