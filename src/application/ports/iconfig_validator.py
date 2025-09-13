from abc import ABC, abstractmethod

class IConfigValidator(ABC):
    @abstractmethod
    def validate(self, config: dict) -> bool:
        pass