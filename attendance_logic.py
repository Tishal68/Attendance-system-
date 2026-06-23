from datetime import date
from db_connection import get_connection, close_connection
def add_student(roll_no, name, branch, year):
    """
    Inserts a new student record into the 'students' table.
    Returns (True, message) on success or (False, message) on failure.
    """
    connection = get_connection()
    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO students (roll_no, name, branch, year)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (roll_no, name, branch, year))
        connection.commit()
        return True, "Student added successfully!"
    except Exception as e:
        return False, f"Could not add student: {e}"
    finally:
        close_connection(connection, cursor)
def get_all_students():
    """
    Returns a list of all students as a list of tuples:
    (student_id, roll_no, name, branch, year)
    """
    connection = get_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT student_id, roll_no, name, branch, year FROM students ORDER BY name")
        rows = cursor.fetchall()
        return rows
    finally:
        close_connection(connection, cursor)
def find_student(search_text):
    """
    Searches for students whose roll number OR name matches the given text.
    Used by the 'Search' feature in the GUI.
    """
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        query = """
            SELECT student_id, roll_no, name, branch, year
            FROM students
            WHERE roll_no LIKE %s OR name LIKE %s
        """
        like_text = f"%{search_text}%"
        cursor.execute(query, (like_text, like_text))
        return cursor.fetchall()
    finally:
        close_connection(connection, cursor)
def mark_attendance(student_id, status, attendance_date=None):
    """
    Marks attendance for a student on a given date.
    status should be either 'Present' or 'Absent'.
    If attendance_date is not given, today's date is used.

    If attendance for that student on that date already exists, we UPDATE
    it instead of creating a duplicate row (a student can only have ONE
    attendance status per day).
    """
    if attendance_date is None:
        attendance_date = date.today()

    connection = get_connection()
    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT attendance_id FROM attendance WHERE student_id = %s AND attendance_date = %s",
            (student_id, attendance_date)
        )
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                "UPDATE attendance SET status = %s WHERE attendance_id = %s",
                (status, existing[0])
            )
            message = "Attendance updated successfully!"
        else:
            cursor.execute(
                "INSERT INTO attendance (student_id, attendance_date, status) VALUES (%s, %s, %s)",
                (student_id, attendance_date, status)
            )
            message = "Attendance marked successfully!"

        connection.commit()
        return True, message
    except Exception as e:
        return False, f"Could not mark attendance: {e}"
    finally:
        close_connection(connection, cursor)
def get_all_attendance():
    """
    Returns every attendance record, joined with student details, so the
    GUI can display a readable table:
    (name, roll_no, attendance_date, status)
    """
    connection = get_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    try:
        query = """
            SELECT s.name, s.roll_no, a.attendance_date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            ORDER BY a.attendance_date DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        close_connection(connection, cursor)


def get_attendance_for_student(search_text):
    """
    Returns attendance history for a specific student, searched by
    roll number or name. Used by the Search tab in the GUI.
    """
    connection = get_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    try:
        query = """
            SELECT s.name, s.roll_no, a.attendance_date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            WHERE s.roll_no LIKE %s OR s.name LIKE %s
            ORDER BY a.attendance_date DESC
        """
        like_text = f"%{search_text}%"
        cursor.execute(query, (like_text, like_text))
        return cursor.fetchall()
    finally:
        close_connection(connection, cursor)
def calculate_attendance_percentage(student_id):
    """
    Calculates and returns the attendance percentage of a single student.
    Formula: (No. of days Present / Total days marked) * 100
    Returns 0 if no attendance has been marked yet (avoids division by zero).
    """
    connection = get_connection()
    if connection is None:
        return 0.0

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id = %s",
            (student_id,)
        )
        total_days = cursor.fetchone()[0]

        if total_days == 0:
            return 0.0

        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id = %s AND status = 'Present'",
            (student_id,)
        )
        present_days = cursor.fetchone()[0]

        percentage = (present_days / total_days) * 100
        return round(percentage, 2)
    finally:
        close_connection(connection, cursor)
def generate_report():
    """
    Generates a simple attendance report for ALL students:
    (roll_no, name, total_days, present_days, absent_days, percentage)

    This is used by the 'Generate Report' button in the GUI and can also
    be saved to a text file.
    """
    students = get_all_students()
    report_rows = []

    for student_id, roll_no, name, branch, year in students:
        connection = get_connection()
        if connection is None:
            continue
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM attendance WHERE student_id = %s", (student_id,)
            )
            total_days = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM attendance WHERE student_id = %s AND status = 'Present'",
                (student_id,)
            )
            present_days = cursor.fetchone()[0]
            absent_days = total_days - present_days

            percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0.0

            report_rows.append((roll_no, name, total_days, present_days, absent_days, percentage))
        finally:
            close_connection(connection, cursor)

    return report_rows
def save_report_to_file(report_rows, filename="attendance_report.txt"):
    """
    Saves the generated report (list of tuples) into a readable text file.
    This is a simple, beginner-friendly way to 'export' a report without
    needing extra libraries.
    """
    with open(filename, "w") as f:
        f.write("ATTENDANCE REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'Roll No':<12}{'Name':<20}{'Total':<8}{'Present':<10}{'Absent':<8}{'%':<6}\n")
        f.write("-" * 60 + "\n")
        for roll_no, name, total, present, absent, pct in report_rows:
            f.write(f"{roll_no:<12}{name:<20}{total:<8}{present:<10}{absent:<8}{pct:<6}\n")
    return filename
