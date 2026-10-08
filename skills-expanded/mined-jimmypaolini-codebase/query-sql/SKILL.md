---
name: query-sql

description: Toolkit for interactively querying and exploring the local PostgreSQL database schema and data using the local psql client. Use when asked to write a SQL query, explore database schemas, inspect table structures, or execute local database queries. Relies on workspace default environment variables.
---

# PostgreSQL SQL Query & Exploration

## When to Use This Skill

Use this skill when you need to:

- Explore the schema of the local PostgreSQL database.
- Inspect the structure of specific tables, views, or indexes.
- Draft and execute SQL queries to fetch or analyze data.
- Debug database state or verify data integrity locally.

## Prerequisites

- The local PostgreSQL container must be running. Use `nx run codebase:postgres-container:up` if needed.
- `psql` (PostgreSQL client) must be installed locally.
- The `.env` file at the workspace root must contain the default PostgreSQL connection variables (`POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_DB`, `POSTGRES_PASSWORD`).

## Step-by-Step Workflows

### 1. Schema Exploration

To explore the database quickly, use `psql` meta-commands passed via the `-c` flag. Use `set -a; source .env; set +a;` to ensure environment variables are automatically exported.

- **List all tables:**

  ```bash
  set -a; source .env; set +a; PGPASSWORD=$POSTGRES_PASSWORD psql -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres} -c "\dt"

  ```

- **Describe a specific table:**

  ```bash
  set -a; source .env; set +a; PGPASSWORD=$POSTGRES_PASSWORD psql -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres} -c "\d+ table_name"

  ```

- **List all schemas:**

  ```bash
  set -a; source .env; set +a; PGPASSWORD=$POSTGRES_PASSWORD psql -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres} -c "\dn"

  ```

### 2. Query Execution

**CRITICAL:** NEVER execute multiline or complex queries using the inline `-c` flag, as this often leads to shell escaping errors. Always use `notepads/notepad.sql` as a scratchpad.

1. **Write the query to the scratchpad:**
   Use your file editing tools to write your SQL query into `notepads/notepad.sql`.

2. **Execute the query:**
   Run the file using the `-f` flag in the terminal:

   ```bash
   set -a; source .env; set +a; PGPASSWORD=$POSTGRES_PASSWORD psql -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres} -f notepads/notepad.sql
   ```

## Good SQL Practices

- **Always use `LIMIT`:** When running exploratory `SELECT` queries, always append a limit (e.g., `LIMIT 10`) to avoid flooding the terminal output.
- **Use Expanded Display (`\x`):** For queries returning many columns, prepend `\x on;` to your query in `notepads/notepad.sql` to render the output in a readable key-value format (similar to MySQL's `\G`).

  \_Example `notepads/notepad.sql`:*

  ```sql
  \x on;
  SELECT * FROM users LIMIT 1;

  ```

- **Formatting:** Keep SQL clean and well-indented in the scratchpad for easy review and modification.
