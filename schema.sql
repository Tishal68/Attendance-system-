
CREATE DATABASE IF NOT EXISTS attendance_db;

USE attendance_db;

CREATE TABLE IF NOT EXISTS students (
    student_id  INT AUTO_INCREMENT PRIMARY KEY,   -- unique internal ID
    roll_no     VARCHAR(20)  NOT NULL UNIQUE,      -- college roll number, must be unique
    name        VARCHAR(100) NOT NULL,             -- student's full name
    branch      VARCHAR(50)  DEFAULT 'AI & DS',    -- branch/department
    year        VARCHAR(10)  DEFAULT '2',          -- year of study
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id    INT AUTO_INCREMENT PRIMARY KEY,
    student_id       INT NOT NULL,
    attendance_date  DATE NOT NULL,
    status           ENUM('Present', 'Absent') NOT NULL,
    UNIQUE KEY unique_attendance_per_day (student_id, attendance_date),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE   -- if a student is deleted, their attendance rows go too
);

