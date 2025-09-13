from src.application.ports.iblob_storage_client import IBlobStorageClient

class BlobUploaderService:
    def __init__(self, blob_client: IBlobStorageClient):
        self.blob_client = blob_client

    def upload_patient_file(self, file_path: str) -> str:
        container = "patient-data"
        success = self.blob_client.upload_file(file_path, container)

        if success:
            return "Upload successful"
        else:
            return "Upload failed"