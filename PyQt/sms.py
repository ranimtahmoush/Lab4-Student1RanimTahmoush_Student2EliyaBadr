import tkinter as tk
from tkinter import ttk, messagebox

# Global storage
students = []
instructors = []
courses = []

# ---------------- GUI FUNCTIONS ----------------

# Add Student
def add_student():
    try:
        name = student_name_entry.get()
        age = int(student_age_entry.get())
        email = student_email_entry.get()
        student_id = student_id_entry.get()

        student = Student(name, age, email, student_id)
        students.append(student)

        messagebox.showinfo("Success", f"Student {name} added!")
        refresh_dropdowns()
        refresh_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Add Instructor
def add_instructor():
    try:
        name = instr_name_entry.get()
        age = int(instr_age_entry.get())
        email = instr_email_entry.get()
        instructor_id = instr_id_entry.get()

        instructor = Instructor(name, age, email, instructor_id)
        instructors.append(instructor)

        messagebox.showinfo("Success", f"Instructor {name} added!")
        refresh_dropdowns()
        refresh_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Add Course
def add_course():
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()
    course = Course(course_id, course_name, None)
    courses.append(course)
    messagebox.showinfo("Success", f"Course {course_name} added!")
    refresh_dropdowns()
    refresh_table()

# Register Student to Course
def register_student_to_course():
    student_name = student_select.get()
    course_name = course_select.get()
    student = next((s for s in students if s.name == student_name), None)
    course = next((c for c in courses if c.course_name == course_name), None)
    if student and course:
        student.register_course(course)
        course.add_student(student)
        messagebox.showinfo("Success", f"{student.name} registered in {course.course_name}")
        refresh_table()

# Assign Instructor to Course
def assign_instructor_to_course():
    instr_name = instr_select.get()
    course_name = course_assign_select.get()
    instructor = next((i for i in instructors if i.name == instr_name), None)
    course = next((c for c in courses if c.course_name == course_name), None)
    if instructor and course:
        instructor.assign_course(course)
        course.instructor = instructor
        messagebox.showinfo("Success", f"{instructor.name} assigned to {course.course_name}")
        refresh_table()

# Refresh dropdowns
def refresh_dropdowns():
    student_select["values"] = [s.name for s in students]
    course_select["values"] = [c.course_name for c in courses]
    instr_select["values"] = [i.name for i in instructors]
    course_assign_select["values"] = [c.course_name for c in courses]

# Refresh table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for s in students:
        tree.insert("", "end", values=("Student", s.name, s.student_id))
    for i in instructors:
        tree.insert("", "end", values=("Instructor", i.name, i.instructor_id))
    for c in courses:
        instr_name = c.instructor.name if c.instructor else "None"
        tree.insert("", "end", values=("Course", c.course_name, instr_name))

# Search records
def search_records():
    query = search_entry.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for s in students:
        if query in s.name.lower() or query in s.student_id.lower():
            tree.insert("", "end", values=("Student", s.name, s.student_id))
    for i in instructors:
        if query in i.name.lower() or query in i.instructor_id.lower():
            tree.insert("", "end", values=("Instructor", i.name, i.instructor_id))
    for c in courses:
        if query in c.course_name.lower() or query in c.course_id.lower():
            instr_name = c.instructor.name if c.instructor else "None"
            tree.insert("", "end", values=("Course", c.course_name, instr_name))

# ---------------- GUI LAYOUT ----------------
root = tk.Tk()
root.title("School Management System")
root.geometry("900x700")

# Student form
student_frame = tk.LabelFrame(root, text="Add Student")
student_frame.pack(fill="x", padx=10, pady=5)
tk.Label(student_frame, text="Name").grid(row=0, column=0)
student_name_entry = tk.Entry(student_frame); student_name_entry.grid(row=0, column=1)
tk.Label(student_frame, text="Age").grid(row=1, column=0)
student_age_entry = tk.Entry(student_frame); student_age_entry.grid(row=1, column=1)
tk.Label(student_frame, text="Email").grid(row=2, column=0)
student_email_entry = tk.Entry(student_frame); student_email_entry.grid(row=2, column=1)
tk.Label(student_frame, text="ID").grid(row=3, column=0)
student_id_entry = tk.Entry(student_frame); student_id_entry.grid(row=3, column=1)
tk.Button(student_frame, text="Add Student", command=add_student).grid(row=4, columnspan=2, pady=5)

# Instructor form
instr_frame = tk.LabelFrame(root, text="Add Instructor")
instr_frame.pack(fill="x", padx=10, pady=5)
tk.Label(instr_frame, text="Name").grid(row=0, column=0)
instr_name_entry = tk.Entry(instr_frame); instr_name_entry.grid(row=0, column=1)
tk.Label(instr_frame, text="Age").grid(row=1, column=0)
instr_age_entry = tk.Entry(instr_frame); instr_age_entry.grid(row=1, column=1)
tk.Label(instr_frame, text="Email").grid(row=2, column=0)
instr_email_entry = tk.Entry(instr_frame); instr_email_entry.grid(row=2, column=1)
tk.Label(instr_frame, text="ID").grid(row=3, column=0)
instr_id_entry = tk.Entry(instr_frame); instr_id_entry.grid(row=3, column=1)
tk.Button(instr_frame, text="Add Instructor", command=add_instructor).grid(row=4, columnspan=2, pady=5)

# Course form
course_frame = tk.LabelFrame(root, text="Add Course")
course_frame.pack(fill="x", padx=10, pady=5)
tk.Label(course_frame, text="Course ID").grid(row=0, column=0)
course_id_entry = tk.Entry(course_frame); course_id_entry.grid(row=0, column=1)
tk.Label(course_frame, text="Course Name").grid(row=1, column=0)
course_name_entry = tk.Entry(course_frame); course_name_entry.grid(row=1, column=1)
tk.Button(course_frame, text="Add Course", command=add_course).grid(row=2, columnspan=2, pady=5)

# Student Registration
reg_frame = tk.LabelFrame(root, text="Register Student to Course")
reg_frame.pack(fill="x", padx=10, pady=5)
student_select = ttk.Combobox(reg_frame); student_select.grid(row=0, column=0, padx=5)
course_select = ttk.Combobox(reg_frame); course_select.grid(row=0, column=1, padx=5)
tk.Button(reg_frame, text="Register", command=register_student_to_course).grid(row=0, column=2, padx=5)

# Instructor Assignment
assign_frame = tk.LabelFrame(root, text="Assign Instructor to Course")
assign_frame.pack(fill="x", padx=10, pady=5)
instr_select = ttk.Combobox(assign_frame); instr_select.grid(row=0, column=0, padx=5)
course_assign_select = ttk.Combobox(assign_frame); course_assign_select.grid(row=0, column=1, padx=5)
tk.Button(assign_frame, text="Assign", command=assign_instructor_to_course).grid(row=0, column=2, padx=5)

# Records Display
display_frame = tk.LabelFrame(root, text="All Records")
display_frame.pack(fill="both", expand=True, padx=10, pady=5)
tree = ttk.Treeview(display_frame, columns=("Type", "Name", "ID/Instructor"), show="headings")
tree.heading("Type", text="Type")
tree.heading("Name", text="Name")
tree.heading("ID/Instructor", text="ID / Instructor")
tree.pack(fill="both", expand=True)

# Search
search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=10, pady=5)
search_entry = tk.Entry(search_frame); search_entry.pack(side="left", fill="x", expand=True, padx=5)
tk.Button(search_frame, text="Search", command=search_records).pack(side="left")

root.mainloop()
