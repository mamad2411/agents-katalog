---
name: db-inspect
description: Inspect the ServerKit SQLite database — show tables, schemas, row counts, and run queries. Runs via WSL for local dev or SSH MCP for production. Use when debugging data issues or understanding the current database state.
disable-model-invocation: true
argument-hint: "[query or table-name]"
allowed-tools: Bash, mcp__ssh-mcp__exec
---

Inspect the ServerKit database. Argument: **$ARGUMENTS**

## Database Location

- **Local dev**: `backend/instance/serverkit.db` (relative to project root)
- **Production**: `/opt/serverkit/backend/instance/serverkit.db` (access via SSH MCP)

## If no argument or argument is "schema"

Show the full database schema:
```bash
sqlite3 backend/instance/serverkit.db '.schema'
```

And row counts for all tables:
```bash
sqlite3 backend/instance/serverkit.db "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
```
Then for each table, get the row count and present as a formatted table: Table Name | Row Count

## If argument is a table name

Show the schema and last 10 rows:
```bash
sqlite3 -header -column backend/instance/serverkit.db 'PRAGMA table_info(<table>);'
sqlite3 -header -column backend/instance/serverkit.db 'SELECT * FROM <table> ORDER BY id DESC LIMIT 10;'
```

## If argument looks like a SQL query

Run it directly:
```bash
sqlite3 -header -column backend/instance/serverkit.db '<query>'
```

## If argument is "production" or "prod"

Run the schema/overview commands on the production server via SSH MCP instead, using `/opt/serverkit/backend/instance/serverkit.db`.

## Safety

- NEVER run DELETE, DROP, UPDATE, or INSERT queries unless explicitly asked
- Always show the query before running it
- For production, double-check with the user before running any query
