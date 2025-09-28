import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from school_management import Student, Instructor, Course

students = []
instructors = []
courses = []

root = tk.Tk()
root.title("School Management System")
root.geometry("1000x600")

tabControl = ttk.Notebook(root)
tab_students = ttk.Frame(tabControl)
tab_instructors = ttk.Frame(tabControl)
tab_courses = ttk.Frame(tabControl)
tabControl.add(tab_students, text='Students')
tabControl.add(tab_instructors, text='Instructors')
tabControl.add(tab_courses, text='Courses')
tabControl.pack(expand=1, fill="both")


def refresh_treeview():
    """
    Refresh all treeviews (students, instructors, courses).

    This clears out the treeviews and repopulates them with the
    latest data from the global ``students``, ``instructors``,
    and ``courses`` lists.
    """
    for tree in [student_tree, instructor_tree, course_tree]:
        for i in tree.get_children():
            tree.delete(i)
    for s in students:
        student_tree.insert(
            '',
            'end',
            values=(s.student_id, s.name, s.age, s._email,
                    ",".join([c.course_id for c in s.registered_courses]))
        )
    for i in instructors:
        instructor_tree.insert(
            '',
            'end',
            values=(i.instructor_id, i.name, i.age, i._email,
                    ",".join([c.course_id for c in i.assigned_courses]))
        )
    for c in courses:
        instructor_name = c.instructor.name if c.instructor else ""
        course_tree.insert(
            '',
            'end',
            values=(c.course_id, c.course_name, instructor_name,
                    ",".join([s.student_id for s in c.enrolled_students]))
        )


def save_data():
    """
    Save all data (students, instructors, courses) to a JSON file.

    Opens a save dialog so the user can choose where to save.
    Each object is serialized via its ``to_dict`` method.

    A popup message is shown if saving succeeds.
    """
    data = {
        "students": [s.to_dict() for s in students],
        "instructors": [i.to_dict() for i in instructors],
        "courses": [c.to_dict() for c in courses]
    }
    file = filedialog.asksaveasfilename(defaultextension=".json")
    if file:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Save", "Data saved successfully!")


def load_data():
    """
    Load data from a JSON file.

    Recreates students, instructors, and courses from saved JSON.
    Also re-links relationships:
      - Which students are enrolled in which courses
      - Which instructor is assigned to which course

    Updates the treeviews when done.
    """
    global students, instructors, courses
    file = filedialog.askopenfilename(defaultextension=".json")
    if file:
        with open(file, "r") as f:
            data = json.load(f)
        students = [Student(s["name"], s["age"], s["email"], s["student_id"])
                    for s in data["students"]]
        instructors = [Instructor(i["name"], i["age"], i["email"], i["instructor_id"])
                       for i in data["instructors"]]
        courses = [Course(c["course_id"], c["course_name"])
                   for c in data["courses"]]

        course_dict = {c.course_id: c for c in courses}
        student_dict = {s.student_id: s for s in students}
        instructor_dict = {i.instructor_id: i for i in instructors}

        for c_data, c_obj in zip(data["courses"], courses):
            if c_data["instructor"]:
                c_obj.instructor = instructor_dict.get(c_data["instructor"])
            for sid in c_data["enrolled_students"]:
                if sid in student_dict:
                    c_obj.enrolled_students.append(student_dict[sid])

        for s in students:
            for cid in s.to_dict()["registered_courses"]:
                if cid in course_dict:
                    s.registered_courses.append(course_dict[cid])

        for i in instructors:
            for cid in i.to_dict()["assigned_courses"]:
                if cid in course_dict:
                    i.assigned_courses.append(course_dict[cid])

        refresh_treeview()
        messagebox.showinfo("Load", "Data loaded successfully!")


# ------------------------
# Student tab
# ------------------------
tk.Label(tab_students, text="ID").grid(row=0, column=0)
tk.Label(tab_students, text="Name").grid(row=1, column=0)
tk.Label(tab_students, text="Age").grid(row=2, column=0)
tk.Label(tab_students, text="Email").grid(row=3, column=0)

s_id = tk.Entry(tab_students)
s_name = tk.Entry(tab_students)
s_age = tk.Entry(tab_students)
s_email = tk.Entry(tab_students)
s_id.grid(row=0, column=1)
s_name.grid(row=1, column=1)
s_age.grid(row=2, column=1)
s_email.grid(row=3, column=1)


def add_student():
    """
    Add a new student based on form inputs.

    Reads the fields (ID, name, age, email), creates a ``Student``,
    adds it to the global list, and updates the treeview.

    Shows an error message if something goes wrong (e.g. invalid age).
    """
    try:
        s = Student(s_name.get(), int(s_age.get()), s_email.get(), s_id.get())
        students.append(s)
        refresh_treeview()
    except Exception as e:
        messagebox.showerror("Error", str(e))


tk.Button(tab_students, text="Add Student", command=add_student).grid(row=4, column=0, columnspan=2)

# ------------------------
# Instructor tab
# ------------------------
tk.Label(tab_instructors, text="ID").grid(row=0, column=0)
tk.Label(tab_instructors, text="Name").grid(row=1, column=0)
tk.Label(tab_instructors, text="Age").grid(row=2, column=0)
tk.Label(tab_instructors, text="Email").grid(row=3, column=0)

i_id = tk.Entry(tab_instructors)
i_name = tk.Entry(tab_instructors)
i_age = tk.Entry(tab_instructors)
i_email = tk.Entry(tab_instructors)
i_id.grid(row=0, column=1)
i_name.grid(row=1, column=1)
i_age.grid(row=2, column=1)
i_email.grid(row=3, column=1)


def add_instructor():
    """
    Add a new instructor based on form inputs.

    Creates an ``Instructor`` and adds it to the global list.
    Updates the instructor treeview.
    """
    try:
        i = Instructor(i_name.get(), int(i_age.get()), i_email.get(), i_id.get())
        instructors.append(i)
        refresh_treeview()
    except Exception as e:
        messagebox.showerror("Error", str(e))


tk.Button(tab_instructors, text="Add Instructor", command=add_instructor).grid(row=4, column=0, columnspan=2)

# ------------------------
# Courses tab
# ------------------------
tk.Label(tab_courses, text="ID").grid(row=0, column=0)
tk.Label(tab_courses, text="Name").grid(row=1, column=0)

c_id = tk.Entry(tab_courses)
c_name = tk.Entry(tab_courses)
c_id.grid(row=0, column=1)
c_name.grid(row=1, column=1)


def add_course():
    """
    Add a new course based on form inputs.

    Creates a ``Course`` and stores it in the global list.
    """
    try:
        c = Course(c_id.get(), c_name.get())
        courses.append(c)
        refresh_treeview()
    except Exception as e:
        messagebox.showerror("Error", str(e))


tk.Button(tab_courses, text="Add Course", command=add_course).grid(row=2, column=0, columnspan=2)

# ------------------------
# Course registration / assignment
# ------------------------
tk.Label(tab_students, text="Register Course:").grid(row=5, column=0)
course_var = tk.StringVar()
course_dropdown = ttk.Combobox(tab_students, textvariable=course_var)
course_dropdown.grid(row=5, column=1)


def update_course_dropdown():
    """
    Update the course dropdown in the student tab.

    Keeps the options current after courses are added/removed.
    """
    course_dropdown['values'] = [c.course_id for c in courses]


def register_course_to_student():
    """
    Register a student to a selected course.

    Uses the ID from the form and the course from the dropdown.
    Calls ``student.register_course`` if valid.
    """
    sid = s_id.get()
    student = next((s for s in students if s.student_id == sid), None)
    course = next((c for c in courses if c.course_id == course_var.get()), None)
    if student and course:
        student.register_course(course)
        refresh_treeview()
    else:
        messagebox.showerror("Error", "Invalid student or course")


tk.Button(tab_students, text="Register", command=register_course_to_student).grid(row=6, column=0, columnspan=2)

tk.Label(tab_instructors, text="Assign Course:").grid(row=5, column=0)
inst_course_var = tk.StringVar()
inst_course_dropdown = ttk.Combobox(tab_instructors, textvariable=inst_course_var)
inst_course_dropdown.grid(row=5, column=1)


def assign_course_to_instructor():
    """
    Assign a course to an instructor.

    Links the instructor and course via ``assign_course``.
    """
    iid = i_id.get()
    instructor = next((i for i in instructors if i.instructor_id == iid), None)
    course = next((c for c in courses if c.course_id == inst_course_var.get()), None)
    if instructor and course:
        instructor.assign_course(course)
        refresh_treeview()
    else:
        messagebox.showerror("Error", "Invalid instructor or course")


tk.Button(tab_instructors, text="Assign", command=assign_course_to_instructor).grid(row=6, column=0, columnspan=2)

# ------------------------
# Treeviews
# ------------------------
student_tree = ttk.Treeview(tab_students, columns=("ID", "Name", "Age", "Email", "Courses"), show="headings")
for col in ("ID", "Name", "Age", "Email", "Courses"):
    student_tree.heading(col, text=col)
student_tree.grid(row=7, column=0, columnspan=2)

instructor_tree = ttk.Treeview(tab_instructors, columns=("ID", "Name", "Age", "Email", "Courses"), show="headings")
for col in ("ID", "Name", "Age", "Email", "Courses"):
    instructor_tree.heading(col, text=col)
instructor_tree.grid(row=7, column=0, columnspan=2)

course_tree = ttk.Treeview(tab_courses, columns=("ID", "Name", "Instructor", "Students"), show="headings")
for col in ("ID", "Name", "Instructor", "Students"):
    course_tree.heading(col, text=col)
course_tree.grid(row=3, column=0, columnspan=2)


def delete_selected_student():
    """
    Delete the currently selected student.

    Removes them from ``students`` and refreshes the tree.
    """
    selected = student_tree.selection()
    if selected:
        sid = student_tree.item(selected[0])['values'][0]
        global students
        students = [s for s in students if s.student_id != sid]
        refresh_treeview()


tk.Button(tab_students, text="Delete Selected", command=delete_selected_student).grid(row=8, column=0, columnspan=2)


def delete_selected_instructor():
    """
    Delete the currently selected instructor.

    Removes them from ``instructors`` and refreshes the tree.
    """
    selected = instructor_tree.selection()
    if selected:
        iid = instructor_tree.item(selected[0])['values'][0]
        global instructors
        instructors = [i for i in instructors if i.instructor_id != iid]
        refresh_treeview()


tk.Button(tab_instructors, text="Delete Selected", command=delete_selected_instructor).grid(row=8, column=0, columnspan=2)


def delete_selected_course():
    """
    Delete the currently selected course.

    Removes it from ``courses`` and refreshes the tree.
    """
    selected = course_tree.selection()
    if selected:
        cid = course_tree.item(selected[0])['values'][0]
        global courses
        courses = [c for c in courses if c.course_id != cid]
        refresh_treeview()


tk.Button(tab_courses, text="Delete Selected", command=delete_selected_course).grid(row=4, column=0, columnspan=2)

# ------------------------
# Save / Load buttons
# ------------------------
tk.Button(root, text="Save Data", command=save_data).pack(side="left")
tk.Button(root, text="Load Data", command=load_data).pack(side="left")


def update_dropdowns_loop():
    """
    Periodically update dropdowns.

    Ensures the course dropdowns for students and instructors
    are always up to date. Runs every second.
    """
    update_course_dropdown()
    inst_course_dropdown['values'] = [c.course_id for c in courses]
    root.after(1000, update_dropdowns_loop)


update_dropdowns_loop()
refresh_treeview()
root.mainloop()
