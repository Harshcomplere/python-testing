
import os
from azure.storage.blob import BlobServiceClient

class BlobUploader:
    def __init__(self, config):
        account_url = f"https://{os.getenv('BLOB_ACCOUNT_NAME')}.blob.core.windows.net"
        credential = os.getenv('BLOB_ACCESS_KEY')
        self.blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
        self.container = config['container']

    def upload_csv(self, filename: str, csv_bytes: bytes):
        blob_client = self.blob_service_client.get_blob_client(container=self.container, blob=filename)
        blob_client.upload_blob(csv_bytes, overwrite=True)
