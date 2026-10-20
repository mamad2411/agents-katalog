---
name: repo-api-docs-review
description: Reviews API documentation, examples, changelogs, migration notes, deprecation notes, and client-facing evidence. Use when API behavior, contracts, request/response fields, errors, auth, pagination, or compatibility changes.
---

# Repository API Documentation Review

Use this skill to keep API docs aligned with behavior.

## When to Use This Skill

Use when API work changes request or response fields, errors, status codes, auth requirements, pagination, filtering, sorting, search, bulk behavior, versioning, deprecation, compatibility, examples, generated docs, client contracts, or migration guidance.

## Process

1. Identify client-visible behavior.
2. Ensure docs match implementation and contract.
3. Include safe request/response examples.
4. Include error examples.
5. Include auth and permission notes.
6. Include migration and deprecation guidance when needed.
7. Avoid secrets or production data in examples.

## Workflow

Use `workflows/api-docs-review-workflow.md`.

## Resources

- `resources/api-docs-checklist.md`

## Scripts

This skill owns:

```text
scripts/api-review-stop-reminder.py
```

The root-level `hooks.json` Stop hook calls this script.
