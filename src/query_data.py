"""
query_data.py
Query and analyze data from the database
"""

import psycopg2
import pandas as pd
from src.config import DB_CONFIG
from src.utils import log_message

class DataAnalyzer:
    """
    Class to query and analyze data from the database
    """
    
    def __init__(self):
        """Initialize data analyzer"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            log_message("INFO", "Connected to database")
        except Exception as e:
            log_message("ERROR", f"Failed to connect to database: {e}")
            raise
    
    def query(self, sql, fetch_all=True):
        """
        Execute a SQL query and return results
        
        Args:
            sql: SQL query string
            fetch_all: If True, return all rows; if False, return one row
        
        Returns:
            pandas DataFrame or None
        """
        try:
            df = pd.read_sql_query(sql, self.connection)
            return df
        except Exception as e:
            log_message("ERROR", f"Query execution failed: {e}")
            return None
    
    def get_all_students(self):
        """Get all students"""
        sql = """
        SELECT 
            student_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            enrollment_date
        FROM students
        ORDER BY first_name;
        """
        df = self.query(sql)
        log_message("INFO", f"Retrieved {len(df)} students")
        return df
    
    def get_all_courses(self):
        """Get all courses"""
        sql = """
        SELECT 
            course_id,
            course_name,
            course_code,
            credits,
            instructor,
            created_date
        FROM courses
        ORDER BY course_name;
        """
        df = self.query(sql)
        log_message("INFO", f"Retrieved {len(df)} courses")
        return df
    
    def get_student_courses(self, student_id):
        """
        Get all courses for a specific student
        
        Args:
            student_id: ID of the student
        
        Returns:
            pandas DataFrame with student's courses and grades
        """
        sql = f"""
        SELECT 
            s.first_name || ' ' || s.last_name AS student_name,
            c.course_name,
            c.course_code,
            c.credits,
            e.grade,
            e.enrollment_date
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE s.student_id = {student_id}
        ORDER BY e.enrollment_date;
        """
        df = self.query(sql)
        if df is not None and len(df) > 0:
            log_message("INFO", f"Retrieved {len(df)} courses for student {student_id}")
        else:
            log_message("WARNING", f"No courses found for student {student_id}")
        return df
    
    def get_student_by_email(self, email):
        """
        Get student by email
        
        Args:
            email: Student email
        
        Returns:
            pandas DataFrame with student details
        """
        sql = f"""
        SELECT * FROM students
        WHERE email = '{email}'
        LIMIT 1;
        """
        df = self.query(sql)
        if df is not None and len(df) > 0:
            log_message("INFO", f"Found student: {email}")
        else:
            log_message("WARNING", f"No student found with email: {email}")
        return df
    
    def get_top_students(self, limit=5):
        """
        Get top performing students (with grade A)
        
        Args:
            limit: Number of top students to return
        
        Returns:
            pandas DataFrame with top students
        """
        sql = f"""
        SELECT 
            s.first_name || ' ' || s.last_name AS student_name,
            COUNT(e.enrollment_id) AS courses_completed,
            COUNT(CASE WHEN e.grade = 'A' THEN 1 END) AS grade_a_count,
            ROUND(
                COUNT(CASE WHEN e.grade = 'A' THEN 1 END)::numeric / 
                COUNT(e.enrollment_id) * 100, 2
            ) AS grade_a_percentage
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        GROUP BY s.student_id, s.first_name, s.last_name
        HAVING COUNT(CASE WHEN e.grade = 'A' THEN 1 END) > 0
        ORDER BY grade_a_percentage DESC
        LIMIT {limit};
        """
        df = self.query(sql)
        log_message("INFO", f"Retrieved top {len(df)} students")
        return df
    
    def get_course_statistics(self):
        """
        Get statistics for each course
        
        Returns:
            pandas DataFrame with course stats
        """
        sql = """
        SELECT 
            c.course_name,
            c.course_code,
            c.credits,
            c.instructor,
            COUNT(e.enrollment_id) AS total_students,
            COUNT(CASE WHEN e.grade = 'A' THEN 1 END) AS grade_a_count,
            COUNT(CASE WHEN e.grade = 'B' THEN 1 END) AS grade_b_count,
            ROUND(
                COUNT(CASE WHEN e.grade = 'A' THEN 1 END)::numeric / 
                COUNT(e.enrollment_id) * 100, 2
            ) AS percent_a_grades
        FROM courses c
        LEFT JOIN enrollments e ON c.course_id = e.course_id
        GROUP BY c.course_id, c.course_name, c.course_code, c.credits, c.instructor
        ORDER BY total_students DESC;
        """
        df = self.query(sql)
        log_message("INFO", f"Retrieved statistics for {len(df)} courses")
        return df
    
    def get_enrollment_summary(self):
        """
        Get enrollment summary statistics
        
        Returns:
            pandas DataFrame with enrollment stats
        """
        sql = """
        SELECT 
            COUNT(DISTINCT student_id) AS total_students,
            COUNT(DISTINCT course_id) AS total_courses,
            COUNT(*) AS total_enrollments,
            ROUND(COUNT(*)::numeric / COUNT(DISTINCT student_id), 2) AS avg_courses_per_student
        FROM enrollments;
        """
        df = self.query(sql)
        if df is not None:
            log_message("INFO", "Enrollment summary retrieved")
        return df
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            log_message("INFO", "Database connection closed")


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DATA ANALYZER - Query Examples")
    print("=" * 60 + "\n")
    
    try:
        analyzer = DataAnalyzer()
        
        # Display all students
        print("\n📚 ALL STUDENTS:")
        print("-" * 60)
        df_students = analyzer.get_all_students()
        if df_students is not None:
            print(df_students.to_string(index=False))
        
        # Display all courses
        print("\n📖 ALL COURSES:")
        print("-" * 60)
        df_courses = analyzer.get_all_courses()
        if df_courses is not None:
            print(df_courses.to_string(index=False))
        
        # Display course statistics
        print("\n📊 COURSE STATISTICS:")
        print("-" * 60)
        df_stats = analyzer.get_course_statistics()
        if df_stats is not None:
            print(df_stats.to_string(index=False))
        
        # Display top students
        print("\n🏆 TOP STUDENTS:")
        print("-" * 60)
        df_top = analyzer.get_top_students()
        if df_top is not None:
            print(df_top.to_string(index=False))
        
        # Display enrollment summary
        print("\n📈 ENROLLMENT SUMMARY:")
        print("-" * 60)
        df_summary = analyzer.get_enrollment_summary()
        if df_summary is not None:
            print(df_summary.to_string(index=False))
        
        analyzer.close()
        
        print("\n" + "=" * 60)
        print("✅ Queries completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        log_message("ERROR", f"Error in data analyzer: {e}")
