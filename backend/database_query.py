import sqlite3
import os


def execute_query(sql_query):
    """
    Execute a SQL query on the company database
    and return the results.
    """

    # Database path
    base_path = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(
        base_path,
        "database",
        "company.db"
    )

    # Connect to database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Execute query
        cursor.execute(sql_query)

        # Get column names
        columns = [
            description[0]
            for description in cursor.description
        ]

        # Get rows
        rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows
        }

    except Exception as error:

        return {
            "error": str(error)
        }

    finally:
        connection.close()


# Test the function
if __name__ == "__main__":

    query = """
    SELECT
        d.department_name,
        COUNT(e.employee_id) AS employee_count
    FROM employees e
    JOIN departments d
        ON e.department_id = d.department_id
    GROUP BY d.department_name
    ORDER BY employee_count DESC;
    """

    result = execute_query(query)

    print("\nColumns:")
    print(result["columns"])

    print("\nRows:")

    for row in result["rows"]:
        print(row)