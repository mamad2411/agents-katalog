---
name: mcp-db-connector
description: "MCP Database Connector — querying, schema inspection, and data analysis using live database connections. Use when querying or inspecting databases via MCP."
---

# MCP Database Connector (MCP DB Connector)

## Overview

MCP DB Connector is a skill that enables querying, schema inspection, and data analysis by establishing live connections to databases over the MCP protocol. By default, it operates in read-only mode; write operations are only possible when explicitly authorized and enabled. Using connection pool management, multiple concurrent database connections are handled efficiently.

**Core principle:** READ-ONLY BY DEFAULT — DATA MODIFICATION REQUIRES EXPLICIT AUTHORIZATION.

## The Iron Law

```
NO QUERY MAY MODIFY DATA (INSERT/UPDATE/DELETE/DDL) IN A PRODUCTION DATABASE. WRITE PERMISSIONS ARE VALID ONLY WHEN EXPLICITLY AND CONSCIOUSLY ENABLED.
```

## When to Use

**Use this when:**
- You need to inspect a database schema (tables, indexes, foreign keys).
- You need to execute SELECT queries and analyze live data results.
- You need to run data quality or consistency checks.
- You need to extract query results for reporting or data analysis.

**Use this ESPECIALLY when:**
- You think, "Let me quickly check a table structure" — it is faster than manual connection setups.
- You need to verify database state during a debugging session.
- You need to perform verification post-database migrations in a CI/CD pipeline.

**Don't skip when:**
- You intend to perform a write operation to the database (remember to enable write permissions first).
- Connection parameters (host, port, credentials) are not fully configured.
- You lack access or are unauthorized to connect to the database.

## Phase 1: Connection Configuration and Verification

**BEFORE proceeding:**

1. **Gather connection credentials** — host, port, database name, username, password, and role.
2. **Identify database type** — PostgreSQL, MySQL, SQLite, MSSQL, Oracle, etc.
3. **Check SSL/TLS requirements** — is an encrypted connection mandatory?
4. **Test the connection** — verify that the connection can be established successfully.

```
mcp-db-connector connect --type postgresql --host db.example.com --port 5432 --db production --user analyzer --role readonly
mcp-db-connector test --connection-id conn-123
```

## Phase 2: Schema Inspection

**BEFORE proceeding:**

1. **List database objects** — tables, views, indexes, and stored functions.
2. **Inspect table structure** — columns, data types, constraints, and default values.
3. **Explore relationships** — foreign keys and referential integrity constraints.
4. **Audit index configuration** — primary keys, unique indexes, and performance indexes.

```
mcp-db-connector schema tables --connection-id conn-123
mcp-db-connector schema describe --connection-id conn-123 --table users
mcp-db-connector schema indexes --connection-id conn-123 --table orders
mcp-db-connector schema foreign-keys --connection-id conn-123
```

## Phase 3: Query Execution and Result Analysis

**BEFORE proceeding:**

1. **Verify read-only mode** — if the connection has no write permissions, query execution is safe.
2. **Write and test queries** — formulate the query, execute it, and inspect the returned data.
3. **Apply query limits** — always use LIMIT clauses or pagination when querying large tables.
4. **Format results** — output the query results in JSON, tabular, or CSV format.

```
mcp-db-connector query --connection-id conn-123 --sql "SELECT * FROM users WHERE status = 'active' LIMIT 100"
mcp-db-connector query --connection-id conn-123 --sql "SELECT COUNT(*) FROM orders WHERE created_at > NOW() - INTERVAL '7 days'" --format json
```

## Phase 4: Write Permission Management (Only If Necessary)

**BEFORE proceeding:**

1. **Validate the write requirement** — is an INSERT/UPDATE/DELETE/DDL statement strictly necessary?
2. **Obtain approval** — secure written confirmation from your human partner or authorized system.
3. **Enable in restricted scope** — grant write privileges only to specific tables or columns.
4. **Revoke immediately post-execution** — disable write access immediately after completing the operation.

```
mcp-db-connector enable-write --connection-id conn-123 --scope "UPDATE orders SET status WHERE id IN (...) ONLY" --reason "ETL bug fix - approved by #ticket-456"
mcp-db-connector disable-write --connection-id conn-123  # close immediately
```

## Phase 5: Final Verification

Before marking complete:

- [ ] Has the connection been successfully established and tested?
- [ ] Is the schema inspection complete?
- [ ] Have the queries executed as expected?
- [ ] Has read-only mode been maintained? (if write access was not required)
- [ ] If write access was enabled, has it been disabled?
- [ ] Has the connection pool been properly managed? (no dangling connections)
- [ ] Are sensitive data points (passwords, tokens, PII) excluded from log outputs?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "It's just a single UPDATE, nobody will notice."
- "Operating in read-only is too restrictive, I'll just enable write permissions directly."
- "This table is large, but there's no need to use a LIMIT clause; it probably has few records."
- "I don't need to test the connection, it should work fine."
- "I can write the password as plain text in the query, nobody will see it."

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why has the database state changed?" — You opened write permissions without proper controls.
- "Why is this query so slow?" — You skipped adding LIMIT clauses or ran queries against unindexed columns.
- "Why is the connection failing?" — You misconfigured connection parameters.
- "Where did this password leak from?" — You exposed credentials in log outputs.
- "Where is the query output?" — You failed to format or capture the query result.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's just a quick UPDATE, it won't break anything." | Rogue writes bypass validation logic, compromise data integrity, and create audit risks. |
| "LIMIT is unnecessary, the table is small." | Fetching unbounded result sets exhausts memory buffers and introduces network lag. |
| "Testing the connection is a waste of time." | Troubleshooting queries on a bad connection takes far longer than a simple test. |
| "I can write the password in the query string temporarily." | Query logs are saved persistently; plaintext passwords in queries will leak credentials. |
| "I'll close the write permissions later when I'm done." | Leaving write access open invites accidental modifications and introduces security risks. |

## Related Skills

- **mcp-api-tester** — Use the DB Connector to verify database state during API testing.
- **mcp-infra-scanner** — Use to verify database configurations during infrastructure scans.
- **spec-first-development** — Inspect schema structures to verify database matches API specifications.

## Self-Review

After completing this process:

1. **Security Check:** Was read-only mode preserved? If write mode was enabled, was it disabled immediately after use?
2. **Schema Audit:** Have all required tables, columns, indexes, and relationships been documented?
3. **Query Quality:** Have all queries executed successfully with appropriate LIMIT parameters?
4. **Resource Management:** Are all database connections closed and returned to the pool?
