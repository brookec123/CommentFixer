class Person:
    def __init__(self, name) -> None:
        self.name = name
        
class Teacher(Person):
    def __init__(self, name, subject) -> None:
        super().__init__(name)
        self.subject = subject
