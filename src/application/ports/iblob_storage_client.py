from abc import ABC, abstractmethod

class IBlobStorageClient(ABC):
    @abstractmethod
    def upload_file(self, file_path: str, container_name: str) -> bool:
        pass