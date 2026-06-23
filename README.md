# 🎓 Attendance Tracking System

A simple, beginner-friendly **Attendance Tracking System** built with **Python**, **Tkinter**, and **MySQL**.
This project was created as a second-year B.Tech (Artificial Intelligence & Data Science) academic project.

It allows a teacher/admin to:
- Add student details
- Mark daily attendance (Present/Absent)
- View all attendance records
- Search attendance by student ID/roll number or name
- Generate attendance reports
- Automatically calculate attendance percentage



| Add Student | Mark Attendance |
|---|---|
| ![Add Student](screenshots/screenshot_add_student.png) | ![Mark Attendance](screenshots/screenshot_mark_attendance.png) |

| View / Search | Reports |
|---|---|
| ![View Search](screenshots/screenshot_view_search.png) | ![Reports](screenshots/screenshot_reports.png) |

> Note: These screenshots are illustrative mockups of the interface layout. When you run `gui.py` on your own computer, the real Tkinter window will look very similar to this.

---

## 🛠️ Tech Stack

| Component        | Technology              |
|-------------------|--------------------------|
| Programming Language | Python 3.x           |
| GUI Library       | Tkinter (built into Python) |
| Database          | MySQL                   |
| DB Connector      | `mysql-connector-python` |

---

## 📁 Project Structure

```
attendance_system/
│
├── gui.py                  # Main GUI file – run this file to start the app
├── attendance_logic.py     # All business logic (add/search/report functions)
├── db_connection.py        # MySQL connection handling
├── schema.sql              # Database schema (run this in MySQL first)
├── requirements.txt        # Python dependencies
├── generate_screenshots.py # (optional) regenerates the mockup screenshots
├── screenshots/            # GUI screenshots used in this README
└── README.md
```

Each file has a single, clear responsibility:
- **gui.py** → only handles what the user *sees* and *clicks*
- **attendance_logic.py** → only handles the *rules* (calculations, validations)
- **db_connection.py** → only handles *talking to MySQL*

This separation makes the project much easier to debug and extend.

---

## ⚙️ Setup Instructions

### 1. Install Python
Make sure Python 3.8+ is installed. Check with:
```bash
python --version
```

### 2. Install MySQL Server
Download and install MySQL Community Server from https://dev.mysql.com/downloads/
Remember the **root password** you set during installation — you'll need it later.

### 3. Create the Database
Open the MySQL command line (or MySQL Workbench) and run:
```bash
mysql -u root -p < schema.sql
```
Or simply open `schema.sql` in MySQL Workbench and click **Execute**.
This creates the `attendance_db` database with two tables: `students` and `attendance`.

### 4. Install Python Dependencies
Navigate to the project folder and run:
```bash
pip install -r requirements.txt
```

### 5. Configure Database Credentials
Open `db_connection.py` and update the `DB_CONFIG` dictionary with your own MySQL username and password:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",   # <-- change this
    "database": "attendance_db"
}
```

### 6. Test the Database Connection (optional but recommended)
```bash
python db_connection.py
```
You should see: `Connection to MySQL database successful!`

### 7. Run the Application
```bash
python gui.py
```
The Attendance Tracking System window should open.

---

## 📋 How to Use

1. **Add Student tab** → Fill in Roll Number, Name, Branch, Year → click **Add Student**.
2. **Mark Attendance tab** → Select a student from the dropdown, pick a date, choose Present/Absent → click **Mark Attendance**.
3. **View / Search tab** → See all attendance records, or type a roll number/name to search.
4. **Reports tab** → Click **Generate Report** to see attendance % for every student. Click **Save Report to File** to export it as a `.txt` file.

---

## 🗄️ Database Schema (Summary)

**students**
| Column | Type | Description |
|---|---|---|
| student_id | INT (PK) | Auto-generated unique ID |
| roll_no | VARCHAR(20) | Unique roll number |
| name | VARCHAR(100) | Student name |
| branch | VARCHAR(50) | Branch (default: AI & DS) |
| year | VARCHAR(10) | Year of study |

**attendance**
| Column | Type | Description |
|---|---|---|
| attendance_id | INT (PK) | Auto-generated unique ID |
| student_id | INT (FK) | Links to students table |
| attendance_date | DATE | Date of attendance |
| status | ENUM('Present','Absent') | Attendance status |

See [`schema.sql`](schema.sql) for the full SQL.

---

## 🚀 Future Enhancements

- Login system for teacher/admin
- Export reports to PDF/Excel
- Monthly/subject-wise attendance
- Charts/graphs for attendance trends
- SMS/email alerts for low attendance



