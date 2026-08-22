import sqlite3
import os

# Database path
base_path = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_path, "database", "company.db")

# Connect to database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# -------------------------
# 1. Show all departments
# -------------------------

cursor.execute("""
SELECT * FROM departments
""")

departments = cursor.fetchall()

print("\n--- Departments ---")

for department in departments:
    print(department)


# -------------------------
# 2. Show all employees
# -------------------------

cursor.execute("""
SELECT * FROM employees
""")

employees = cursor.fetchall()

print("\n--- Employees ---")

for employee in employees:
    print(employee)


# -------------------------
# 3. Department with
#    highest average salary
# -------------------------

cursor.execute("""
SELECT
    d.department_name,
    AVG(e.salary) AS average_salary
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY average_salary DESC
LIMIT 1
""")

result = cursor.fetchone()

print("\n--- Highest Average Salary ---")
print(result)


# Close database
connection.close()