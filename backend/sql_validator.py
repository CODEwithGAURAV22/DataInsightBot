def validate_sql(sql_query):
    """
    Validate SQL query before executing it.
    Only SELECT queries are allowed.
    """

    # Remove unnecessary spaces
    query = sql_query.strip().lower()

    # Query must start with SELECT
    if not query.startswith("select"):
        return False, "Only SELECT queries are allowed."

    # Dangerous SQL commands
    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "pragma"
    ]

    # Check for forbidden commands
    for keyword in forbidden_keywords:

        if keyword in query:
            return False, f"Forbidden SQL operation detected: {keyword}"

    return True, "SQL query is safe."


# -------------------------
# Test the validator
# -------------------------

if __name__ == "__main__":

    # Safe query
    safe_query = """
    SELECT employee_name, salary
    FROM employees
    WHERE salary > 60000;
    """

    valid, message = validate_sql(safe_query)

    print("Safe Query:")
    print(valid, "-", message)


    # Dangerous query
    dangerous_query = """
    DELETE FROM employees;
    """

    valid, message = validate_sql(dangerous_query)

    print("\nDangerous Query:")
    print(valid, "-", message)