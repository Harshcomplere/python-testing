
class Person():
    """A class representing a person with a name and age."""
    def __init__(self, person_name: str, person_age: int):
        self.person_name = person_name
        
    def get_age(self) -> int:
        """Get the age of the recipient"""
        return 18