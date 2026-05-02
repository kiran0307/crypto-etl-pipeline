import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


def upload_file_to_adls(local_file_path, blob_path):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")

    if not connection_string or not container_name:
        raise ValueError(
            "Missing Azure Storage configuration. "
            "Check AZURE_STORAGE_CONNECTION_STRING and AZURE_CONTAINER_NAME in .env."
        )

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_path
    )

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    logging.info(f"Uploaded {local_file_path} to ADLS path: {blob_path}")