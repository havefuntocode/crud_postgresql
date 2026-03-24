# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
import psycopg2
import psycopg2.extras
import os

mcp = FastMCP("crud-postgresql")

DB_CONFIG = {
    "host":     os.getenv("host"),
    "user":     os.getenv("user"),
    "password": os.getenv("password"),
    "database": os.getenv("database"),
    "port":     int(os.getenv("port", "5432")),
    "options":  "-c client_encoding=UTF8"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ---------------------------------------------------------------------------
# SELECT
# ---------------------------------------------------------------------------

@mcp.tool()
def get_employees(department: str = "") -> list[dict]:
    """
    Gibt alle Mitarbeiter zurueck.
    Optional: Filtere nach Abteilung (department), z.B. 'Engineering'.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if department:
            cursor.execute(
                "SELECT * FROM employees WHERE department = %s ORDER BY id",
                (department,)
            )
        else:
            cursor.execute("SELECT * FROM employees ORDER BY id")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        if conn:
            conn.close()


@mcp.tool()
def get_departments() -> list[str]:
    """Gibt alle vorhandenen Abteilungen zurueck."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT department FROM employees ORDER BY department"
        )
        return [row[0] for row in cursor.fetchall()]
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# INSERT
# ---------------------------------------------------------------------------

@mcp.tool()
def add_employee(
    first_name: str,
    last_name: str,
    department: str,
    salary: float,
    hire_date: str
) -> dict:
    """
    Fuegt einen neuen Mitarbeiter hinzu.
    hire_date im Format YYYY-MM-DD, z.B. '2024-01-15'.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
            INSERT INTO employees (first_name, last_name, department, salary, hire_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
            """,
            (first_name, last_name, department, salary, hire_date)
        )
        conn.commit()
        return dict(cursor.fetchone())
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------

@mcp.tool()
def update_employee(
    employee_id: int,
    first_name: str = None,
    last_name: str = None,
    department: str = None,
    salary: float = None,
    hire_date: str = None
) -> dict:
    """
    Aktualisiert einen Mitarbeiter anhand seiner ID.
    Nur die uebergebenen Felder werden geaendert.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        fields = []
        values = []
        if first_name is not None:
            fields.append("first_name = %s")
            values.append(first_name)
        if last_name is not None:
            fields.append("last_name = %s")
            values.append(last_name)
        if department is not None:
            fields.append("department = %s")
            values.append(department)
        if salary is not None:
            fields.append("salary = %s")
            values.append(salary)
        if hire_date is not None:
            fields.append("hire_date = %s")
            values.append(hire_date)

        if not fields:
            return {"error": "Keine Felder zum Aktualisieren angegeben."}

        values.append(employee_id)
        cursor.execute(
            f"UPDATE employees SET {', '.join(fields)} WHERE id = %s RETURNING *",
            values
        )
        conn.commit()
        row = cursor.fetchone()
        if row is None:
            return {"error": f"Kein Mitarbeiter mit ID {employee_id} gefunden."}
        return dict(row)
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

@mcp.tool()
def delete_employee(employee_id: int) -> dict:
    """
    Loescht einen Mitarbeiter anhand seiner ID.
    Gibt den geloeschten Datensatz zurueck.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "DELETE FROM employees WHERE id = %s RETURNING *",
            (employee_id,)
        )
        conn.commit()
        row = cursor.fetchone()
        if row is None:
            return {"error": f"Kein Mitarbeiter mit ID {employee_id} gefunden."}
        return {"deleted": dict(row)}
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
