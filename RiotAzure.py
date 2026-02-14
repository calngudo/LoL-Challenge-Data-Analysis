import os
import json
from dotenv import load_dotenv
import requests
import sqlalchemy
import pyodbc
import pandas as pd
import RiotApi
from azure.storage.blob import BlobServiceClient

load_dotenv()

class AzureBlobStorage:
    def __init__(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("AZURE_CONTAINER_NAME")
        if not connection_string or not container_name:
            raise ValueError("Azure Blob Storage env vars not set")
        service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_client = service_client.get_container_client(
            container_name
        )
    
    def upload_json(self, data: dict, blob_path: str):
        json_bytes = json.dumps(data).encode("utf-8")
        self.container_client.upload_blob(
            name=blob_path,
            data=json_bytes,
            overwrite=True
        )

blob_client = AzureBlobStorage() 

server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

conn_str = (
    f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=no"
)
engine = sqlalchemy.create_engine(conn_str)


def fetch_and_store_match_history(puuid):
    match_ids = RiotApi.get_matchhistory(puuid, count=100)
    if match_ids:
        blob_path = f"raw/match_history/{puuid}.json"
        blob_client.upload_json(match_ids, blob_path)

def fetch_and_store_match(match_id):
    match_data = RiotApi.get_match_details(match_id)
    if match_data:
        blob_path = f"raw/matches/{match_id}.json"
        blob_client.upload_json(match_data, blob_path)

def upload_dataframe_to_sql(fullmatch, table_name='match_data'):
    fullmatch.to_sql(table_name, con=engine, if_exists='append', index=False)
