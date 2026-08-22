import sqlite3
import os

# Database path
base_path = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_path, "database", "company.db")

# Connect to database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# =========================
# Departments
# =========================

departments = [
    (1, "IT", "Rahul Sharma"),
    (2, "HR", "Priya Singh"),
    (3, "Finance", "Amit Verma"),
    (4, "Sales", "Neha Gupta"),
    (5, "Marketing", "Rohan Mehta")
]

cursor.executemany("""
INSERT INTO departments
(department_id, department_name, manager_name)
VALUES (?, ?, ?)
""", departments)


# =========================
# Employees
# =========================

employees = [
    (1, "Aarav Kumar", 1, 65000, "2023-01-15", "Delhi", 8.5),
    (2, "Ananya Singh", 1, 72000, "2022-06-20", "Mumbai", 9.1),
    (3, "Riya Sharma", 2, 58000, "2024-02-10", "Delhi", 8.2),
    (4, "Karan Verma", 2, 62000, "2023-08-05", "Bangalore", 7.9),
    (5, "Arjun Mehta", 3, 75000, "2021-11-12", "Delhi", 9.0),
    (6, "Sneha Gupta", 3, 68000, "2022-03-18", "Mumbai", 8.7),
    (7, "Vivek Patel", 4, 55000, "2024-01-22", "Delhi", 8.0),
    (8, "Simran Kaur", 4, 60000, "2023-05-14", "Mumbai", 8.6),
    (9, "Aditya Rao", 5, 70000, "2022-09-30", "Bangalore", 8.9),
    (10, "Meera Nair", 5, 64000, "2023-12-01", "Delhi", 9.2)
]

cursor.executemany("""
INSERT INTO employees
(employee_id, employee_name, department_id, salary,
joining_date, location, performance_score)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", employees)


# =========================
# Projects
# =========================

projects = [
    (1, "Employee Management System", 1, 500000, 650000, "Completed"),
    (2, "AI Chatbot", 1, 800000, 950000, "In Progress"),
    (3, "Recruitment Portal", 2, 300000, 420000, "Completed"),
    (4, "Financial Dashboard", 3, 600000, 780000, "Completed"),
    (5, "Sales Analytics", 4, 450000, 620000, "In Progress"),
    (6, "Marketing Campaign", 5, 350000, 500000, "Completed")
]

cursor.executemany("""
INSERT INTO projects
(project_id, project_name, department_id,
budget, revenue, status)
VALUES (?, ?, ?, ?, ?, ?)
""", projects)


# =========================
# Sales
# =========================

sales = [
    (1, "Laptop", "2026-07-01", 10, 60000, 600000, 120000, "Delhi"),
    (2, "Laptop", "2026-07-05", 8, 60000, 480000, 96000, "Mumbai"),
    (3, "Phone", "2026-07-08", 20, 30000, 600000, 90000, "Delhi"),
    (4, "Phone", "2026-07-12", 15, 30000, 450000, 67500, "Bangalore"),
    (5, "Tablet", "2026-07-15", 12, 25000, 300000, 60000, "Delhi"),
    (6, "Laptop", "2026-08-01", 6, 60000, 360000, 72000, "Delhi"),
    (7, "Phone", "2026-08-03", 10, 30000, 300000, 45000, "Mumbai"),
    (8, "Tablet", "2026-08-05", 8, 25000, 200000, 40000, "Delhi"),
    (9, "Laptop", "2026-08-08", 12, 60000, 720000, 144000, "Bangalore"),
    (10, "Phone", "2026-08-10", 18, 30000, 540000, 81000, "Delhi")
]

cursor.executemany("""
INSERT INTO sales
(sale_id, product, sale_date, quantity,
price, revenue, profit, location)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", sales)


# Save everything
connection.commit()

# Close database
connection.close()

print("Company data inserted successfully!")