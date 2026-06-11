"""
demo_etl.py - Standalone demo of the ETL pipeline WITHOUT database
This demonstrates all the ETL concepts without needing PostgreSQL
"""

import pandas as pd
from datetime import datetime
import os

class DemoETL:
    """Demo ETL Job that works without database"""
    
    def __init__(self):
        self.extracted_data = None
        self.transformed_data = None
        
    def extract(self, csv_file):
        """EXTRACT: Read data from CSV file"""
        try:
            print(f"[EXTRACT] Reading data from {csv_file}...")
            df = pd.read_csv(csv_file)
            print(f"[EXTRACT] ✅ Successfully loaded {len(df)} rows")
            print(f"[EXTRACT] Columns: {', '.join(df.columns)}\n")
            self.extracted_data = df
            return df
        except Exception as e:
            print(f"[ERROR] Extract failed: {e}")
            raise
    
    def transform(self, df):
        """TRANSFORM: Clean and prepare data"""
        print("[TRANSFORM] Starting data transformation...")
        print("─" * 60)
        
        try:
            # Remove duplicates
            initial_count = len(df)
            df = df.drop_duplicates()
            duplicates_removed = initial_count - len(df)
            if duplicates_removed > 0:
                print(f"  ✓ Removed {duplicates_removed} duplicate rows")
            
            # Fill missing values
            missing_before = df.isnull().sum().sum()
            df = df.fillna('Unknown')
            if missing_before > 0:
                print(f"  ✓ Filled {missing_before} missing values")
            
            # Convert email to lowercase
            if 'email' in df.columns:
                df['email'] = df['email'].str.lower()
                print("  ✓ Converted emails to lowercase")
            
            # Convert names to title case
            if 'first_name' in df.columns:
                df['first_name'] = df['first_name'].str.title()
            if 'last_name' in df.columns:
                df['last_name'] = df['last_name'].str.title()
            if 'first_name' in df.columns or 'last_name' in df.columns:
                print("  ✓ Converted names to title case")
            
            # Clean phone numbers
            if 'phone' in df.columns:
                df['phone'] = df['phone'].astype(str).str.replace(' ', '')
                print("  ✓ Cleaned phone numbers")
            
            print(f"[TRANSFORM] ✅ Transformation complete. {len(df)} rows ready\n")
            self.transformed_data = df
            return df
            
        except Exception as e:
            print(f"[ERROR] Transform failed: {e}")
            raise
    
    def load(self, df, output_file='data/transformed_data.csv'):
        """LOAD: Save data to CSV (simulating database load)"""
        print(f"[LOAD] Loading data to {output_file}...")
        
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            df.to_csv(output_file, index=False)
            print(f"[LOAD] ✅ Successfully saved {len(df)} rows to {output_file}\n")
            return True
        except Exception as e:
            print(f"[ERROR] Load failed: {e}")
            raise
    
    def validate(self, df):
        """Validate data before loading"""
        print("[VALIDATE] Validating data...")
        
        is_valid = True
        
        # Check required columns
        required = ['first_name', 'last_name']
        for col in required:
            if col not in df.columns:
                print(f"  ❌ Missing required column: {col}")
                is_valid = False
        
        # Validate emails
        if 'email' in df.columns:
            valid_emails = df['email'].str.contains('@', na=False).sum()
            invalid_count = len(df) - valid_emails
            if invalid_count > 0:
                print(f"  ⚠️  {invalid_count} invalid emails found")
        
        if is_valid:
            print("[VALIDATE] ✅ Data validation passed\n")
        
        return is_valid
    
    def run(self, csv_file, output_file='data/transformed_data.csv'):
        """Run complete ETL pipeline"""
        print("\n" + "=" * 60)
        print("🚀 DEMO ETL JOB - STANDALONE (NO DATABASE REQUIRED)")
        print("=" * 60 + "\n")
        
        start_time = datetime.now()
        success = False
        
        try:
            # Step 1: Extract
            df = self.extract(csv_file)
            print(df.head())
            
            # Step 2: Transform
            df = self.transform(df)
            print("Transformed Data Sample:")
            print(df.head())
            
            # Step 3: Validate
            if not self.validate(df):
                print("[ERROR] Validation failed. Aborting ETL job.\n")
                return False
            
            # Step 4: Load
            self.load(df, output_file)
            
            success = True
            
        except Exception as e:
            print(f"❌ ETL JOB FAILED: {e}\n")
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("=" * 60)
        if success:
            print("✅ ETL JOB COMPLETED SUCCESSFULLY")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            print(f"📊 Output file: {output_file}")
        else:
            print("❌ ETL JOB FAILED")
        print("=" * 60 + "\n")
        
        return success


class DataAnalyzer:
    """Analyze data from CSV files (no database needed)"""
    
    @staticmethod
    def load_and_analyze(csv_file):
        """Load CSV and show analysis"""
        try:
            df = pd.read_csv(csv_file)
            
            print("\n" + "=" * 60)
            print("📊 DATA ANALYSIS REPORT")
            print("=" * 60 + "\n")
            
            print(f"📈 Total Records: {len(df)}")
            print(f"📋 Total Columns: {len(df.columns)}")
            print(f"\nColumn Summary:")
            print("-" * 60)
            for col in df.columns:
                print(f"  • {col}: {df[col].dtype}")
            
            print(f"\n📄 Data Preview (first 5 rows):")
            print("-" * 60)
            print(df.head().to_string(index=False))
            
            print(f"\n📊 Statistics:")
            print("-" * 60)
            if 'date_of_birth' in df.columns:
                print(f"  • Total unique values in each column:")
                for col in df.columns:
                    unique = df[col].nunique()
                    print(f"    - {col}: {unique} unique values")
            
            print("\n" + "=" * 60 + "\n")
            
            return df
            
        except Exception as e:
            print(f"Error analyzing data: {e}")
            return None


# Run the demo
if __name__ == "__main__":
    print("\n🎓 DATA ENGINEERING DEMO - ETL Pipeline")
    print("This demo works WITHOUT requiring PostgreSQL!\n")
    
    # Check if sample data exists
    if os.path.exists('data/sample_students.csv'):
        etl = DemoETL()
        etl.run('data/sample_students.csv', 'data/transformed_data.csv')
        
        # Analyze transformed data
        print("\n📊 Analyzing transformed data...")
        analyzer = DataAnalyzer()
        analyzer.load_and_analyze('data/transformed_data.csv')
        
        print("\n✅ DEMO COMPLETE!")
        print("📁 Check 'data/transformed_data.csv' for the transformed data")
    else:
        print("❌ Sample data not found at 'data/sample_students.csv'")
        print("Please ensure the project structure is correct.")
