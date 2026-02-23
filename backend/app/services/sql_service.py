from sqlalchemy import text
from sqlalchemy.orm import Session

FORBIDDEN_KEYWORDS = [
    "insert", "update", "delete", "drop",
    "alter", "truncate", "create"
]

FORBIDDEN_PATTERNS = [
    "information_schema",
    "pg_catalog",
    "pg_",
    "pg_sleep",
    "current_user",
    "version()"
]

MAX_LIMIT = 100


def enforce_limit(query: str) -> str:
    lowered = query.lower()
    if "limit" not in lowered:
        return query.rstrip(";") + f" LIMIT {MAX_LIMIT};"
    return query


def execute_readonly_query(db: Session, query: str):
    lowered = query.strip().lower()

    # Must start with SELECT
    if not lowered.startswith("select"):
        return {"error": "Only SELECT queries are allowed."}

    # Block obvious destructive keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in lowered:
            return {"error": f"Keyword '{keyword}' not allowed."}

    # Block system schemas & risky functions
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in lowered:
            return {"error": f"Access to '{pattern}' is not allowed."}

    # Enforce row limit
    safe_query = enforce_limit(query)

    try:
        # Add timeout at DB level (3 seconds)
        db.execute(text("SET statement_timeout = 3000;"))

        result = db.execute(text(safe_query))
        rows = result.fetchall()
        columns = result.keys()

        return {
            "columns": list(columns),
            "rows": [list(row) for row in rows]
        }

    except Exception as e:
        return {"error": str(e)}