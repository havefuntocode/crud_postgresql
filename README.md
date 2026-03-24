# crud_postgresql
MCP-Server for CRUD Operations on a PostgreSQL Database


# CRUD PostgreSQL MCP Server

Ein FastMCP-Server mit allen 4 CRUD-Operationen fuer eine PostgreSQL-Datenbank.

## Voraussetzungen

- Python 3.11+
- PostgreSQL
- Claude Desktop

## Installation

```bash
pip install mcp psycopg2-binary
```

## Datenbankstruktur

```sql
CREATE TABLE employees (
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name  VARCHAR(100),
    department VARCHAR(100),
    salary     NUMERIC(10,2),
    hire_date  DATE
);
```

## Claude Desktop Konfiguration

In `claude_desktop_config.json` eintragen:

```json
"crud-postgresql": {
  "command": "c:/Users/<user>/AppData/Local/Programs/Python/Python311/python.exe",
  "args": ["c:/deploy/mcp/crud_postgresql/server.py"],
  "env": {
    "host":     "localhost",
    "user":     "postgres",
    "password": "dein-passwort",
    "database": "mitarbeiter_db",
    "port":     "5432"
  }
}
```

## Verfuegbare Tools

| Tool | Beschreibung |
|------|-------------|
| `get_employees` | Alle Mitarbeiter abrufen, optional nach Abteilung filtern |
| `get_departments` | Alle Abteilungen abrufen |
| `add_employee` | Neuen Mitarbeiter hinzufuegen |
| `update_employee` | Mitarbeiter aktualisieren (nur geaenderte Felder) |
| `delete_employee` | Mitarbeiter loeschen |

## Wichtige Hinweise fuer Windows

In `postgresql.conf` muss folgendes gesetzt sein:

```
lc_messages = 'en_US.UTF-8'
```

Sonst kommt es zu einem `UnicodeDecodeError` beim Verbindungsaufbau mit psycopg2.