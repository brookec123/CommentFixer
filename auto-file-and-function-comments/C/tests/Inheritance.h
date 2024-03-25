#pragma once
#include <string>

class Person
{
    std::string name;
};

class Employee
{
    int id;
};

class Teacher : public Person, public Employee
{
    std::string courseName;
};