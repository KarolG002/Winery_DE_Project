import pandas as pd
from sqlalchemy import create_engine
from google.cloud import bigquery
import pandas_gbq
import logging
from prefect import flow, task
from prefect.client.schemas.schedules import IntervalSchedule
from datetime import timedelta, datetime
from src.pipeline.credentials import credentials
import os

# Database connection parameters
db_host = 'localhost'
db_user = 'root'
db_pass = 'root'
db_name = 'winedb'
GCP_credentials = credentials
dataset_id = "wine_dataset"
project_id = "dwh-terraform-gcp"
offset_file = 'src/pipeline/offset.txt'


connection_string = f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}'

engine = create_engine(connection_string)

@task
def read_table(table_name: str, engine, offset: int, limit: int) -> pd.DataFrame:
    query = f'SELECT * FROM {table_name} OFFSET {offset} LIMIT {limit}'
    return pd.read_sql(query, engine)

# Function to merge chunks of tables
@task
def merge_tables(engine, offset: int, limit: int) -> pd.DataFrame:
    tables = ['red_wines', 'rose_wines', 'sparkling_wines', 'white_wines']
    dataframes = [read_table(table, engine, offset, limit) for table in tables]
    merged_df = pd.concat(dataframes, ignore_index=True)
    if not merged_df.empty:
        merged_df.drop(columns=['id'], inplace=True)
    return merged_df

# Function to upload a DataFrame to BigQuery
@task
def upload_to_bigquery(table: pd.DataFrame, table_name: str, dataset_id: str, project_id: str, GCP_credentials):
    pandas_gbq.context.credentials = GCP_credentials
    try:
        pandas_gbq.to_gbq(table, f"{dataset_id}.{table_name}", project_id=project_id, if_exists='append')
        logging.info(f"Successfully uploaded {table_name} to BigQuery.")
    except ValueError as e:
        logging.error(f"Value error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

@task
def read_offset(file_path: str) -> int:
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as f:
        return int(f.read().strip())

@task
def write_offset(file_path: str, offset: int):
    with open(file_path, 'w') as f:
        f.write(str(offset))

@flow
def load_flow():
    limit = 1000
    offset = read_offset(offset_file)
    logging.info(f"Reading chunk from offset {offset}")
    chunk_df = merge_tables(engine, offset, limit)
    if not chunk_df.empty:
        upload_to_bigquery(chunk_df, 'merged_wines', dataset_id, project_id, GCP_credentials)
        offset += limit
        write_offset(offset_file, offset)
    else:
        logging.info("No more data to process.")


def main():
    schedule = IntervalSchedule(
        interval=timedelta(minutes=10), 
    )
    load_flow.serve(
        name="wine-collection-deployment",
        schedule=schedule
    )

if __name__ == "__main__":
    main()
