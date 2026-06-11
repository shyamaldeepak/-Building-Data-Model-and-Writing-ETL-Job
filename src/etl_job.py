"""
etl_job.py
Main ETL (Extract, Transform, Load) job for the project
This script demonstrates the complete ETL workflow
"""

import psycopg2
import pandas as pd
from datetime import datetime
from src.config import DB_CONFIG
from src.utils import log_message, validate_email, validate_phone, sanitize_string

class ETLJob:
    """
    ETL Job class that handles Extract, Transform, and Load operations
    """
    
    def __init__(self):
        """Initialize ETL job"""
        self.connection = None
        self.extracted_data = None
        self.transformed_data = None
        
    def extract(self, csv_file):
        """
        EXTRACT: Read data from CSV file
        
        Args:
            csv_file: Path to CSV file
        
        Returns:
            pandas DataFrame with extracted data
        """
        try:
            log_message("EXTRACT", f"Reading data from {csv_file}...")
            df = pd.read_csv(csv_file)
            log_message("EXTRACT", f"✅ Successfully loaded {len(df)} rows")
            self.extracted_data = df
            return df
        except Exception as e:
            log_message("ERROR", f"Extract failed: {e}")
            raise
    
    def transform(self, df):
        """
        TRANSFORM: Clean and prepare data
        
        Args:
            df: pandas DataFrame to transform
        
        Returns:
            Cleaned pandas DataFrame
        """
        log_message("TRANSFORM", "Starting data transformation...")
        
        try:
            # Step 1: Remove duplicate rows
            initial_count = len(df)
            df = df.drop_duplicates()
            duplicates_removed = initial_count - len(df)
            if duplicates_removed > 0:
                log_message("TRANSFORM", f"  - Removed {duplicates_removed} duplicate rows")
            
            # Step 2: Fill missing values
            missing_before = df.isnull().sum().sum()
            df = df.fillna('Unknown')
            if missing_before > 0:
                log_message("TRANSFORM", f"  - Filled {missing_before} missing values")
            
            # Step 3: Convert email to lowercase
            if 'email' in df.columns:
                df['email'] = df['email'].str.lower()
                log_message("TRANSFORM", "  - Converted emails to lowercase")
            
            # Step 4: Convert first_name and last_name to title case
            if 'first_name' in df.columns:
                df['first_name'] = df['first_name'].str.title()
            if 'last_name' in df.columns:
                df['last_name'] = df['last_name'].str.title()
                log_message("TRANSFORM", "  - Converted names to title case")
            
            # Step 5: Remove whitespace from phone
            if 'phone' in df.columns:
                df['phone'] = df['phone'].str.replace(' ', '')
                log_message("TRANSFORM", "  - Cleaned phone numbers")
            
            log_message("TRANSFORM", f"✅ Transformation complete. {len(df)} rows ready for load")
            self.transformed_data = df
            return df
            
        except Exception as e:
            log_message("ERROR", f"Transform failed: {e}")
            raise
    
    def connect(self):
        """
        Connect to PostgreSQL database
        """
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            log_message("CONNECT", "✅ Successfully connected to PostgreSQL")
        except Exception as e:
            log_message("ERROR", f"Failed to connect: {e}")
            raise
    
    def load(self, df, table_name):
        """
        LOAD: Insert data into database table
        
        Args:
            df: pandas DataFrame to load
            table_name: Name of target database table
        """
        log_message("LOAD", f"Loading data into '{table_name}' table...")
        
        try:
            cursor = self.connection.cursor()
            loaded_count = 0
            failed_count = 0
            
            for idx, row in df.iterrows():
                try:
                    # Build INSERT query dynamically
                    columns = ', '.join(df.columns)
                    placeholders = ', '.join(['%s' for _ in df.columns])
                    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    
                    # Execute insert
                    cursor.execute(sql, tuple(row))
                    loaded_count += 1
                    
                except psycopg2.IntegrityError as e:
                    # Handle constraint violations (e.g., duplicate email)
                    self.connection.rollback()
                    log_message("WARNING", f"  Row {idx} skipped (constraint violation): {e}")
                    failed_count += 1
                    cursor = self.connection.cursor()  # Reset cursor
                except Exception as e:
                    self.connection.rollback()
                    log_message("ERROR", f"  Row {idx} failed: {e}")
                    failed_count += 1
                    cursor = self.connection.cursor()  # Reset cursor
            
            self.connection.commit()
            log_message("LOAD", f"✅ Successfully loaded {loaded_count} rows into '{table_name}'")
            if failed_count > 0:
                log_message("WARNING", f"  {failed_count} rows failed to load")
            
            cursor.close()
            
        except Exception as e:
            log_message("ERROR", f"Load failed: {e}")
            raise
    
    def validate(self, df):
        """
        Validate data before loading
        
        Args:
            df: pandas DataFrame to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        log_message("VALIDATE", "Validating data...")
        
        is_valid = True
        
        # Check for required columns
        if 'first_name' not in df.columns or 'last_name' not in df.columns:
            log_message("ERROR", "  Missing required columns: first_name, last_name")
            is_valid = False
        
        # Validate emails if present
        if 'email' in df.columns:
            invalid_emails = df[~df['email'].apply(validate_email)].index.tolist()
            if invalid_emails:
                log_message("WARNING", f"  {len(invalid_emails)} invalid emails found")
        
        # Validate phones if present
        if 'phone' in df.columns:
            invalid_phones = df[~df['phone'].apply(validate_phone)].index.tolist()
            if invalid_phones:
                log_message("WARNING", f"  {len(invalid_phones)} invalid phone numbers found")
        
        if is_valid:
            log_message("VALIDATE", "✅ Data validation passed")
        
        return is_valid
    
    def run(self, csv_file, table_name):
        """
        Run complete ETL pipeline
        
        Args:
            csv_file: Path to CSV file to load
            table_name: Name of target database table
        
        Returns:
            bool: True if successful, False otherwise
        """
        print("\n" + "=" * 60)
        print("🚀 STARTING ETL JOB")
        print("=" * 60 + "\n")
        
        start_time = datetime.now()
        success = False
        
        try:
            # Step 1: Extract
            df = self.extract(csv_file)
            
            # Step 2: Transform
            df = self.transform(df)
            
            # Step 3: Validate
            if not self.validate(df):
                log_message("ERROR", "Validation failed. Aborting ETL job.")
                return False
            
            # Step 4: Connect to database
            self.connect()
            
            # Step 5: Load
            self.load(df, table_name)
            
            success = True
            
        except Exception as e:
            log_message("ERROR", f"ETL JOB FAILED: {e}")
            
        finally:
            # Clean up
            if self.connection:
                self.connection.close()
                log_message("CONNECT", "Database connection closed")
        
        # Print summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ ETL JOB COMPLETED SUCCESSFULLY")
        else:
            print("❌ ETL JOB FAILED")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print("=" * 60 + "\n")
        
        return success


# Example usage
if __name__ == "__main__":
    print("ETL Job module loaded successfully!")
    print("To run an ETL job:")
    print("  etl = ETLJob()")
    print("  etl.run('data/sample_data.csv', 'students')")
