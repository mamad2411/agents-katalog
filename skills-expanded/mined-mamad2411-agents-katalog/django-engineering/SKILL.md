---
name: django-engineering
description: Develop maintainable Django applications. Use when building or
  reviewing Django projects.
metadata:
  tags: django, engineering
---

# Django Engineering

## Use this skill when
- Structuring Django apps, models, and views
- Writing queries and using the ORM safely
- Implementing auth, permissions, and settings
- Writing Django tests and migrations

## Do not use this skill when
- Non-Python backends
- Fetching/writing data unrelated to Django (use django-pro for advanced patterns)

## Instructions
1. Split functionality into focused Django apps; one app per domain.
2. Model with explicit fields, indexes, and constraints; use migrations for schema changes.
3. Avoid N+1: use select_related/prefetch_related.
4. Default views to class-based or function-based consistently; keep them thin.
5. Run permission checks at the view and serialization boundary.
6. Keep settings environment-specific via env vars and settings modules.
7. Write model and view tests with signals/triggers in mind.

## Checklist
- Migrations are committed and reviewed
- Querysets are profiled for N+1 at request hot spots

## Output Format
- App map | model design | query hotspots | permission matrix

## Common Mistakes
- Giant models with all business logic
- Raw SQL where the ORM suffices
- Debug=True or hidden secrets in settings
