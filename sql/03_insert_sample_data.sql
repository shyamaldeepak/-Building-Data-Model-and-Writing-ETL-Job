-- ============================================
-- 03_INSERT_SAMPLE_DATA.SQL
-- Step 3: Insert sample data for testing
-- ============================================

-- 1. INSERT STUDENTS
INSERT INTO students (first_name, last_name, email, phone, date_of_birth)
VALUES 
('Alice', 'Johnson', 'alice.johnson@example.com', '1234567890', '2005-05-15'),
('Bob', 'Smith', 'bob.smith@example.com', '0987654321', '2006-08-22'),
('Charlie', 'Brown', 'charlie.brown@example.com', '5555555555', '2005-12-10'),
('Diana', 'Davis', 'diana.davis@example.com', '4444444444', '2006-03-18'),
('Eve', 'Wilson', 'eve.wilson@example.com', '3333333333', '2005-07-25');

-- 2. INSERT COURSES
INSERT INTO courses (course_name, course_code, credits, instructor)
VALUES 
('Data Engineering 101', 'DE101', 3, 'Dr. Smith'),
('Python Basics', 'PY101', 4, 'Prof. Johnson'),
('Database Design', 'DB101', 3, 'Dr. Williams'),
('Advanced SQL', 'SQL201', 4, 'Dr. Kumar'),
('ETL Development', 'ETL101', 3, 'Ms. Garcia');

-- 3. INSERT ENROLLMENTS
INSERT INTO enrollments (student_id, course_id, grade)
VALUES 
(1, 1, 'A'),      -- Alice in Data Engineering
(1, 2, 'B'),      -- Alice in Python Basics
(2, 2, 'A'),      -- Bob in Python Basics
(2, 3, 'B'),      -- Bob in Database Design
(3, 3, 'A'),      -- Charlie in Database Design
(3, 4, 'B'),      -- Charlie in Advanced SQL
(4, 1, 'B'),      -- Diana in Data Engineering
(4, 5, 'A'),      -- Diana in ETL Development
(5, 4, 'A'),      -- Eve in Advanced SQL
(5, 5, 'A');      -- Eve in ETL Development

-- Verify data insertion
SELECT 'Students' AS table_name, COUNT(*) AS row_count FROM students
UNION ALL
SELECT 'Courses', COUNT(*) FROM courses
UNION ALL
SELECT 'Enrollments', COUNT(*) FROM enrollments;
