---
name: database-security
description: Database security auditor covering PostgreSQL, MySQL, SQL Server, MongoDB, and Supabase/Firebase-style backends. Use when the user asks about database security, Row Level Security (RLS) policies, exposed database access, ORM-related SQL injection, or backend-as-a-service data access rules for any project.
---

# Database Security — Data Layer Auditor

A specialized skill for auditing the database layer: permissions, policies, queries, and data exposure.

## When to use this
- Any project using PostgreSQL/MySQL/MongoDB/SQL Server or a BaaS like Supabase/Firebase
- Reviewing Row Level Security (RLS) or equivalent row-level access rules
- Suspected data leakage or excessive permissions

## Core Checks

### SQL / NoSQL Injection
- Any query built via string concatenation with user input is a likely vulnerability — require parameterized queries or a correctly used ORM (Prisma, Drizzle, TypeORM, SQLAlchemy, Mongoose).
- Watch for "safe-looking but not" escape hatches: many ORMs expose `raw()`/`$queryRaw`/`.raw()` that bypass protection if fed unsanitized input.

### Row Level Security (Postgres/Supabase-style backends)
- Is RLS enabled on every table containing user data? (Enabling RLS with no policies blocks everything — but *forgetting* to enable it is often catastrophic.)
- Are `SELECT`/`INSERT`/`UPDATE`/`DELETE` policies written precisely (`auth.uid() = user_id`) instead of a blanket `true` policy?
- Is a service-role / admin key (which bypasses RLS) ever used in client-side code? This is always Critical — such keys must stay server-side only.

### Permissions and Roles
- Principle of least privilege: the application's runtime DB user should not have `DROP`/`ALTER` on tables it doesn't need to modify structurally.
- Separate read/write roles where appropriate.

### Database Exposure
- Is the database port open to the public internet without IP restrictions?
- Is the connection string kept only in environment variables — never committed to source control or config files checked into git?

### Sensitive Data
- Encryption at rest for especially sensitive fields when the regulatory/business context calls for it
- Passwords never stored in plaintext (details covered in `authentication-security`)

### Weak or Costly Queries
- Unbounded queries (missing `LIMIT`) on large tables that could enable denial-of-service
- Missing indexes on columns used frequently in permission-related filters (can slow down RLS checks and become a performance-driven weakness)

## Report Format
```
Table/Query: [name]
Issue: [problem]
Severity: Critical/High/Medium/Low
Evidence: [the policy or query in question]
Impact: [e.g., any authenticated user can read every other user's data]
Fix: [corrected policy or query]
```

## Rules
- When reviewing a BaaS like Supabase, ask to see the actual migration files or RLS policies rather than assuming their content.
- Never write actual exploitation queries against systems the user doesn't own.
