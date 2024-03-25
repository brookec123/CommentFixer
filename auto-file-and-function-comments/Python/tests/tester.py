"""
File Name: tester.py
File Author: Brooke Cronin
Course Code: CSCN71030 Group 4
Description: 
"""
class Person:
    """
    Class Name: Person
    Class Author: Brooke Cronin
    Description: 
    """
    def __init__(self, name) -> None:
        """
        Description: Written by: Brooke Cronin
        ### Parameters
        - Not Specified
        ### Returns
        - Not Specified
        """
        self.name = name
        
class Teacher(Person):
    """
    Class Name: Teacher
    Class Author: Brooke Cronin
    Description: 
    """
    def __init__(self, name, subject) -> None:
        """
        Description: Written by: Brooke Cronin
        ### Parameters
        - Not Specified
        ### Returns
        - Not Specified
        """
        super().__init__(name)
        self.subject = subject
