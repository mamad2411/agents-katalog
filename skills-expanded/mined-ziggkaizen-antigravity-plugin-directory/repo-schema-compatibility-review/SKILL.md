---
name: repo-schema-compatibility-review
description: Reviews schema and data contract changes for backwards compatibility, expand/contract sequencing, rollout order, rollback behavior, and client/service compatibility. Use when changing columns, fields, constraints, indexes, enum values, relationships, or persisted data formats.
---

# Repository Schema Compatibility Review

Use this skill when a schema or persisted data contract may affect deployed application versions, clients, jobs, reports, analytics, or integrations.

## When to Use This Skill

Use this skill for:

- adding, removing, renaming, or changing fields
- changing nullability, uniqueness, defaults, or constraints
- changing relationships or foreign keys
- changing indexes
- changing enum values
- changing API payload fields backed by persisted data
- changing event schemas or message payloads
- changing serialized data formats
- removing legacy data

## Compatibility Principles

- Prefer additive changes first.
- Avoid removing or renaming data fields in the same release that introduces replacements.
- Use dual-read or dual-write when needed.
- Backfill before requiring new fields.
- Validate existing data before adding constraints.
- Separate expansion and contraction into multiple deployable steps.
- Consider all consumers, not just the main application.

## Workflow

Use `workflows/schema-compatibility-review-workflow.md` for compatibility-sensitive changes.

## Resources

Use `resources/expand-contract-patterns.md` for general rollout patterns.

## Scripts

This skill owns:

```text
scripts/schema-compatibility-scan.py
```

Run it with `--help` before manual use.
