"""
demo_database.py - Shows database concepts using in-memory SQLite
No PostgreSQL setup needed! Uses SQLite which works out of the box.
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

class DatabaseDemo:
    """Demonstrate database operations without PostgreSQL"""
    
    def __init__(self, db_file='demo_database.db'):
        self.db_file = db_file
        self.connection = None
        
    def connect(self):
        """Create or connect to SQLite database"""
        self.connection = sqlite3.connect(self.db_file)
        print(f"[CONNECT] ✅ Connected to database: {self.db_file}\n")
        
    def create_tables(self):
        """Create database tables"""
        print("[SCHEMA] Creating database tables...")
        
        cursor = self.connection.cursor()
        
        # Create STUDENTS table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                date_of_birth DATE,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("  ✓ Created 'students' table")
        
        # Create COURSES table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                course_code TEXT UNIQUE,
                credits INTEGER,
                instructor TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("  ✓ Created 'courses' table")
        
        # Create ENROLLMENTS table (junction table)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                grade TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        print("  ✓ Created 'enrollments' table")
        
        self.connection.commit()
        print("[SCHEMA] ✅ Tables created successfully!\n")
    
    def insert_sample_data(self):
        """Insert sample data"""
        print("[DATA] Inserting sample data...")
        
        cursor = self.connection.cursor()
        
        # Insert students
        students = [
            ('Alice', 'Johnson', 'alice.johnson@example.com', '1234567890', '2005-05-15'),
            ('Bob', 'Smith', 'bob.smith@example.com', '0987654321', '2006-08-22'),
            ('Charlie', 'Brown', 'charlie.brown@example.com', '5555555555', '2005-12-10'),
        ]
        
        for student in students:
            cursor.execute('''
                INSERT INTO students (first_name, last_name, email, phone, date_of_birth)
                VALUES (?, ?, ?, ?, ?)
            ''', student)
        print(f"  ✓ Inserted {len(students)} students")
        
        # Insert courses
        courses = [
            ('Data Engineering 101', 'DE101', 3, 'Dr. Smith'),
            ('Python Basics', 'PY101', 4, 'Prof. Johnson'),
            ('Database Design', 'DB101', 3, 'Dr. Williams'),
        ]
        
        for course in courses:
            cursor.execute('''
                INSERT INTO courses (course_name, course_code, credits, instructor)
                VALUES (?, ?, ?, ?)
            ''', course)
        print(f"  ✓ Inserted {len(courses)} courses")
        
        # Insert enrollments
        enrollments = [
            (1, 1, 'A'),
            (1, 2, 'B'),
            (2, 2, 'A'),
            (2, 3, 'B'),
            (3, 1, 'B'),
        ]
        
        for enrollment in enrollments:
            cursor.execute('''
                INSERT INTO enrollments (student_id, course_id, grade)
                VALUES (?, ?, ?)
            ''', enrollment)
        print(f"  ✓ Inserted {len(enrollments)} enrollments")
        
        self.connection.commit()
        print("[DATA] ✅ Sample data inserted!\n")
    
    def query_data(self, query_name, sql):
        """Execute and display query results"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        df = pd.DataFrame(rows, columns=columns)
        
        print(f"📊 {query_name}")
        print("─" * 80)
        print(df.to_string(index=False) if len(df) > 0 else "No results")
        print()
        return df
    
    def run_demo(self):
        """Run complete database demo"""
        print("\n" + "=" * 80)
        print("🗄️  DATABASE DEMO - Using SQLite (No PostgreSQL needed!)")
        print("=" * 80 + "\n")
        
        try:
            # Step 1: Connect
            self.connect()
            
            # Step 2: Create tables
            self.create_tables()
            
            # Step 3: Insert data
            self.insert_sample_data()
            
            # Step 4: Run queries
            print("[QUERIES] Executing sample queries...\n")
            
            # Query 1: All students
            self.query_data(
                "All Students",
                "SELECT * FROM students ORDER BY first_name"
            )
            
            # Query 2: All courses
            self.query_data(
                "All Courses",
                "SELECT * FROM courses ORDER BY course_name"
            )
            
            # Query 3: Student courses with grades
            self.query_data(
                "Student Courses (with JOINs)",
                """
                SELECT 
                    s.first_name || ' ' || s.last_name AS student_name,
                    c.course_name,
                    e.grade
                FROM students s
                JOIN enrollments e ON s.student_id = e.student_id
                JOIN courses c ON e.course_id = c.course_id
                ORDER BY s.first_name
                """
            )
            
            # Query 4: Students with Grade A
            self.query_data(
                "Top Students (Grade A)",
                """
                SELECT 
                    s.first_name || ' ' || s.last_name AS student_name,
                    c.course_name,
                    e.grade
                FROM students s
                JOIN enrollments e ON s.student_id = e.student_id
                JOIN courses c ON e.course_id = c.course_id
                WHERE e.grade = 'A'
                """
            )
            
            # Query 5: Course enrollment count
            self.query_data(
                "Course Enrollment Statistics",
                """
                SELECT 
                    c.course_name,
                    COUNT(e.enrollment_id) AS total_students,
                    COUNT(CASE WHEN e.grade = 'A' THEN 1 END) AS grade_a_count
                FROM courses c
                LEFT JOIN enrollments e ON c.course_id = e.course_id
                GROUP BY c.course_id, c.course_name
                """
            )
            
            print("=" * 80)
            print("✅ DATABASE DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            
            # Show table info
            print("\n📋 Database Information:")
            print(f"  • Database File: {self.db_file}")
            print(f"  • Tables: students, courses, enrollments")
            print(f"  • Total Students: {len(self.query_data('', 'SELECT COUNT(*) FROM students'))}")
            print(f"  • Total Courses: {len(self.query_data('', 'SELECT COUNT(*) FROM courses'))}")
            print(f"  • Total Enrollments: {len(self.query_data('', 'SELECT COUNT(*) FROM enrollments'))}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        finally:
            if self.connection:
                self.connection.close()
                print("\n[CLOSE] ✅ Database connection closed")


# Run the demo
if __name__ == "__main__":
    demo = DatabaseDemo('demo_database.db')
    demo.run_demo()
    
    print("\n💡 This demo uses SQLite for quick local testing.")
    print("For production, use PostgreSQL (as shown in README.md)")
