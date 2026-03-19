import sqlite3
from src.config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_total_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM transactions")
    total = cursor.fetchone()["total"]

    conn.close()
    return total


def get_risk_distribution():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT risk_level, COUNT(*) as count
        FROM transactions
        GROUP BY risk_level
    """)

    result = cursor.fetchall()
    conn.close()

    return {row["risk_level"]: row["count"] for row in result}


def get_recent_transactions(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows

