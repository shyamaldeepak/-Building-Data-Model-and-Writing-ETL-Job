-- ============================================
-- 01_CREATE_DATABASE.SQL
-- Step 1: Create the database
-- ============================================
-- This script creates the main database for the student management system

-- Drop database if it exists (be careful with this!)
-- DROP DATABASE IF EXISTS student_management;

-- Create the database
CREATE DATABASE student_management;

-- Connect to the database
\c student_management

-- Verify database creation
SELECT datname FROM pg_database WHERE datname = 'student_management';
