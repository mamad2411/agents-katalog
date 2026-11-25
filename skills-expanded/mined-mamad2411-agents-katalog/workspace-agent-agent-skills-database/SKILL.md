---
description: Use for schema design, migrations, SQL, indexes, relations, multi-tenancy, and query performance. Separate suggestion from execution.
---

# Database mode

Support PostgreSQL, Neon, MySQL, and SQLite. Use `explore_database` first.

Separate **SQL suggestion** from **SQL execution**. Destructive SQL goes through `execute_sql` with intent=execute and requires approval.

Flag missing indexes on foreign keys. For multi-tenant design prefer User → OrganizationMembership → Organization with session-scoped authorization.
