# Quick Start Guide

This is a **quick reference** to get the project running. For detailed information, see `README.md`.

## ⚡ Quick Setup (5 minutes)

### 1. Install PostgreSQL
- **Windows/Mac**: Download from https://www.postgresql.org/
- **Linux**: `sudo apt install postgresql`

### 2. Install Python Requirements
```bash
pip install -r requirements.txt
```

### 3. Create Database & Tables
```bash
psql -U postgres
```

Then copy-paste this:
```sql
CREATE DATABASE student_management;
\c student_management
```

Then run all SQL scripts:
```bash
psql -U postgres -d student_management -f sql/02_create_tables.sql
psql -U postgres -d student_management -f sql/03_insert_sample_data.sql
```

### 4. Run Queries
```bash
python src/query_data.py
```

### 5. Run ETL Job
```bash
python src/etl_job.py
```

## 📁 File Structure

```
project/
├── README.md                    ← Full documentation
├── requirements.txt             ← Python dependencies
├── QUICKSTART.md               ← This file
├── sql/                        ← SQL scripts
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_insert_sample_data.sql
│   └── 04_sample_queries.sql
├── src/                        ← Python source code
│   ├── __init__.py
│   ├── config.py              ← Database config
│   ├── utils.py               ← Helper functions
│   ├── etl_job.py             ← ETL pipeline
│   └── query_data.py          ← Query analyzer
└── data/                       ← CSV data files
    └── sample_students.csv
```

## 🔧 Common Commands

**Test database connection:**
```bash
psql -U postgres -d student_management -c "SELECT * FROM students;"
```

**View all students:**
```bash
python src/query_data.py
```

**Get course statistics:**
```bash
psql -U postgres -d student_management -f sql/04_sample_queries.sql
```

**Run ETL (with CSV file):**
```python
from src.etl_job import ETLJob
etl = ETLJob()
etl.run('data/sample_students.csv', 'students')
```

## ❓ Need Help?

See the **Troubleshooting** section in `README.md`
