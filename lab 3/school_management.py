import json
import re


class Person:
    """
    defines a person

    :param name: Name of person
    :type name: str
    :param age: age of person
    :type age: int
    :param email: email of person
    :type email: str

    :raises ValueError: If age is negative or email is invalid
    """

    def __init__(self, name: str, age: int, email: str):
        if age < 0:
            raise ValueError("Age cannot be negative")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """
        prints hello message for person
        """
        print(f"Hi, my name is {self.name}, I am {self.age} years old.")

    def to_dict(self):
        """
        person to dictionary

        :return: Dictionary containing person's attributes
        :rtype: dict
        """
        return {"name": self.name, "age": self.age, "email": self._email}

    @classmethod
    def from_dict(cls, data):
        """
        creates person from dict

        :param data: Dictionary containing person data
        :type data: dict
        :return: Person object
        :rtype: Person
        """
        return cls(data["name"], data["age"], data["email"])


class Student(Person):
    """
    inheritence from person, for student

    :param name: Name of the student
    :type name: str
    :param age: Age of the student
    :type age: int
    :param email: Email of the student
    :type email: str
    :param student_id: Unique student identifier
    :type student_id: str
    """

    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        registers student in course


        :param course: Course object to register
        :type course: Course
        """
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)

    def to_dict(self):
        """
        Converts the Student object to a dictionary representation.

        :return: Dictionary containing student's data
        :rtype: dict
        """
        return {
            "type": "student",
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "student_id": self.student_id,
            "registered_courses": [c.course_id for c in self.registered_courses],
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Student instance from a dictionary.

        :param data: Dictionary containing student data
        :type data: dict
        :return: Student object
        :rtype: Student
        """
        return cls(data["name"], data["age"], data["email"], data["student_id"])


class Instructor(Person):
    """
    Represents an instructor, inheriting from Person.

    :param name: Name of the instructor
    :type name: str
    :param age: Age of the instructor
    :type age: int
    :param email: Email of the instructor
    :type email: str
    :param instructor_id: Unique instructor identifier
    :type instructor_id: str
    """

    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assigns a course to the instructor and sets the instructor of the course.

        :param course: Course object to assign
        :type course: Course
        """
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self

    def to_dict(self):
        """
        Converts the Instructor object to a dictionary representation.

        :return: Dictionary containing instructor's data
        :rtype: dict
        """
        return {
            "type": "instructor",
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "instructor_id": self.instructor_id,
            "assigned_courses": [c.course_id for c in self.assigned_courses],
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates an Instructor instance from a dictionary.

        :param data: Dictionary containing instructor data
        :type data: dict
        :return: Instructor object
        :rtype: Instructor
        """
        return cls(data["name"], data["age"], data["email"], data["instructor_id"])


class Course:
    """
    defines a course

    :param course_id: Unique course identifier
    :type course_id: str
    :param course_name: Name of the course
    :type course_name: str
    """

    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None
        self.enrolled_students = []

    def add_student(self, student):
        """
        Adds a student to the enrolled students list if not already present.

        :param student: Student object to add
        :type student: Student
        """
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)

    def to_dict(self):
        """
        Converts the Course object to a dictionary representation.

        :return: Dictionary containing course data
        :rtype: dict
        """
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor": self.instructor.instructor_id if self.instructor else None,
            "enrolled_students": [s.student_id for s in self.enrolled_students],
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Course instance from a dictionary.

        :param data: Dictionary containing course data
        :type data: dict
        :return: Course object
        :rtype: Course
        """
        return cls(data["course_id"], data["course_name"])


def save_data(filename, students, instructors, courses):
    """
    Saves students, instructors, and courses data into a JSON file.

    :param filename: Path to the output JSON file
    :type filename: str
    :param students: List of Student objects
    :type students: list[Student]
    :param instructors: List of Instructor objects
    :type instructors: list[Instructor]
    :param courses: List of Course objects
    :type courses: list[Course]
    """
    data = {
        "students": [s.to_dict() for s in students],
        "instructors": [i.to_dict() for i in instructors],
        "courses": [c.to_dict() for c in courses],
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_data(filename):
    """
    Loads students, instructors, and courses data from a JSON file.

    :param filename: Path to the input JSON file
    :type filename: str
    :return: Tuple of lists (students, instructors, courses)
    :rtype: tuple[list[Student], list[Instructor], list[Course]]
    """
    with open(filename, "r") as f:
        data = json.load(f)

    students = [Student.from_dict(s) for s in data["students"]]
    instructors = [Instructor.from_dict(i) for i in data["instructors"]]
    courses = [Course.from_dict(c) for c in data["courses"]]

    return students, instructors, courses
