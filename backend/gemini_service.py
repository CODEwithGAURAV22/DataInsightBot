import os

from dotenv import load_dotenv
from google import genai

from backend.schema import DATABASE_SCHEMA


# =========================
# Load environment variables
# =========================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# =========================
# Create Gemini client
# =========================

client = genai.Client(api_key=api_key)


# =========================
# Generate SQL
# =========================

def generate_sql(question):

    prompt = f"""
You are an expert SQLite SQL developer.

Your job is to convert the user's natural language
business question into a valid SQLite SQL query.

DATABASE SCHEMA:

{DATABASE_SCHEMA}

IMPORTANT RULES:

1. Return ONLY the SQL query.
2. Do NOT use markdown.
3. Do NOT use ```sql.
4. Only generate SELECT queries.
5. Never generate INSERT, UPDATE, DELETE, DROP,
   ALTER, CREATE, REPLACE or TRUNCATE queries.
6. Use only tables and columns present in the schema.
7. Use valid SQLite syntax.
8. Use table aliases when useful.
9. If a JOIN is required, use the relationships
   provided in the schema.
10. When calculating AVG, SUM, COUNT, MAX or MIN,
    give the calculated column a clear alias.
11. Return all columns necessary to properly answer
    the user's question.

USER QUESTION:

{question}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    sql = response.text.strip()

    # Remove markdown code fences
    if sql.startswith("```sql"):
        sql = sql[6:]

    elif sql.startswith("```"):
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()


# =========================
# Explain Database Result
# =========================

def explain_result(question, sql, columns, rows):

    prompt = f"""
You are an AI Business Analyst.

Answer the user's business question using
the database result provided below.

USER QUESTION:
{question}

SQL QUERY:
{sql}

COLUMNS:
{columns}

RESULTS:
{rows}

INSTRUCTIONS:

1. Directly answer the user's question.
2. Use simple and clear English.
3. Mention important numbers from the result.
4. Keep the answer concise.
5. Do not explain the SQL query.
6. Do not mention that you are an AI.
7. If there are multiple results, summarize the
   important findings.
8. Do not make up information that is not present
   in the database result.
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text.strip()


# =========================
# Test Gemini
# =========================

if __name__ == "__main__":

    question = "Which department has the highest average salary?"

    print("=" * 50)
    print("Testing Gemini")
    print("=" * 50)

    print("\nUser Question:")
    print(question)

    print("\nGenerating SQL...")

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    print("\nGemini connection successful!")