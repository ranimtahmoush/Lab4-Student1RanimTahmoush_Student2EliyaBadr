class Person:
    """
    A base class representing a person.

    :param name: The person's name.
    :type name: str
    :param age: The person's age.
    :type age: int
    :param email: The person's email address.
    :type email: str
    :raises ValueError: If the age is negative number or email format is invalid.
    """

    def __init__(self, name, age, email):
        Validator.validate_age(age)
        Validator.validate_email(email)
        self.name = name
        self.age = age
        self.__email = email

    def get_email(self):
        """
        Get the person's email.

        :return: The email address.
        :rtype: str
        """
        return self.__email

    def introduce(self):
        """
        Introduce the person with their personal details.

        :return: A tuple containing a formatted introduction message.
        :rtype: tuple
        """
        return ("This person's name is:", self.name,
                " and age is:", self.age,
                " and his email is:", self.__email)


class Student(Person):
    """
    A student, subclass of Person.

    :param name: Student's name.
    :type name: str
    :param age: Student's age.
    :type age: int
    :param email: Student's email address.
    :type email: str
    :param student_id: Unique student identifier.
    :type student_id: str
    """

    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Register a student for a course.

        :param course: Course object to register.
        :type course: Course
        """
        self.registered_courses.append(course)


class Instructor(Person):
    """
    An instructor, subclass of Person.

    :param name: Instructor's name.
    :type name: str
    :param age: Instructor's age.
    :type age: int
    :param email: Instructor's email address.
    :type email: str
    :param instructor_id: Unique instructor identifier.
    :type instructor_id: str
    """

    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assign a course to the instructor.

        :param course: Course object to assign.
        :type course: Course
        """
        self.assigned_courses.append(course)

    def get_name(self):
        """
        Get the instructor's name.

        :return: Instructor name.
        :rtype: str
        """
        return self.name


class Course:
    """
    A course offered by an instructor.

    :param course_id: Unique course identifier.
    :type course_id: str
    :param course_name: The course's name.
    :type course_name: str
    :param instructor: The instructor teaching the course.
    :type instructor: Instructor
    """

    def __init__(self, course_id, course_name, instructor):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        """
        Add a student to the course.

        :param student: Student to enroll.
        :type student: Student
        """
        self.enrolled_students.append(student)

    def get_name(self):
        """
        Get the course name.

        :return: The name of the course.
        :rtype: str
        """
        return self.course_name


import json


class DataManager:
    """
    A utility class to manage saving and loading data.
    """

    @staticmethod
    def save_data(filename, data):
        """
        Save data to a JSON file.

        :param filename: Path to the file.
        :type filename: str
        :param data: Data to be saved.
        :type data: dict or list
        """
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_data(filename):
        """
        Load data from a JSON file.

        :param filename: Path to the file.
        :type filename: str
        :return: Loaded data.
        :rtype: dict or list
        """
        with open(filename, "r") as f:
            return json.load(f)


import re


class Validator:
    """
    A validator class to validate age and email inputs.
    """

    @staticmethod
    def validate_age(age):
        """
        Validate that the age is non-negative.

        :param age: Age to validate.
        :type age: int
        :raises ValueError: If age is negative.
        :return: True if valid.
        :rtype: bool
        """
        if age < 0:
            raise ValueError("Age cannot be negative")
        return True

    @staticmethod
    def validate_email(email):
        """
        Validate that the email has a valid format.

        :param email: Email that has to be validated.
        :type email: str
        :raises ValueError: If the email format is invalid.
        :return: True if it's valid.
        :rtype: bool
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return True
