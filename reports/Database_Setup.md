# Database Setup Guide

## Project
ArchintX – AI-Powered User Behaviour Analytics

## Technology
- Database: MySQL
- Database Name: `user_behaviour_analytics`
- Storage Engine: InnoDB

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- MySQL Server
- Required Python libraries

### 2. Create Database and Tables
1. Open MySQL Workbench.
2. Open the project file `sql/03_create_tables.sql`.
3. Execute the complete SQL script.
4. Verify that all four tables are created:
   - users
   - courses
   - enrollments
   - user_activity

### 3. Load Cleaned Data

Activate the project virtual environment and run:

```bash
python scripts/03_load_mysql.py
```

Ensure MySQL connection credentials are correctly configured.

### 4. Verify Database

Execute the queries in:

`sql/01_sql_verification.sql`

Verify table records, primary keys, foreign keys and indexes.

### 5. Run Python Analytics

```bash
python scripts/04_python_analytics.py
```

### 6. Launch Dashboard

```bash
streamlit run app.py
```

## Database Relationships

- One user can have multiple enrollments.
- One course can have multiple enrollments.
- One user can generate multiple activity events.
- One course can be associated with multiple activity events.

## Data Integrity

Primary keys uniquely identify records, while foreign keys maintain relationships between users, courses, enrollments and activity records.
