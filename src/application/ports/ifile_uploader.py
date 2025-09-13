from abc import ABC, abstractmethod

class IFileUploader(ABC):
    @abstractmethod
    def upload(self, path: str, metadata: dict) -> str:
        pass