-- ============================================
-- 02_CREATE_TABLES.SQL
-- Step 2: Create tables with relationships
-- ============================================
-- This script creates the data model with 3 main tables

-- 1. STUDENTS TABLE
-- Stores information about students
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    date_of_birth DATE,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE students IS 'Stores student information';
COMMENT ON COLUMN students.student_id IS 'Unique identifier for each student';
COMMENT ON COLUMN students.email IS 'Student email (must be unique)';

-- 2. COURSES TABLE
-- Stores information about available courses
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    instructor VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE courses IS 'Stores course information';
COMMENT ON COLUMN courses.course_code IS 'Unique course code (e.g., DE101)';

-- 3. ENROLLMENTS TABLE
-- Links students to courses (Many-to-Many relationship)
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

COMMENT ON TABLE enrollments IS 'Junction table linking students and courses';
COMMENT ON COLUMN enrollments.grade IS 'Student grade (A, B, C, D, F)';

-- Create indexes for better query performance
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_courses_code ON courses(course_code);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);

-- Verify table creation
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
