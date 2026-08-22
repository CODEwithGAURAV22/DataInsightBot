DATABASE_SCHEMA = """

DATABASE: company.db
DATABASE TYPE: SQLite

TABLE: departments

Columns:
- department_id INTEGER PRIMARY KEY
- department_name TEXT
- manager_name TEXT


TABLE: employees

Columns:
- employee_id INTEGER PRIMARY KEY
- employee_name TEXT
- department_id INTEGER
- salary REAL
- joining_date TEXT
- location TEXT
- performance_score REAL

Relationship:
employees.department_id → departments.department_id


TABLE: projects

Columns:
- project_id INTEGER PRIMARY KEY
- project_name TEXT
- department_id INTEGER
- budget REAL
- revenue REAL
- status TEXT

Relationship:
projects.department_id → departments.department_id


TABLE: sales

Columns:
- sale_id INTEGER PRIMARY KEY
- product TEXT
- sale_date TEXT
- quantity INTEGER
- price REAL
- revenue REAL
- profit REAL
- location TEXT

"""