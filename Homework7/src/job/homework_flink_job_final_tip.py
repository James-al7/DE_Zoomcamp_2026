from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

def create_events_source_kafka(t_env):
    table_name = "events"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            lpep_pickup_datetime STRING,

            -- Event-time parsing
            event_timestamp AS TO_TIMESTAMP_LTZ(
                CAST(lpep_pickup_datetime AS DOUBLE), 3
            ),

            -- Watermark for late events
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-rides',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'flink-consumer',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json',
            'json.ignore-parse-errors' = 'true',
            'json.fail-on-missing-field' = 'false'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def create_tip_sink(t_env):
    table_name = "green_rides_hourly_tips"
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            total_tip DOUBLE,
            PRIMARY KEY (window_start) NOT ENFORCED
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

def log_hourly_tips():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        source_table = create_events_source_kafka(t_env)
        sink_table = create_tip_sink(t_env)

        # Aggregate tip_amount per 1-hour tumbling window
        t_env.execute_sql(f"""
            INSERT INTO {sink_table}
            SELECT
                window_start,
                window_end,
                SUM(IFNULL(tip_amount,0)) AS total_tip
            FROM TABLE(
                TUMBLE(
                    TABLE {source_table},
                    DESCRIPTOR(event_timestamp),
                    INTERVAL '1' HOUR
                )
            )
            GROUP BY window_start, window_end
        """).wait()

    except Exception as e:
        print("Writing hourly tip aggregation to PostgreSQL failed:", str(e))

if __name__ == "__main__":
    log_hourly_tips()