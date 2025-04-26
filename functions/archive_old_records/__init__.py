import datetime
import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

COSMOS_CONN_STR = "YourCosmosConnectionString"
COSMOS_DB = "billing"
COSMOS_CONTAINER = "records"

BLOB_CONN_STR = "YourBlobStorageConnectionString"
BLOB_CONTAINER_NAME = "billing-records"

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow()
    logging.info(f"Python timer trigger function ran at {utc_timestamp}")

    cosmos = CosmosClient.from_connection_string(COSMOS_CONN_STR)
    database = cosmos.get_database_client(COSMOS_DB)
    container = database.get_container_client(COSMOS_CONTAINER)

    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    blob_container = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

    cutoff_date = (utc_timestamp - datetime.timedelta(days=90)).isoformat()

    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff_date}'"
    old_records = container.query_items(query=query, enable_cross_partition_query=True)

    for record in old_records:
        record_id = record['id']
        month_folder = record['timestamp'][:7]
        blob_path = f"{month_folder}/{record_id}.json"
        
        # Upload record to blob
        blob_container.upload_blob(blob_path, json.dumps(record), overwrite=True)

        # Only after successful upload, delete from Cosmos DB
        container.delete_item(record, partition_key=record['partitionKey'])

    logging.info("Archival process completed.")
