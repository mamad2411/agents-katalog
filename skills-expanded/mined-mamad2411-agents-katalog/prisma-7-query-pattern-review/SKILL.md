---
name: prisma-7-query-pattern-review
description: Reviews Prisma ORM 7 query patterns for performance, authorization, data leakage, raw SQL safety, sensitive logging, and optional database inspection. Use when changing Prisma Client queries, repositories, transactions, or query diagnostics.
license: MIT
compatibility: Requires Prisma ORM 7 generated client code or Prisma query code.
---

# Prisma ORM 7 Query Pattern Review

Use this skill for Prisma Client query review, query performance, sensitive data leakage, raw SQL review, transactions, and optional database inspection.

## When to Use This Skill

Use this skill when:

- Reviewing Prisma Client queries.
- Reviewing repository methods that return Prisma model data.
- Debugging slow queries or connection behavior.
- Adding raw SQL or TypedSQL.
- Checking for sensitive Prisma logging.
- Using Prisma MCP or MCP Toolbox for database context.

## Workflows

- `workflows/query-pattern-review-workflow.md`: Use for query correctness, security, leakage, and performance review.
- `workflows/database-inspection-workflow.md`: Use before enabling MCP-backed database inspection.

## Resources

- `resources/query-safety-checklist.md`: Query review checklist.
- `resources/mcp-toolbox-database-inspection-notes.md`: Safe MCP Toolbox usage notes.
- `resources/mcp-toolbox-tools-example.yaml`: Example read-only Toolbox tool configuration.

## Examples

- `examples/safe-prisma-query-patterns.md`: Safe Prisma query and raw SQL patterns.

## Operating Guidance

1. Apply authorization and tenant filters in the database query when possible.
2. Use `select` to avoid returning sensitive fields.
3. Avoid production query logging of sensitive values.
4. Keep transactions short.
5. Prefer generated Prisma types inside the database access layer.
6. Map raw Prisma model results to explicit DTOs at public or trust boundaries.
7. Use MCP database inspection only with explicit target/environment confirmation and least-privilege read-only tools.
