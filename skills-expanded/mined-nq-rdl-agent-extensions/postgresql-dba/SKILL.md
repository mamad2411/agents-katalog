---
name: postgresql-dba
description: 'Use when administering PostgreSQL: schema design, query optimization, backup/restore, tuning, or security. Inspect the database with an available client or MCP tool.'
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/postgresql-dba.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Administer

Use an available PostgreSQL client or MCP tool to inspect the target database directly. Establish the database, requested operation, and allowed mutations before execution. Inspection is read-only by default: writing a migration file does not apply it, and DDL, DML, or maintenance runs against a database only when the user authorized that change for that database. Base schema, tuning, backup, and security recommendations on observed state and report verification.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
