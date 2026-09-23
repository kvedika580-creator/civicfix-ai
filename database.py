import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path("data/civicfix.db")


def get_connection():
    """Create a connection to the CivicFix SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the complaints table if it does not already exist."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                issue TEXT NOT NULL,
                category TEXT,
                severity TEXT,
                summary TEXT,
                department TEXT,
                complaint TEXT,
                location TEXT,
                status TEXT DEFAULT 'Submitted',
                created_at TEXT
            )
            """
        )
        connection.commit()
        connection.close()
    except sqlite3.DatabaseError:
        if DB_PATH.exists():
            DB_PATH.unlink()
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                issue TEXT NOT NULL,
                category TEXT,
                severity TEXT,
                summary TEXT,
                department TEXT,
                complaint TEXT,
                location TEXT,
                status TEXT DEFAULT 'Submitted',
                created_at TEXT
            )
            """
        )
        connection.commit()
        connection.close()


def create_ticket(data):
    """Store a new civic complaint in the database."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO complaints (
            ticket_id,
            name,
            issue,
            category,
            severity,
            summary,
            department,
            complaint,
            location,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["ticket_id"],
            data["name"],
            data["issue"],
            data["category"],
            data["severity"],
            data["summary"],
            data["department"],
            data["complaint"],
            data["location"],
            "Submitted",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    connection.commit()
    connection.close()


def get_all_complaints():
    """Return all complaints for the dashboard."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            ticket_id,
            name,
            issue,
            category,
            severity,
            summary,
            department,
            complaint,
            location,
            status,
            created_at
        FROM complaints
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    columns = [
        "id",
        "ticket_id",
        "name",
        "issue",
        "category",
        "severity",
        "summary",
        "department",
        "complaint",
        "location",
        "status",
        "created_at",
    ]

    connection.close()

    return rows, columns
