from abc import ABC, abstractmethod

class INotificationService(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str):
        """Send a notification message to the recipient"""
        pass

    @abstractmethod
    def get_age(self) -> int:
        """Get the age of the recipient"""
        return 18