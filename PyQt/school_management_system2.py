import sys, re, csv, sqlite3, shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFormLayout, QTabWidget,
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem,
    QHBoxLayout
)


DB_FILE = "school.db"

def init_db():
    """
    Create database tables for Students, Instructors, Courses, and Registrations.
    Ensures schema exists before app runs.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )
    """)

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS instructors (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )
    """)

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        instructor_id TEXT,
        FOREIGN KEY (instructor_id) REFERENCES instructors(id)
    )
    """)

   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        student_id TEXT,
        course_id TEXT,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
    """)

    conn.commit()
    conn.close()


def execute_query(query, params=(), fetch=False):
    """
    Run SQL queries in a safe manner  against the database.
    - query: SQL command
    - params: tuple of values for placeholders
    - fetch: if True, return results
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data



class SchoolManagementSystem(QMainWindow):
    """
    School Management System GUI
    Features:
      - Manage the classes: Students, Instructors, and Courses
      - Register the students to courses
      - Assign the instructors to courses
      - Display and manage records such as (delete, export, backup)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(200, 200, 950, 650)


        init_db()


        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)


        self.add_student_tab()
        self.add_instructor_tab()
        self.add_course_tab()
        self.add_registration_tab()
        self.add_assignment_tab()
        self.add_records_tab()

    
        self.refresh_records()
        self.update_dropdowns()

        self.show()

  
    def validate_input(self, name=None, age=None, email=None, id_value=None):
        """Validate user inputs for name, age, email, and IDs."""
        if name is not None:
            if not name.strip() or not name.replace(" ", "").isalpha():
                QMessageBox.warning(self, "Invalid Input", "Name must contain only letters.")
                return False

        if age is not None:
            if not age.isdigit() or int(age) <= 0:
                QMessageBox.warning(self, "Invalid Input", "Age must be a positive number.")
                return False

        if email is not None:
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, email):
                QMessageBox.warning(self, "Invalid Input", "Invalid email format.")
                return False

        if id_value is not None:
            if not id_value.strip() or not id_value.isalnum():
                QMessageBox.warning(self, "Invalid Input", "ID must be alphanumeric.")
                return False

        return True

    
    def add_student_tab(self):
        tab = QWidget()
        layout = QFormLayout()

        
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()

        layout.addRow("Name:", self.student_name)
        layout.addRow("Age:", self.student_age)
        layout.addRow("Email:", self.student_email)
        layout.addRow("Student ID:", self.student_id)

        
        btn = QPushButton("Add Student")
        btn.clicked.connect(self.add_student)
        layout.addRow(btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Students")

    def add_student(self):
        """Insert a new student record into database."""
        name, sid, age, email = (
            self.student_name.text(),
            self.student_id.text(),
            self.student_age.text(),
            self.student_email.text(),
        )
        if not self.validate_input(name=name, age=age, email=email, id_value=sid):
            return
        try:
            execute_query("INSERT INTO students VALUES (?, ?, ?, ?)", (sid, name, age, email))
            QMessageBox.information(self, "Success", f"Student {name} added!")
            self.refresh_records()
            self.update_dropdowns()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Student ID already exists.")

    
    def add_instructor_tab(self):
        tab = QWidget()
        layout = QFormLayout()

        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()

        layout.addRow("Name:", self.instructor_name)
        layout.addRow("Age:", self.instructor_age)
        layout.addRow("Email:", self.instructor_email)
        layout.addRow("Instructor ID:", self.instructor_id)

        btn = QPushButton("Add Instructor")
        btn.clicked.connect(self.add_instructor)
        layout.addRow(btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Instructors")

    def add_instructor(self):
        """Add  a new instructor record into the  database."""
        name, iid, age, email = (
            self.instructor_name.text(),
            self.instructor_id.text(),
            self.instructor_age.text(),
            self.instructor_email.text(),
        )
        if not self.validate_input(name=name, age=age, email=email, id_value=iid):
            return
        try:
            execute_query("INSERT INTO instructors VALUES (?, ?, ?, ?)", (iid, name, age, email))
            QMessageBox.information(self, "Success", f"Instructor {name} added!")
            self.refresh_records()
            self.update_dropdowns()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Instructor ID already exists.")

    
    def add_course_tab(self):
        tab = QWidget()
        layout = QFormLayout()

        self.course_id = QLineEdit()
        self.course_name = QLineEdit()
        self.course_instructor = QComboBox()

        layout.addRow("Course ID:", self.course_id)
        layout.addRow("Course Name:", self.course_name)
        layout.addRow("Instructor:", self.course_instructor)

        btn = QPushButton("Add Course")
        btn.clicked.connect(self.add_course)
        layout.addRow(btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Courses")

    def add_course(self):
        """Insert a new course record into database."""
        cid, cname, inst = self.course_id.text(), self.course_name.text(), self.course_instructor.currentText()
        if not self.validate_input(name=cname, id_value=cid):
            return
        inst_id = inst.split(" - ")[0] if inst else None
        try:
            execute_query("INSERT INTO courses VALUES (?, ?, ?)", (cid, cname, inst_id))
            QMessageBox.information(self, "Success", f"Course {cname} added!")
            self.refresh_records()
            self.update_dropdowns()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Course ID already exists.")

   
    def add_registration_tab(self):
        tab = QWidget()
        layout = QFormLayout()

        self.student_dropdown = QComboBox()
        self.course_dropdown = QComboBox()

        layout.addRow("Select Student:", self.student_dropdown)
        layout.addRow("Select Course:", self.course_dropdown)

        btn = QPushButton("Register Student to Course")
        btn.clicked.connect(self.register_student)
        layout.addRow(btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Registration")

    def register_student(self):
        """Register a student for a course."""
        if not self.student_dropdown.currentText() or not self.course_dropdown.currentText():
            return
        student = self.student_dropdown.currentText().split(" - ")[0]
        course = self.course_dropdown.currentText().split(" - ")[0]
        try:
            execute_query("INSERT INTO registrations VALUES (?, ?)", (student, course))
            QMessageBox.information(self, "Success", "Student registered to course.")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Student already registered for this course.")

 
    def add_assignment_tab(self):
        tab = QWidget()
        layout = QFormLayout()

        self.instructor_dropdown = QComboBox()
        self.course_assign_dropdown = QComboBox()

        layout.addRow("Select Instructor:", self.instructor_dropdown)
        layout.addRow("Select Course:", self.course_assign_dropdown)

        btn = QPushButton("Assign Instructor")
        btn.clicked.connect(self.assign_instructor)
        layout.addRow(btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Assignments")

    def assign_instructor(self):
        """Assign an instructor to a course."""
        if not self.instructor_dropdown.currentText() or not self.course_assign_dropdown.currentText():
            return
        instructor = self.instructor_dropdown.currentText().split(" - ")[0]
        course = self.course_assign_dropdown.currentText().split(" - ")[0]
        execute_query("UPDATE courses SET instructor_id=? WHERE id=?", (instructor, course))
        QMessageBox.information(self, "Success", "Instructor assigned to course.")
        self.refresh_records()
        self.update_dropdowns()

   
    def add_records_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(4)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email"])
        layout.addWidget(QLabel("Students"))
        layout.addWidget(self.student_table)

        
        self.instructor_table = QTableWidget()
        self.instructor_table.setColumnCount(4)
        self.instructor_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email"])
        layout.addWidget(QLabel("Instructors"))
        layout.addWidget(self.instructor_table)

    
        self.course_table = QTableWidget()
        self.course_table.setColumnCount(3)
        self.course_table.setHorizontalHeaderLabels(["ID", "Course Name", "Instructor ID"])
        layout.addWidget(QLabel("Courses"))
        layout.addWidget(self.course_table)

       
        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete Selected")
        export_btn = QPushButton("Export to CSV")
        backup_btn = QPushButton("Backup DB")

        delete_btn.clicked.connect(self.delete_record)
        export_btn.clicked.connect(self.export_csv)
        backup_btn.clicked.connect(self.backup_db)

        for b in (delete_btn, export_btn, backup_btn):
            btn_layout.addWidget(b)
        layout.addLayout(btn_layout)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Records")

    def refresh_records(self):
        """Reload all tables from the database."""
       
        rows = execute_query("SELECT * FROM students", fetch=True)
        self.student_table.setRowCount(len(rows))
        for r, s in enumerate(rows):
            for c, val in enumerate(s):
                self.student_table.setItem(r, c, QTableWidgetItem(str(val)))

        rows = execute_query("SELECT * FROM instructors", fetch=True)
        self.instructor_table.setRowCount(len(rows))
        for r, s in enumerate(rows):
            for c, val in enumerate(s):
                self.instructor_table.setItem(r, c, QTableWidgetItem(str(val)))

       
        rows = execute_query("SELECT * FROM courses", fetch=True)
        self.course_table.setRowCount(len(rows))
        for r, s in enumerate(rows):
            for c, val in enumerate(s):
                self.course_table.setItem(r, c, QTableWidgetItem(str(val)))

    def delete_record(self):
        """Delete the selected record from the table that has focus."""
        if self.student_table.hasFocus():
            row = self.student_table.currentRow()
            sid = self.student_table.item(row, 0).text()
            execute_query("DELETE FROM students WHERE id=?", (sid,))
        elif self.instructor_table.hasFocus():
            row = self.instructor_table.currentRow()
            iid = self.instructor_table.item(row, 0).text()
            execute_query("DELETE FROM instructors WHERE id=?", (iid,))
        elif self.course_table.hasFocus():
            row = self.course_table.currentRow()
            cid = self.course_table.item(row, 0).text()
            execute_query("DELETE FROM courses WHERE id=?", (cid,))
        self.refresh_records()
        self.update_dropdowns()

    def export_csv(self):
        """Export all the records to CSV for external use."""
        with open("school_records.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["--- Students ---"])
            writer.writerow(["ID", "Name", "Age", "Email"])
            for row in execute_query("SELECT * FROM students", fetch=True):
                writer.writerow(row)
            writer.writerow([])

            writer.writerow(["--- Instructors ---"])
            writer.writerow(["ID", "Name", "Age", "Email"])
            for row in execute_query("SELECT * FROM instructors", fetch=True):
                writer.writerow(row)
            writer.writerow([])

            writer.writerow(["--- Courses ---"])
            writer.writerow(["ID", "Name", "Instructor ID"])
            for row in execute_query("SELECT * FROM courses", fetch=True):
                writer.writerow(row)

        QMessageBox.information(self, "Exported", "Data exported to school_records.csv")

    def backup_db(self):
        """Backup the database file to backup_school.db"""
        try:
            shutil.copy(DB_FILE, "backup_school.db")
            QMessageBox.information(self, "Backup Complete", "Database backed up to backup_school.db")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Backup failed: {e}")

   
    def update_dropdowns(self):
        """Refresh dropdowns for Students, Courses, and Instructors."""
        self.student_dropdown.clear()
        self.course_dropdown.clear()
        self.instructor_dropdown.clear()
        self.course_assign_dropdown.clear()
        self.course_instructor.clear()

        for s in execute_query("SELECT id, name FROM students", fetch=True):
            self.student_dropdown.addItem(f"{s[0]} - {s[1]}")

        for c in execute_query("SELECT id, name FROM courses", fetch=True):
            self.course_dropdown.addItem(f"{c[0]} - {c[1]}")
            self.course_assign_dropdown.addItem(f"{c[0]} - {c[1]}")

        for i in execute_query("SELECT id, name FROM instructors", fetch=True):
            self.instructor_dropdown.addItem(f"{i[0]} - {i[1]}")
            self.course_instructor.addItem(f"{i[0]} - {i[1]}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    sys.exit(app.exec_())
