---
name: sqlite-db-query
description: Execute read-only SQL queries on a local SQLite database file
---

# SQLite Database Query

Execute read-only SQL queries on a local SQLite database file

## When to Use

- User wants to sqlite query
- User wants to db query
- Keywords: database, sqlite, sql, query

## Required Parameters

- **db_path** (string): Path to SQLite database file
- **query** (string): SQL SELECT query

## Output

- **rows** (array): Query result rows
- **columns** (array): Column names
- **row_count** (number): Number of rows returned

## Security

- Sandbox level: standard
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `check_ro` -> 7 steps -> Exit: `ret_ok`, `ret_readonly`, `ret_fail`
