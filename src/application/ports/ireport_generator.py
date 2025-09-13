from abc import ABC, abstractmethod

class IReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: list[dict]) -> str:
        """Generates a CSV string from data"""
        pass