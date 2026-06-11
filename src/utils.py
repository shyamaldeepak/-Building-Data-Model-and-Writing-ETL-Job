"""
utils.py
Utility functions for ETL operations
"""

import psycopg2
from datetime import datetime
from src.config import DB_CONFIG

def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        psycopg2 connection object
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        raise

def log_message(level, message):
    """
    Print timestamped log message
    
    Args:
        level: Log level (INFO, ERROR, WARNING, SUCCESS)
        message: Message to log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def validate_email(email):
    """
    Simple email validation
    
    Args:
        email: Email string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or '@' not in email:
        return False
    return True

def validate_phone(phone):
    """
    Simple phone validation (10+ digits)
    
    Args:
        phone: Phone string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return True  # Phone is optional
    digits_only = ''.join(c for c in phone if c.isdigit())
    return len(digits_only) >= 10

def sanitize_string(value):
    """
    Remove extra whitespace and convert to lowercase for consistency
    
    Args:
        value: String to sanitize
    
    Returns:
        str: Cleaned string
    """
    if value is None:
        return None
    return str(value).strip().lower()

def execute_query(connection, query, fetch_all=False):
    """
    Execute a SELECT query and return results
    
    Args:
        connection: Database connection
        query: SQL query string
        fetch_all: If True, return all rows; if False, return one row
    
    Returns:
        Query results or None
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        if fetch_all:
            results = cursor.fetchall()
        else:
            results = cursor.fetchone()
        
        cursor.close()
        return results
    except Exception as e:
        log_message("ERROR", f"Query execution failed: {e}")
        return None

def execute_insert(connection, query, data_tuple):
    """
    Execute an INSERT query
    
    Args:
        connection: Database connection
        query: SQL INSERT query with %s placeholders
        data_tuple: Tuple of values to insert
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, data_tuple)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        connection.rollback()
        log_message("ERROR", f"Insert failed: {e}")
        return False

# Test utilities
if __name__ == "__main__":
    print("Testing utility functions...")
    print(f"Email validation (valid): {validate_email('test@example.com')}")
    print(f"Email validation (invalid): {validate_email('testexample.com')}")
    print(f"Phone validation (10 digits): {validate_phone('1234567890')}")
    print(f"Phone validation (short): {validate_phone('123')}")
    print(f"Sanitize: '{sanitize_string('  Hello World  ')}'")
    log_message("INFO", "Utility functions working correctly!")
