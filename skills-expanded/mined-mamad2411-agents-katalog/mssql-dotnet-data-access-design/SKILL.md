---
name: mssql-dotnet-data-access-design
description: "Design SQL Server .NET access with EF Core, Dapper, procedures, transactions, and migrations."
---

# MSSQL Dotnet Data Access Design

Use this skill when designing or implementing SQL Server data access in .NET applications using EF Core, Dapper, stored procedures, migrations, transactions, indexing, or database-backed features.

## Process

1. Identify access patterns, write/read paths, expected cardinality, tenant boundaries, retention needs, and operational constraints before choosing schema or data-access style.
2. Choose EF Core, Dapper, stored procedures, or a combination per use case. Do not make it an ideological project-wide rule.
3. Keep domain logic, DTO composition, API response formatting, and JSON serialization in the application unless there is a narrow, explicitly justified exception.
4. Design rollout, rollback or roll-forward, verification, and observability together with the code change.

## Coordination

Use with `dotnet-web-api-implementation` for ASP.NET Core behavior, `mssql-review` before handoff, `mssql-operations-debugging` for production symptoms, and focused `security-*` or `infra-*` skills when the change touches permissions, secrets, deployment, backup, HA, or production readiness.

## Focused References

- [01-principles-modeling-tenancy.md](./references/01-principles-modeling-tenancy.md) - Principles Modeling And Tenancy
- [02-ef-dapper-stored-procedures.md](./references/02-ef-dapper-stored-procedures.md) - EF Dapper And Stored Procedures
- [03-query-performance-transactions-migrations.md](./references/03-query-performance-transactions-migrations.md) - Query Performance Transactions And Migrations
- [04-testing-and-feature-checklist.md](./references/04-testing-and-feature-checklist.md) - Testing And Feature Checklist
