---
name: mysql-prep-admin
description: Use when executing any SQL against LumiCore preparation MySQL data, especially requests to preview, update, correct, insert, delete, or otherwise modify records. Always require explicit user confirmation before executing any mutating SQL.
---

# Mysql Prep Admin

## Overview

Use this skill for any SQL against preparation MySQL data. Draft the exact SQL, explain the impact clearly, wait for explicit confirmation for mutating statements, then execute only the approved change.

## Safe Workflow

1. Identify the request and classify it as read-only or mutating.
2. If the request is ambiguous, ask one short clarification question before drafting SQL.
3. For read-only requests, query and return the result normally.
4. For mutating requests, prepare the exact SQL and a short impact summary.
5. Ask the user to confirm before running anything that changes data.
6. Execute only after an explicit confirmation such as `yes`, `confirm`, `go ahead`, `execute`, or `approved`.
7. Report the executed SQL, rows affected, and any database error.

## Confirmation Rules

- Treat `ok`, `looks good`, or similar acknowledgements as not confirmed unless the user clearly authorizes execution.
- If the user changes the request after previewing the SQL, rebuild the statement and ask again.
- Never run `UPDATE`, `DELETE`, `INSERT`, `ALTER`, `DROP`, or `TRUNCATE` without confirmation.
- Never execute a broad change without a narrow `WHERE` clause unless the user explicitly wants a full-table operation and confirms the risk.

## Execution Notes

- Use the local MySQL client (`mysql.exe`) with the configured LumiCore database connection available in the environment.
- Use the MCP tool `execute_sql` for any SQL the user gives.
- For mutating SQL, preview first with `confirm=false`, then run only after explicit confirmation with `confirm=true`.
- For read-only SQL, execute directly.
- Call the MCP server named `lumicore` through `mcporter`.
- For the canonical connection pattern and env var names, read `references/test2-integration.md` and the source file `C:\Users\hp\.openclaw\workspace\test2\db\mysql.js`.
- The `lumicore` MCP server loads `C:\Users\hp\.openclaw\workspace\test2\.env` automatically.
- Do not report a write as successful unless MySQL actually reports affected rows.
- Prefer the smallest safe change that solves the user's request.
- Mirror the user's language when asking for confirmation and when reporting results.
- If a query could affect multiple rows, say that clearly before asking for confirmation.

## Example Triggers

- `update the credat-date of ... to ...`
- `delete the zonne-prep where ...`
- `correct this preparation row`
- `change a delivery point in MySQL`
