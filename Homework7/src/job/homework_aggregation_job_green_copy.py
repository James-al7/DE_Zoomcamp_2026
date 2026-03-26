from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

def create_events_source_kafka(t_env):
    table_name = "events"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
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
            'topic' = 'greenrides',
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

def create_events_sink(t_env):
    table_name = "greenrides_db"
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            window_start TIMESTAMP(3),
            PULocationID INT,
            num_trips BIGINT,
            total_revenue DOUBLE,
            PRIMARY KEY (window_start, PULocationID) NOT ENFORCED
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
    # Setup Flink environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        source_table = create_events_source_kafka(t_env)
        sink_table = create_events_sink(t_env)

        # Debug: print aggregated results before writing to JDBC


        # Write to JDBC
        t_env.execute_sql(f"""
            INSERT INTO {sink_table}
            SELECT
                window_start,
                PULocationID,
                COUNT(*) AS num_trips,
                SUM(IFNULL(total_amount,0)) AS total_revenue
            FROM TABLE(
                TUMBLE(
                    TABLE {source_table},
                    DESCRIPTOR(event_timestamp),
                    INTERVAL '5' MINUTES
                )
            )
            GROUP BY window_start, PULocationID
        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))

if __name__ == "__main__":
    log_aggregation()