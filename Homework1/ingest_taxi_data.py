import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click

#Source URL: 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
#prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
#url = f'{prefix}/green_tripdata_2025-11.parquet'


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='trip_data', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--target-table', default='green_taxi_data', help='Target table name')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table):

    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{prefix}/green_tripdata_{year}-{month:02d}.parquet'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_load_data = pd.read_parquet(url)

    df_load_data.to_sql(name = target_table, con = engine, if_exists = 'replace')


if __name__ == '__main__':
    run()