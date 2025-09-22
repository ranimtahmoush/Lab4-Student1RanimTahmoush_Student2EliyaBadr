import tkinter as tk
from tkinter import ttk, messagebox
from main import Student, Instructor, Course
import json


students = []
instructors = []
courses = []



def add_student():
    """Add a new student to the system."""
    try:
        student = Student(
            student_name_entry.get(),
            int(student_age_entry.get()),
            student_email_entry.get(),
            student_id_entry.get()
        )
        students.append(student)
        messagebox.showinfo("Success", f"Student {student.name} added!")
        update_dropdowns()
        refresh_records()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def add_instructor():
    """Add a new instructor to the system."""
    try:
        instructor = Instructor(
            instructor_name_entry.get(),
            int(instructor_age_entry.get()),
            instructor_email_entry.get(),
            instructor_id_entry.get()
        )
        instructors.append(instructor)
        messagebox.showinfo("Success", f"Instructor {instructor.name} added!")
        update_dropdowns()
        refresh_records()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def add_course():
    """Add a new course to the system."""
    try:
        course = Course(
            course_id_entry.get(),
            course_name_entry.get(),
            course_instructor_entry.get()
        )
        courses.append(course)
        messagebox.showinfo("Success", f"Course {course.course_name} added!")
        update_dropdowns()
        refresh_records()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def register_student_to_course():
    """Register a student to a course."""
    student_name = student_dropdown.get()
    course_name = course_dropdown.get()

    if not student_name or not course_name:
        return messagebox.showerror("Error", "Select both a student and a course")

    student_obj = next((s for s in students if s.name == student_name), None)
    course_obj = next((c for c in courses if c.course_name == course_name), None)

    if student_obj and course_obj:
        student_obj.register_course(course_obj)
        course_obj.add_student(student_obj)
        messagebox.showinfo("Success", f"{student_obj.name} registered in {course_obj.course_name}")
    else:
        messagebox.showerror("Error", "Student or course not found")


def assign_instructor_to_course():
    """Assign an instructor to a course."""
    instructor_name = instructor_dropdown.get()
    course_name = course_assign_dropdown.get()

    if not instructor_name or not course_name:
        return messagebox.showerror("Error", "Select both an instructor and a course")

    instructor_obj = next((i for i in instructors if i.name == instructor_name), None)
    course_obj = next((c for c in courses if c.course_name == course_name), None)

    if instructor_obj and course_obj:
        instructor_obj.assign_course(course_obj)
        course_obj.instructor = instructor_obj
        messagebox.showinfo("Success", f"Instructor {instructor_obj.name} assigned to {course_obj.course_name}")
        refresh_records()
    else:
        messagebox.showerror("Error", "Instructor or course not found")


def update_dropdowns():
    """Refresh dropdowns with current data."""
    student_dropdown["values"] = [s.name for s in students]
    course_dropdown["values"] = [c.course_name for c in courses]
    instructor_dropdown["values"] = [i.name for i in instructors]
    course_assign_dropdown["values"] = [c.course_name for c in courses]



def save_all_data():
    """Save all records into JSON file."""
    data = {
        "students": [
            {"id": s.student_id, "name": s.name, "age": s.age, "email": s.get_email()}
            for s in students
        ],
        "instructors": [
            {"id": i.instructor_id, "name": i.name, "age": i.age, "email": i.get_email()}
            for i in instructors
        ],
        "courses": [
            {"id": c.course_id, "name": c.course_name,
             "instructor": getattr(c.instructor, "name", str(c.instructor))}
            for c in courses
        ]
    }
    with open("school_data.json", "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Success", "Data saved to school_data.json")


def load_all_data():
    """Load records from JSON file."""
    try:
        with open("school_data.json", "r") as f:
            data = json.load(f)

        students.clear()
        instructors.clear()
        courses.clear()

        for s in data["students"]:
            students.append(Student(s["name"], int(s["age"]), s["email"], s["id"]))
        for i in data["instructors"]:
            instructors.append(Instructor(i["name"], int(i["age"]), i["email"], i["id"]))
        for c in data["courses"]:
            courses.append(Course(c["id"], c["name"], c["instructor"]))

        refresh_records()
        update_dropdowns()
        messagebox.showinfo("Success", "Data loaded successfully")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved data file found")



def refresh_records():
    """Refresh all tables with updated data."""
    for tree in (student_tree, instructor_tree, course_tree):
        for row in tree.get_children():
            tree.delete(row)

    for s in students:
        student_tree.insert("", "end", values=(s.student_id, s.name, s.age, s.get_email()))
    for i in instructors:
        instructor_tree.insert("", "end", values=(i.instructor_id, i.name, i.age, i.get_email()))
    for c in courses:
        instructor_name = getattr(c.instructor, "name", c.instructor)
        course_tree.insert("", "end", values=(c.course_id, c.course_name, instructor_name))


def search_records():
    """Search for records by name, ID, or email."""
    query = search_entry.get().lower()

    for tree in (student_tree, instructor_tree, course_tree):
        for row in tree.get_children():
            tree.delete(row)

    for s in students:
        if query in str(s.student_id).lower() or query in s.name.lower() or query in s.get_email().lower():
            student_tree.insert("", "end", values=(s.student_id, s.name, s.age, s.get_email()))

    for i in instructors:
        if query in str(i.instructor_id).lower() or query in i.name.lower() or query in i.get_email().lower():
            instructor_tree.insert("", "end", values=(i.instructor_id, i.name, i.age, i.get_email()))

    for c in courses:
        instructor_name = getattr(c.instructor, "name", c.instructor)
        if query in str(c.course_id).lower() or query in c.course_name.lower() or query in str(instructor_name).lower():
            course_tree.insert("", "end", values=(c.course_id, c.course_name, instructor_name))


def delete_record(tree, data_list, id_attr):
    """Delete selected record."""
    selected = tree.selection()
    if not selected:
        return messagebox.showerror("Error", "No record selected")

    item = tree.item(selected[0])
    record_id = item["values"][0]

    obj = next((o for o in data_list if str(getattr(o, id_attr)) == str(record_id)), None)
    if obj:
        data_list.remove(obj)

    tree.delete(selected[0])
    messagebox.showinfo("Success", f"Record {record_id} deleted")


def edit_record(tree, data_list, id_attr):
    """Edit selected record through popup."""
    selected = tree.selection()
    if not selected:
        return messagebox.showerror("Error", "No record selected")

    item = tree.item(selected[0])
    record_id = item["values"][0]

    obj = next((o for o in data_list if str(getattr(o, id_attr)) == str(record_id)), None)
    if not obj:
        return messagebox.showerror("Error", "Record not found")

    
    edit_win = tk.Toplevel(root)
    edit_win.title("Edit Record")
    edit_win.geometry("300x200")

    entries = {}
    row = 0
    for attr, value in obj.__dict__.items():
        if attr.startswith("_"):
            continue
        tk.Label(edit_win, text=attr).grid(row=row, column=0, padx=5, pady=5)
        e = tk.Entry(edit_win)
        e.insert(0, value)
        e.grid(row=row, column=1, padx=5, pady=5)
        entries[attr] = e
        row += 1

    def save_changes():
        for attr, entry in entries.items():
            setattr(obj, attr, entry.get())
        refresh_records()
        edit_win.destroy()
        messagebox.showinfo("Success", "Record updated")

    tk.Button(edit_win, text="Save", command=save_changes).grid(row=row, column=0, columnspan=2, pady=10)



root = tk.Tk()
root.title("School Management System")
root.geometry("750x550")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")


student_frame = ttk.Frame(notebook)
notebook.add(student_frame, text="Students")

ttk.Label(student_frame, text="Add Student", font=("Arial", 14, "bold")).pack(pady=10)
student_name_entry = ttk.Entry(student_frame)
student_age_entry = ttk.Entry(student_frame)
student_email_entry = ttk.Entry(student_frame)
student_id_entry = ttk.Entry(student_frame)
for label, entry in [("Name", student_name_entry), ("Age", student_age_entry),
                     ("Email", student_email_entry), ("Student ID", student_id_entry)]:
    ttk.Label(student_frame, text=label).pack()
    entry.pack()
ttk.Button(student_frame, text="Add Student", command=add_student).pack(pady=10)


instructor_frame = ttk.Frame(notebook)
notebook.add(instructor_frame, text="Instructors")

ttk.Label(instructor_frame, text="Add Instructor", font=("Arial", 14, "bold")).pack(pady=10)
instructor_name_entry = ttk.Entry(instructor_frame)
instructor_age_entry = ttk.Entry(instructor_frame)
instructor_email_entry = ttk.Entry(instructor_frame)
instructor_id_entry = ttk.Entry(instructor_frame)
for label, entry in [("Name", instructor_name_entry), ("Age", instructor_age_entry),
                     ("Email", instructor_email_entry), ("Instructor ID", instructor_id_entry)]:
    ttk.Label(instructor_frame, text=label).pack()
    entry.pack()
ttk.Button(instructor_frame, text="Add Instructor", command=add_instructor).pack(pady=10)


course_frame = ttk.Frame(notebook)
notebook.add(course_frame, text="Courses")

ttk.Label(course_frame, text="Add Course", font=("Arial", 14, "bold")).pack(pady=10)
course_id_entry = ttk.Entry(course_frame)
course_name_entry = ttk.Entry(course_frame)
course_instructor_entry = ttk.Entry(course_frame)
for label, entry in [("Course ID", course_id_entry), ("Course Name", course_name_entry),
                     ("Instructor", course_instructor_entry)]:
    ttk.Label(course_frame, text=label).pack()
    entry.pack()
ttk.Button(course_frame, text="Add Course", command=add_course).pack(pady=10)

registration_frame = ttk.Frame(notebook)
notebook.add(registration_frame, text="Registration")

ttk.Label(registration_frame, text="Register Student for Course", font=("Arial", 14, "bold")).pack(pady=10)
student_dropdown = ttk.Combobox(registration_frame, state="readonly")
course_dropdown = ttk.Combobox(registration_frame, state="readonly")
ttk.Label(registration_frame, text="Select Student").pack()
student_dropdown.pack()
ttk.Label(registration_frame, text="Select Course").pack()
course_dropdown.pack()
ttk.Button(registration_frame, text="Register", command=register_student_to_course).pack(pady=10)


assignment_frame = ttk.Frame(notebook)
notebook.add(assignment_frame, text="Assignments")

ttk.Label(assignment_frame, text="Assign Instructor to Course", font=("Arial", 14, "bold")).pack(pady=10)
instructor_dropdown = ttk.Combobox(assignment_frame, state="readonly")
course_assign_dropdown = ttk.Combobox(assignment_frame, state="readonly")
ttk.Label(assignment_frame, text="Select Instructor").pack()
instructor_dropdown.pack()
ttk.Label(assignment_frame, text="Select Course").pack()
course_assign_dropdown.pack()
ttk.Button(assignment_frame, text="Assign", command=assign_instructor_to_course).pack(pady=10)


records_frame = ttk.Frame(notebook)
notebook.add(records_frame, text="Records")


search_frame = ttk.Frame(records_frame)
search_frame.pack(pady=5)
ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
search_entry = ttk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)
ttk.Button(search_frame, text="Search", command=search_records).pack(side="left", padx=5)
ttk.Button(search_frame, text="Reset", command=refresh_records).pack(side="left", padx=5)


student_tree = ttk.Treeview(records_frame, columns=("ID", "Name", "Age", "Email"), show="headings")
for col, width in zip(("ID", "Name", "Age", "Email"), (100, 150, 50, 200)):
    student_tree.heading(col, text=col)
    student_tree.column(col, width=width)
student_tree.pack(fill="x", padx=10, pady=5)

instructor_tree = ttk.Treeview(records_frame, columns=("ID", "Name", "Age", "Email"), show="headings")
for col, width in zip(("ID", "Name", "Age", "Email"), (120, 150, 50, 200)):
    instructor_tree.heading(col, text=col)
    instructor_tree.column(col, width=width)
instructor_tree.pack(fill="x", padx=10, pady=5)

course_tree = ttk.Treeview(records_frame, columns=("ID", "Name", "Instructor"), show="headings")
for col, width in zip(("ID", "Name", "Instructor"), (100, 150, 200)):
    course_tree.heading(col, text=col)
    course_tree.column(col, width=width)
course_tree.pack(fill="x", padx=10, pady=5)


ttk.Button(records_frame, text="Edit Student", command=lambda: edit_record(student_tree, students, "student_id")).pack(pady=2)
ttk.Button(records_frame, text="Delete Student", command=lambda: delete_record(student_tree, students, "student_id")).pack(pady=2)
ttk.Button(records_frame, text="Edit Instructor", command=lambda: edit_record(instructor_tree, instructors, "instructor_id")).pack(pady=2)
ttk.Button(records_frame, text="Delete Instructor", command=lambda: delete_record(instructor_tree, instructors, "instructor_id")).pack(pady=2)
ttk.Button(records_frame, text="Edit Course", command=lambda: edit_record(course_tree, courses, "course_id")).pack(pady=2)
ttk.Button(records_frame, text="Delete Course", command=lambda: delete_record(course_tree, courses, "course_id")).pack(pady=2)
ttk.Button(records_frame, text="Save Data", command=save_all_data).pack(pady=5)
ttk.Button(records_frame, text="Load Data", command=load_all_data).pack(pady=5)


root.mainloop()
