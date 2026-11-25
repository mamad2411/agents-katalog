---
name: mssql-review
description: "Review SQL Server schema, migrations, queries, indexes, .NET access, and transactions."
---

# MSSQL Review

Use this skill when reviewing SQL Server, EF Core, Dapper, stored procedure, migration, or database-backed .NET application changes.

## Process

1. Inspect the diff, surrounding data access code, migrations, stored procedures, configs, and tests before applying checklist items.
2. Check correctness, data integrity, tenant isolation, SQL injection risk, query shape, migration safety, locks, transactions, performance, observability, backup/DR impact, and tests.
3. Lead with concrete findings by severity, with file references, affected behavior, and missing verification.
4. Separate confirmed bugs from risks, questions, and follow-up suggestions.

## Large PR Subagent Review

For large pull requests, use focused subagents before producing the final review. Split by risk area such as schema/migrations, EF Core, Dapper/procedures, security/tenant boundaries, performance/indexing, operational readiness, or QA.

The main agent consolidates subagent findings, removes duplicates, resolves conflicts, decides final severity, and writes the final review summary.

## Coordination

Use with `itsol-code-review-workflow` for PR review process, `mssql-dotnet-data-access-design` for intended implementation patterns, `mssql-operations-debugging` for performance/incident evidence, and focused `security-*` or `infra-*` skills for trust boundaries or production deployment risk.

## Focused References

- [01-review-scope-and-findings.md](./references/01-review-scope-and-findings.md) - Review Scope And Findings
- [02-schema-query-and-stored-procedures.md](./references/02-schema-query-and-stored-procedures.md) - Schema Query And Stored Procedures
- [03-ef-dapper-and-migrations.md](./references/03-ef-dapper-and-migrations.md) - EF Dapper And Migrations
- [04-security-operations-tests.md](./references/04-security-operations-tests.md) - Security Operations And Tests
