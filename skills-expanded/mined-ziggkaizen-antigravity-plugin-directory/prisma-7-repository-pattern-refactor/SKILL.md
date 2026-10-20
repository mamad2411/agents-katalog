---
name: prisma-7-repository-pattern-refactor
description: Refactors Prisma ORM 7 repository and service-layer patterns. Use when Prisma Client access is duplicated, raw model shapes leak across boundaries, generated client imports are inconsistent, or transaction boundaries need cleanup.
license: MIT
compatibility: Requires Prisma ORM 7 generated client code or repository/service code using Prisma Client.
---

# Prisma ORM 7 Repository Pattern Refactor

Use this skill for improving how application code wraps Prisma Client.

## When to Use This Skill

Use this skill when:

- Prisma Client is instantiated in multiple places.
- Generated client imports are inconsistent.
- Repository methods leak raw model shapes to public API layers.
- Transaction boundaries are unclear.
- Query logic is duplicated across services.
- Tests are hard to write because database access is tightly coupled.

## Workflows

- `workflows/repository-pattern-refactor-workflow.md`: Use for refactoring repository/service boundaries around Prisma Client.

## Resources

- `resources/repository-pattern-guidelines.md`: Repository and service-layer guidelines.

## Examples

- `examples/prisma-repository-pattern.md`: Example repository wrapper around Prisma Client.

## Operating Guidance

1. Keep Prisma Client construction centralized.
2. Import generated Prisma Client from the configured output path.
3. Keep repository methods small and named by business intent.
4. Return explicit DTOs for public or trust-boundary responses.
5. Keep transactions at the service/use-case boundary when multiple repository operations must commit together.
6. Add regression tests before large refactors.
