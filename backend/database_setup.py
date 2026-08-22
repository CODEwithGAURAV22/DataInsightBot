import sqlite3
import os

# Get the folder where this Python file is located
base_path = os.path.dirname(os.path.abspath(__file__))

# Existing database folder
database_folder = os.path.join(base_path, "database")

# Database file path
database_path = os.path.join(database_folder, "company.db")

# Connect to database
connection = sqlite3.connect(database_path)

cursor = connection.cursor()

# -------------------------
# Departments Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    manager_name TEXT
)
""")

# -------------------------
# Employees Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    department_id INTEGER,
    salary REAL,
    joining_date TEXT,
    location TEXT,
    performance_score REAL,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
)
""")

# -------------------------
# Projects Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    department_id INTEGER,
    budget REAL,
    revenue REAL,
    status TEXT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
)
""")

# -------------------------
# Sales Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    sale_date TEXT,
    quantity INTEGER,
    price REAL,
    revenue REAL,
    profit REAL,
    location TEXT
)
""")

# Save changes
connection.commit()

# Close database
connection.close()

print("Database created successfully!")
print("Location:", database_path)