---
name: node-pg-8-safe-query-design
description: Designs and implements safe Node pg 8.x handwritten SQL queries, parameterized values, narrow repository functions, and stable result contracts. Use for SELECT, INSERT, UPDATE, DELETE, and UPSERT work.
license: MIT
compatibility: Node applications using Node pg 8.x with handwritten SQL.
---

# Node pg 8 Safe Query Design

This skill guides production data-access functions using Node `pg` 8.x and handwritten SQL.

## When to Use

Use this skill when the task involves:

- adding or changing `pool.query` or `client.query`
- creating repository/data-access modules
- implementing `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `UPSERT`
- designing SQL parameter order and return shapes
- converting unsafe SQL to parameterized SQL
- adding result mapping or row-count checks
- keeping SQL direct and reviewable without an ORM

## Core Approach

1. Confirm the codebase uses `pg` 8.x and handwritten SQL.
2. Locate the shared pool/client boundary before adding new connection code.
3. Define the repository function contract before writing SQL:
   - inputs
   - authorization assumptions
   - returned row shape
   - expected row count
   - transaction participation
   - error behavior
4. Write SQL as a readable constant or query config object.
5. Use `$1`, `$2`, and `values` for all values.
6. Keep dynamic identifiers allowlisted and rare.
7. Map rows to a stable application shape instead of leaking arbitrary `SELECT *` results.
8. Add tests for success, no rows, duplicate/conflict behavior, nulls, and authorization-sensitive predicates.

## Required Patterns

- Prefer `pool.query(text, values)` for one standalone statement.
- Prefer a query config object when `rowMode` or local type parser behavior is truly needed.
- Avoid named prepared statements by default; add them only after measuring benefit.
- Prefer explicit column lists and stable aliases.
- Check `rowCount` for updates/deletes/inserts when expected cardinality matters.
- Return `null` or a domain-specific not-found result consistently.

## Workflows

Use `workflows/implement-handwritten-sql-workflow.md` when implementing a new SQL-backed feature or refactoring existing handwritten SQL.

## Resources

Use `resources/query-contract-checklist.md` before finalizing a repository function.

## Examples

Use `examples/repository-example.md` for a compact TypeScript repository pattern.
