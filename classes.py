from abc import ABC, abstractmethod

# Abstract class (Abstraction)
class Person(ABC):
    """Abstract class representing a person. Demonstrates abstraction."""
    def __init__(self, name):
        self._name = name  # Encapsulation: protected attribute

    @abstractmethod
    def show_info(self):
        """Abstract method to display information."""
        pass

    @property
    def name(self):
        return self._name

# Inheritance: Owner inherits from Person
class Owner(Person):
    """Class representing a pet owner. Demonstrates inheritance and encapsulation."""
    def __init__(self, name, phone, address):
        super().__init__(name)
        self._phone = phone
        self._address = address

    def show_info(self):
        """Shows the owner's information. Polymorphism in action."""
        return f"Name: {self._name}, Phone: {self._phone}, Address: {self._address}"

    def __str__(self):
        return self.show_info()

    # Encapsulation: getters
    @property
    def phone(self):
        return self._phone

    @property
    def address(self):
        return self._address

class Pet:
    """Class representing a pet. Demonstrates encapsulation and polymorphism."""
    def __init__(self, name, species, breed, age, owner):
        self._name = name
        self._species = species
        self._breed = breed
        self._age = age
        self._owner = owner  # Owner is an object of the Owner class
        self._consultations = []  # List to store consultations

    def add_consultation(self, consultation):
        """Adds a consultation to the pet's history."""
        self._consultations.append(consultation)

    def show_info(self):
        """Shows the pet's information and its owner. Polymorphism in action."""
        return (f"Pet: {self._name} | Species: {self._species} | "
                f"Breed: {self._breed} | Age: {self._age} years\nOwner: {self._owner}")

    def show_consultations(self):
        """Displays the consultation history of the pet."""
        if not self._consultations:
            return "No consultations registered for this pet."
        return "\n".join([str(c) for c in self._consultations])

    def __str__(self):
        # Polymorphism: custom __str__ method
        return self.show_info()

    # Encapsulation: getters
    @property
    def name(self):
        return self._name

    @property
    def consultations(self):
        return self._consultations

class Consultation:
    """Class representing a veterinary consultation. Demonstrates encapsulation."""
    def __init__(self, date, reason, diagnosis, pet):
        self._date = date
        self._reason = reason
        self._diagnosis = diagnosis
        self._pet = pet

    def __str__(self):
        return (f"Date: {self._date} | Reason: {self._reason} | "
                f"Diagnosis: {self._diagnosis}")

    # Encapsulation: getters
    @property
    def date(self):
        return self._date

    @property
    def reason(self):
        return self._reason

    @property
    def diagnosis(self):
        return self._diagnosis

    @property
    def pet(self):
        return self._pet

# Polymorphism example
def show_person(person):
    """Polymorphism example: accepts any object derived from Person."""
    print(person.show_info())