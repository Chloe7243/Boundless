import os
import json
from typing import Optional
from dotenv import load_dotenv
from utils.format_data import RawPassportRow
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError


from constants.urls import STORAGE_PREFIX

load_dotenv()

connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
container_name = "passport-data"
_service = BlobServiceClient.from_connection_string(conn_str=connection_string)
_container = _service.get_container_client(container_name)

LATEST_BLOB = f"{STORAGE_PREFIX}/latest.json"


def upload(data: list[RawPassportRow]) -> None:
    """
    Archives the current latest blob under its original upload time,
    then replaces latest with the new raw CSV text.
    """
    text = json.dumps(data)
    
    try:
        prev_latest = _container.download_blob(LATEST_BLOB)
        timestamp = prev_latest.properties.last_modified.strftime("%Y-%m-%dT%H-%M-%SZ")
        _container.upload_blob(
            name=f"{STORAGE_PREFIX}/{timestamp}.csv",
            data=prev_latest.readall(),
            overwrite=True,
        )
    except ResourceNotFoundError:
        pass

    _container.upload_blob(name=LATEST_BLOB, data=text, overwrite=True)


def retrieve(blob_name: Optional[str] = None) -> Optional[list[RawPassportRow]]:
    """
    Returns the blob's CSV text.
    If blob_name is None, retrieves latest.
    Returns None if the blob doesn't exist.
    """
    try:
        text = _container.download_blob(blob_name or LATEST_BLOB).readall()
        return json.loads(text)
    except ResourceNotFoundError:
        return None