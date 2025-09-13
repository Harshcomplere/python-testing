from abc import ABC, abstractmethod

class IDataQualityChecker(ABC):
    @abstractmethod
    def check(self, file_path: str) -> dict:
        """
        Analyzes the file for quality issues. 
        Returns a dict like {'passed': bool, 'issues': list[str]}
        """
        pass