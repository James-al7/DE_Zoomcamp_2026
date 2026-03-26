from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_events_source_homework(t_env):
    table_name = "source_events_homework"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            lpep_pickup_datetime STRING,
            lpep_dropoff_datetime STRING,
            passenger_count DOUBLE,
            event_timestamp AS TO_TIMESTAMP_LTZ(CAST(lpep_pickup_datetime AS BIGINT), 3),

            WATERMARK for event_timestamp as event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'green-rides',
            'scan.startup.mode' = 'earliest-offset',
    		'json.fail-on-missing-field' = 'false',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json',
            'json.ignore-parse-errors' = 'true'
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name


def create_events_sink_homework(t_env):
    table_name = 'processed_events_homework'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
			total_amount DOUBLE,
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            passenger_count DOUBLE,
            window_start TIMESTAMP(3),
            windows_end TIMESTAMP(3),
            PRIMARY KEY (PULocationID, DOLocationID, window_start) NOT ENFORCED



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
        source_table = create_events_source_homework(t_env)
        aggregated_table = create_events_sink_homework(t_env)

        t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
        SELECT
            PULocationID,
            DOLocationID,
            SUM(trip_distance) AS trip_distance,
            SUM(tip_amount) AS tip_amount,
            SUM(total_amount) AS total_amount,
            MAX(lpep_pickup_datetime) AS lpep_pickup_datetime,
            MAX(lpep_dropoff_datetime) AS lpep_dropoff_datetime,
            SUM(passenger_count) AS passenger_count
        FROM TABLE(
            TUMBLE(TABLE {source_table}, DESCRIPTOR(event_timestamp), INTERVAL '1' HOUR)
        )
        GROUP BY
			PULocationID,
            DOLocationID,
            window_start,
            window_end


        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))


if __name__ == '__main__':
    log_aggregation()