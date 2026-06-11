-- ============================================
-- 04_SAMPLE_QUERIES.SQL
-- Useful SQL queries for learning and data analysis
-- ============================================

-- Query 1: Get all students
SELECT * FROM students;

-- Query 2: Get all courses
SELECT * FROM courses;

-- Query 3: Get all enrollments with student and course names
SELECT 
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_name,
    e.grade,
    e.enrollment_date
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
ORDER BY s.first_name;

-- Query 4: Get students with grade A
SELECT 
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_name,
    e.grade
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE e.grade = 'A'
ORDER BY s.first_name;

-- Query 5: Count courses per student
SELECT 
    s.first_name || ' ' || s.last_name AS student_name,
    COUNT(e.enrollment_id) AS num_courses
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
ORDER BY num_courses DESC;

-- Query 6: Get course enrollment statistics
SELECT 
    c.course_name,
    COUNT(e.enrollment_id) AS total_students,
    AVG(CASE WHEN e.grade = 'A' THEN 1 ELSE 0 END) * 100 AS percent_A_grades
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
ORDER BY total_students DESC;

-- Query 7: Find students enrolled in multiple courses
SELECT 
    s.first_name || ' ' || s.last_name AS student_name,
    COUNT(e.enrollment_id) AS num_courses
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.enrollment_id) > 1
ORDER BY num_courses DESC;

-- Query 8: Get student with highest grades
SELECT 
    s.first_name || ' ' || s.last_name AS student_name,
    AVG(CASE 
        WHEN e.grade = 'A' THEN 5
        WHEN e.grade = 'B' THEN 4
        WHEN e.grade = 'C' THEN 3
        WHEN e.grade = 'D' THEN 2
        ELSE 1
    END) AS avg_grade_score
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
ORDER BY avg_grade_score DESC;
