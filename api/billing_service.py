from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient
import json

COSMOS_CONN_STR = "YourCosmosConnectionString"
COSMOS_DB = "billing"
COSMOS_CONTAINER = "records"

BLOB_CONN_STR = "YourBlobStorageConnectionString"
BLOB_CONTAINER_NAME = "billing-records"

def get_billing_record(record_id, timestamp_hint=None):
    try:
        cosmos = CosmosClient.from_connection_string(COSMOS_CONN_STR)
        db = cosmos.get_database_client(COSMOS_DB)
        container = db.get_container_client(COSMOS_CONTAINER)
        
        response = container.read_item(item=record_id, partition_key=record_id)
        return response
    except exceptions.CosmosResourceNotFoundError:
        # Fallback to Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
        blob_container = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        
        if not timestamp_hint:
            # Optional: if no hint provided, search all folders (less efficient)
            raise Exception("timestamp_hint required for cold storage lookup")
        
        month_folder = timestamp_hint[:7]
        blob_path = f"{month_folder}/{record_id}.json"
        
        blob_client = blob_container.get_blob_client(blob_path)
        blob_data = blob_client.download_blob().readall()
        record = json.loads(blob_data)
        return record

