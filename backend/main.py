from gemini_service import generate_sql, explain_result
from sql_validator import validate_sql
from database_query import execute_query


def ask_database(question):

    # Step 1: Generate SQL
    print("\nGenerating SQL...")

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    # Step 2: Validate SQL
    print("\nValidating SQL...")

    is_valid, message = validate_sql(sql)

    if not is_valid:
        return f"SQL validation failed: {message}"

    print(f"SQL validation successful: {message}")

    # Step 3: Execute SQL
    print("\nExecuting SQL...")

    result = execute_query(sql)

    # Check for database error
    if "error" in result:
        return f"Database error: {result['error']}"

    columns = result["columns"]
    rows = result["rows"]

    print("\nDatabase Result:")
    print("Columns:", columns)

    for row in rows:
        print(row)

    # Step 4: Generate business explanation
    print("\nGenerating business explanation...")

    explanation = explain_result(
        question,
        sql,
        columns,
        rows
    )

    return explanation


# =========================
# Main Program
# =========================

if __name__ == "__main__":

    print("=" * 60)
    print("DataInsightBot - AI Powered Business Analyst")
    print("=" * 60)

    question = input("\nAsk your business question: ")

    answer = ask_database(question)

    print("\n" + "=" * 60)
    print("Business Answer")
    print("=" * 60)

    print(answer)