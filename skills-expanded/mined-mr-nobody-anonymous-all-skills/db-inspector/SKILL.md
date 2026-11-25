---
name: db-inspector
description: Inspect database schemas and queries read-only by default and explain performance or safety risks.
category: development
aliases:
- database
- db
- query
- inspect
- mysql
- postgres
triggers:
- Check database schema
- Inspect this database
- Run a query
- Database structure
- Explain this query
keywords:
- database
- sql
- schema
- query
- inspect
- mysql
- postgres
- mongodb
dependencies:
- optional:database-client
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- db-inspector
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- database
- development
- inspector
- query
- schema
- sql
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Db Inspector

## Purpose
Inspect database schemas, run queries, and explain execution plans with read-only
defaults and clear risk indicators. The skill helps developers understand database
structure and optimize queries while preventing accidental modifications.

## When to Use
- Exploring database schema and structure
- Understanding table relationships
- Optimizing slow queries
- Verifying data in development
- Troubleshooting database issues

## When NOT to Use
- For production data modification (use explicit migration tools)
- Without proper database credentials
- For bulk operations without review

## Capabilities
- Schema inspection (tables, columns, indexes, constraints)
- Query execution with EXPLAIN
- Query performance analysis
- Data sampling (LIMIT results)
- Connection testing
- Index recommendations
- Safety risk assessment

## Inputs
- `action` (required) — one of: schema, query, explain, sample
- `connection` (required) — database connection string or alias
- `query` (required for query/explain) — SQL or query language
- `limit` (optional) — result limit (default: 100)

## Workflow
1. **Connect** — Establish database connection
2. **Validate** — Check connection and permissions
3. **Execute** — Run inspection or query
4. **Explain** — Provide execution plan if requested
5. **Assess** — Flag any safety concerns
6. **Present** — Format results clearly

## Tools
optional:database-client

## Examples
**User:** "Show me the users table schema"
**Response:**
```
Table: users
Columns:
- id (UUID, PK, NOT NULL)
- email (VARCHAR(255), UNIQUE, NOT NULL)
- created_at (TIMESTAMP, NOT NULL)
- updated_at (TIMESTAMP)
Indexes:
- idx_email (B-tree, UNIQUE)
- idx_created_at (B-tree)

Related tables: posts(user_id), sessions(user_id)
```

## Safety
- ALWAYS use read-only mode by default
- ALWAYS warn before any write operation
- Require explicit confirmation for DELETE, UPDATE, DROP
- Never expose connection credentials
- Limit result sets to prevent memory issues
- Log all queries for audit

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
