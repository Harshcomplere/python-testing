
class Person():
    """A class representing a person with a name and age."""
    def __init__(self, person_name: str, person_age: str):
        self.person_name = person_name
        self.person_age = person_age
        
    def get_name(self) -> str:
        return f"The Person name is {self.person_name}"
    
    def get_age(self) -> str:
        """Get the age of the recipient"""
        return f"{self.person_age}"