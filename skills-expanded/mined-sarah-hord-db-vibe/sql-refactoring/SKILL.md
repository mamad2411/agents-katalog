---
name: sql-refactoring
description: "Safe SQL and view refactoring patterns. Use when renaming columns, renaming views/tables, moving code, or making bulk changes across SQL files and dependent code."
---

# SQL Refactoring

Core Principle: **"Measure Twice, Cut Once."** Never refactor without understanding the full impact.

## When to Use This Skill

- Column renames across views and dependent code
- View or table renames
- Table migrations (e.g., moving from one schema to another)
- CTE extraction from complex subqueries
- Query consolidation
- Bulk changes across SQL codebases

## Safety Checklist

Before applying **any** refactor:
- [ ] Impact analysis completed -- all usages identified
- [ ] Preview of changes reviewed
- [ ] Backup or rollback plan exists
- [ ] Changes ordered by dependency (source first, then dependents)
- [ ] Tests exist or will be run after changes

## Reference Files

- [column-rename.md](column-rename.md) -- Full column rename workflow
- [view-rename.md](view-rename.md) -- Full view rename workflow
- [refactoring-patterns.md](refactoring-patterns.md) -- Common refactoring patterns and anti-patterns
