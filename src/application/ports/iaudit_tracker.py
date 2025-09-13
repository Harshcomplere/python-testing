from abc import ABC, abstractmethod
from datetime import datetime

class IAuditTracker(ABC):
    @abstractmethod
    def log_run(self, pipeline_id: str, status: str, timestamp: datetime):
        pass

    @abstractmethod
    def log_run_message(self, message: str):
        pass