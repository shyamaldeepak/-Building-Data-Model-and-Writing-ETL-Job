# 📊 Building Data Model and Writing ETL Job

## 🎯 Project Overview

This project is a **complete guide to Data Engineering fundamentals**. You will learn how to:
- **Design and build database models** (tables, relationships, schemas)
- **Write ETL jobs** (Extract, Transform, Load data)
- **Work with PostgreSQL** databases
- **Query data** using SQL and Python
- **Understand DBMS** (Database Management System) basics

This is a **hands-on project** suitable for **school students, beginners, and junior data engineers**.

---

## ✅ What You Will Learn

| Topic | Description |
|-------|-------------|
| **Python** | Write Python scripts for data processing and ETL automation |
| **SQL** | Create databases, tables, and write complex queries |
| **Building Data Models** | Design efficient database schemas with tables and relationships |
| **Basics of DBMS** | Understand how databases store, organize, and retrieve data |
| **Writing ETL Jobs** | Extract data from sources, transform it, and load into databases |
| **Querying Data Programmatically** | Use Python with databases to fetch and manipulate data |
| **PostgreSQL** | Learn industry-standard relational database system |

---

## 📋 Prerequisites

### What You Need to Know (Basics)
- Basic Python programming (if, loops, functions)
- Basic understanding of tables/spreadsheets
- Familiarity with terminal/command line

### What You Need to Install
- Python 3.8+ ([Download here](https://www.python.org/downloads/))
- PostgreSQL ([Download here](https://www.postgresql.org/download/))
- Git ([Download here](https://git-scm.com/))
- Any code editor (VS Code, PyCharm, or any text editor)

---

## 📁 Project Structure

```
project/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── data/
│   ├── raw_data.csv                   # Sample raw data
│   └── transformed_data.csv           # Processed data
├── sql/
│   ├── 01_create_database.sql         # Database creation script
│   ├── 02_create_tables.sql           # Table creation script
│   └── 03_sample_queries.sql          # Example queries
├── src/
│   ├── etl_job.py                     # Main ETL script
│   ├── config.py                      # Database configuration
│   └── utils.py                       # Helper functions
└── notebooks/
    └── exploration.ipynb              # Data exploration (optional)
```

---

## 🔑 Key Concepts Explained (For Beginners)

### 1. **What is a Database?**
Think of a database as a **super-organized spreadsheet** that can store millions of rows efficiently. Instead of one massive Excel file, databases split data into related tables.

**Example:** A student database might have:
- `students` table (student ID, name, email)
- `courses` table (course ID, course name)
- `enrollment` table (which student is in which course)

### 2. **What is a Data Model?**
A data model is the **blueprint** of your database. It defines:
- What **tables** you need
- What **columns** each table has
- How **tables relate** to each other

**Example:**
```
STUDENTS Table:
┌─────────┬──────────┬──────────────┐
│ ID      │ Name     │ Email        │
├─────────┼──────────┼──────────────┤
│ 101     │ Alice    │ alice@ex.com │
│ 102     │ Bob      │ bob@ex.com   │
└─────────┴──────────┴──────────────┘
```

### 3. **What is DBMS?**
DBMS = Database Management System. It's **software that manages databases**.

**Examples:** PostgreSQL, MySQL, Oracle, SQL Server

**What it does:**
- Stores data safely
- Retrieves data quickly
- Keeps data organized
- Prevents data corruption

### 4. **What is SQL?**
SQL = Structured Query Language. It's the **language to talk to databases**.

**Example:**
```sql
-- Get all students named Alice
SELECT * FROM students WHERE name = 'Alice';
```

### 5. **What is ETL?**

**ETL = Extract, Transform, Load**

```
Raw Data (CSV, JSON, API) 
    ↓
  EXTRACT
    ↓
Process & Clean Data
    ↓
  TRANSFORM
    ↓
Insert into Database
    ↓
   LOAD
    ↓
Database (PostgreSQL)
```

**Simple Example:**
- **Extract:** Read data from a CSV file
- **Transform:** Clean data, remove duplicates, convert formats
- **Load:** Insert clean data into database

### 6. **What is PostgreSQL?**
PostgreSQL is a **powerful, free, open-source relational database**.

**Why use it?**
- Industry-standard
- Free to use
- Handles large datasets
- Great for learning

---

## 🚀 Step-by-Step Setup & Running Guide

### Step 1: Install PostgreSQL

**On Windows:**
1. Download from https://www.postgresql.org/download/
2. Run the installer
3. Choose default settings (remember the password you set)
4. PostgreSQL will be installed with pgAdmin (GUI tool)

**On macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

**Verify Installation:**
```bash
psql --version
# Should show: psql (PostgreSQL) 15.x (or similar)
```

---

### Step 2: Set Up Python Environment

**Step 2.1: Clone or Create Project Folder**
```bash
cd ~/Desktop  # Go to where you want the project
mkdir data-engineering-project
cd data-engineering-project
```

**Step 2.2: Create Python Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` at the start of your terminal line.**

**Step 2.3: Install Required Python Packages**

Create a file named `requirements.txt` with:
```
psycopg2-binary==2.9.6
pandas==2.0.0
python-dotenv==1.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

---

### Step 3: Create PostgreSQL Database

**Step 3.1: Login to PostgreSQL**
```bash
psql -U postgres
```
You'll be prompted for the password (the one you set during installation).

**Step 3.2: Create Database**
```sql
CREATE DATABASE student_management;
\c student_management
```

The output `You are now connected to database "student_management"` means you're in!

**Step 3.3: Create Tables**

Copy-paste this SQL code:

```sql
-- Create STUDENTS table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    date_of_birth DATE,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create COURSES table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    instructor VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ENROLLMENTS table (links students to courses)
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

**Step 3.4: Insert Sample Data**

```sql
-- Insert Students
INSERT INTO students (first_name, last_name, email, phone, date_of_birth)
VALUES 
('Alice', 'Johnson', 'alice@example.com', '1234567890', '2005-05-15'),
('Bob', 'Smith', 'bob@example.com', '0987654321', '2006-08-22'),
('Charlie', 'Brown', 'charlie@example.com', '5555555555', '2005-12-10');

-- Insert Courses
INSERT INTO courses (course_name, course_code, credits, instructor)
VALUES 
('Data Engineering 101', 'DE101', 3, 'Dr. Smith'),
('Python Basics', 'PY101', 4, 'Prof. Johnson'),
('Database Design', 'DB101', 3, 'Dr. Williams');

-- Insert Enrollments
INSERT INTO enrollments (student_id, course_id, grade)
VALUES 
(1, 1, 'A'),
(1, 2, 'B'),
(2, 2, 'A'),
(3, 3, 'B');
```

**Verify Data:**
```sql
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM enrollments;
```

**To exit PostgreSQL:**
```sql
\q
```

---

### Step 4: Create Python ETL Job

Create a file named `etl_job.py`:

```python
import psycopg2
import pandas as pd
from datetime import datetime

# Database connection details
DB_CONFIG = {
    'host': 'localhost',
    'database': 'student_management',
    'user': 'postgres',
    'password': 'your_password',  # Replace with your PostgreSQL password
    'port': 5432
}

class ETLJob:
    def __init__(self):
        self.connection = None
        
    def extract(self, csv_file):
        """Extract data from CSV file"""
        print(f"[EXTRACT] Reading data from {csv_file}...")
        df = pd.read_csv(csv_file)
        print(f"[EXTRACT] Successfully loaded {len(df)} rows")
        return df
    
    def transform(self, df):
        """Transform and clean data"""
        print("[TRANSFORM] Starting data transformation...")
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Fill missing values
        df = df.fillna('Unknown')
        
        # Convert email to lowercase
        if 'email' in df.columns:
            df['email'] = df['email'].str.lower()
        
        print(f"[TRANSFORM] Transformation complete. {len(df)} rows ready for load")
        return df
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("[CONNECT] Successfully connected to PostgreSQL")
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            raise
    
    def load(self, df, table_name):
        """Load data into PostgreSQL table"""
        print(f"[LOAD] Loading data into {table_name} table...")
        
        cursor = self.connection.cursor()
        
        for idx, row in df.iterrows():
            columns = ', '.join(df.columns)
            values = ', '.join(['%s' for _ in df.columns])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            
            try:
                cursor.execute(sql, tuple(row))
            except Exception as e:
                print(f"[ERROR] Row {idx} failed: {e}")
        
        self.connection.commit()
        print(f"[LOAD] Successfully loaded {len(df)} rows into {table_name}")
    
    def run(self, csv_file, table_name):
        """Run complete ETL pipeline"""
        print("=" * 50)
        print("🚀 STARTING ETL JOB")
        print("=" * 50)
        
        start_time = datetime.now()
        
        try:
            self.connect()
            df = self.extract(csv_file)
            df = self.transform(df)
            self.load(df, table_name)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("=" * 50)
            print("✅ ETL JOB COMPLETED SUCCESSFULLY")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ ETL JOB FAILED: {e}")
        finally:
            if self.connection:
                self.connection.close()

# Run the ETL job
if __name__ == "__main__":
    etl = ETLJob()
    # Make sure you have a CSV file to load
    # etl.run('data/sample_data.csv', 'students')
    print("ETL Job module loaded successfully!")
```

---

### Step 5: Query Data with Python

Create a file named `query_data.py`:

```python
import psycopg2
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'database': 'student_management',
    'user': 'postgres',
    'password': 'your_password',  # Replace with your PostgreSQL password
    'port': 5432
}

class DataAnalyzer:
    def __init__(self):
        self.connection = psycopg2.connect(**DB_CONFIG)
        
    def query(self, sql):
        """Execute SQL query and return results"""
        df = pd.read_sql_query(sql, self.connection)
        return df
    
    def get_all_students(self):
        """Get all students"""
        sql = "SELECT * FROM students;"
        return self.query(sql)
    
    def get_student_courses(self, student_id):
        """Get all courses for a student"""
        sql = f"""
        SELECT s.first_name, s.last_name, c.course_name, e.grade
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE s.student_id = {student_id};
        """
        return self.query(sql)
    
    def get_top_students(self):
        """Get students with grade A"""
        sql = """
        SELECT s.first_name, s.last_name, c.course_name, e.grade
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.grade = 'A'
        ORDER BY s.first_name;
        """
        return self.query(sql)
    
    def close(self):
        self.connection.close()

# Example usage
if __name__ == "__main__":
    analyzer = DataAnalyzer()
    
    print("\n=== ALL STUDENTS ===")
    print(analyzer.get_all_students())
    
    print("\n=== STUDENT 1 COURSES ===")
    print(analyzer.get_student_courses(1))
    
    print("\n=== TOP STUDENTS ===")
    print(analyzer.get_top_students())
    
    analyzer.close()
```

**Run the query script:**
```bash
python query_data.py
```

---

## 📚 Important SQL Queries to Know

```sql
-- 1. Create a table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- 2. Insert data
INSERT INTO students (name, email) VALUES ('John', 'john@example.com');

-- 3. Select data
SELECT * FROM students;

-- 4. Update data
UPDATE students SET email = 'newemail@example.com' WHERE name = 'John';

-- 5. Delete data
DELETE FROM students WHERE student_id = 1;

-- 6. Join multiple tables
SELECT s.name, c.course_name
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id;

-- 7. Group and aggregate
SELECT course_id, COUNT(*) as total_students
FROM enrollments
GROUP BY course_id;

-- 8. Filter with WHERE
SELECT * FROM students WHERE email LIKE '%example.com%';
```

---

## 🔧 Common Troubleshooting

| Problem | Solution |
|---------|----------|
| `psycopg2.OperationalError: could not connect` | Check if PostgreSQL is running. Verify DB_CONFIG credentials. |
| `relation "students" does not exist` | Make sure you created the tables. Run the CREATE TABLE script. |
| `(venv) not showing in terminal` | Run: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows) |
| `Permission denied` | Run PostgreSQL with admin/sudo if on Linux. |
| `ModuleNotFoundError: psycopg2` | Install requirements: `pip install -r requirements.txt` |

---

## 📖 Learning Path

**Week 1:**
- [ ] Install PostgreSQL & Python
- [ ] Understand database basics
- [ ] Learn SQL basics (CREATE, INSERT, SELECT)

**Week 2:**
- [ ] Build your data model
- [ ] Create tables with relationships
- [ ] Insert sample data

**Week 3:**
- [ ] Learn Python psycopg2
- [ ] Write Python scripts to query data
- [ ] Understand joins and complex queries

**Week 4:**
- [ ] Learn ETL concepts
- [ ] Write your first ETL job
- [ ] Transform and load real data

---

## 💡 Real-World Example

Let's say you work for a company and need to:

**Problem:** Load employee data from a CSV file into a PostgreSQL database

**Solution (ETL):**
1. **Extract:** Read CSV file with employee data
2. **Transform:** 
   - Remove duplicates
   - Convert salary to number format
   - Validate email addresses
3. **Load:** Insert clean data into `employees` table

This is exactly what the `etl_job.py` script does!

---

## 🎓 Resources for Learning

- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **SQL Tutorial:** https://www.w3schools.com/sql/
- **Python with Databases:** https://realpython.com/introduction-to-psycopg2/
- **Data Modeling:** https://en.wikipedia.org/wiki/Data_model

---

## 📝 Next Steps

1. ✅ Follow the setup guide step-by-step
2. ✅ Create and populate the database
3. ✅ Run the Python scripts
4. ✅ Modify the data and see how it changes
5. ✅ Write your own SQL queries
6. ✅ Create your own ETL job for different data

---

## ❓ Need Help?

- Check the **Troubleshooting** section
- Google the error message
- Ask on Stack Overflow
- Reread the concept explanation above

---

## 📌 Key Takeaways

✅ **Data Models** help organize data efficiently  
✅ **SQL** is the language of databases  
✅ **ETL** is how real-world data moves  
✅ **PostgreSQL** is powerful and free  
✅ **Python** makes database automation easy  
✅ **DBMS** keeps data safe and organized  

---

**Happy Learning! 🚀 You're on your way to becoming a Data Engineer!**

---

*Last Updated: 2026-06-11*