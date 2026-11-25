---
name: repo-api-compatibility-review
description: Reviews API changes for breaking changes, deprecation needs, client impact, rollout strategy, generated-client risk, and migration paths. Use when request/response shapes, status codes, schema files, events, webhooks, SDK contracts, or API docs change.
---

# Repository API Compatibility Review

Use this skill to review API changes for client impact.

## When to Use This Skill

Use this skill when changes affect endpoint paths, operation names, request or response fields, field types, status codes, errors, pagination, filtering, sorting, auth requirements, events, webhooks, schemas, SDK contracts, generated clients, or API documentation.

## Process

1. Inventory changed API files.
2. Classify the change as additive, behavior-changing, or breaking.
3. Identify affected clients.
4. Define deprecation and migration needs.
5. Check documentation and changelog evidence.
6. Check tests and compatibility validation.
7. Recommend rollback or mitigation.

## Workflow

Use `workflows/api-breaking-change-review-workflow.md`.

## Resources

- `resources/api-compatibility-checklist.md`

## Examples

- `examples/breaking-change-feedback-example.md`

## Scripts

This skill owns:

```text
scripts/api-breaking-change-scan.py
```

Run with `--help` before manual use.
