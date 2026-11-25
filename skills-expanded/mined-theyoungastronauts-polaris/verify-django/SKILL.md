---
name: verify-django
description: "Django/DRF verification checklist — models, serializers, views, security, API contract."
disable-model-invocation: true
---

# Skill: Verify Django

## Purpose
Systematic verification checklist for Django/DRF code. Used by the reviewer agent in a separate Claude session after code execution.

## Verification Process

Run through each section. Flag issues as PASS, WARN, or FAIL.

### 1. Tests
- [ ] Tests exist for new/changed code
- [ ] `pytest` passes with no failures
- [ ] Test coverage is reasonable (not just happy path)
- [ ] Factory data is realistic (not "test123" placeholder values)

### 2. Models
- [ ] Migrations are generated and match model changes
- [ ] No migration conflicts with main branch
- [ ] New fields have sensible defaults or are nullable where appropriate
- [ ] Indexes exist on fields used in filters/lookups
- [ ] `__str__` methods are defined

### 3. Serializers
- [ ] Fields are explicitly listed (no `__all__`)
- [ ] Read vs write serializers separated where needed
- [ ] Validation covers edge cases (empty strings, nulls, boundaries)
- [ ] Nested serializer performance — no N+1 from nested reads

### 4. Views
- [ ] `permission_classes` set on every view
- [ ] Querysets use `select_related`/`prefetch_related` appropriately
- [ ] Pagination is configured for list endpoints
- [ ] Error responses are consistent and informative
- [ ] No business logic in views — delegated to models/services

### 5. Security
- [ ] Authentication required on all non-public endpoints
- [ ] Object-level permissions checked (not just role-based)
- [ ] `SECRET_KEY` is set from the environment and not the shipped default (`django-insecure-change-me-in-production`) in production
- [ ] No sensitive data in response bodies that shouldn't be there
- [ ] Input validation prevents injection (Django handles most, but check raw SQL)

### 6. API Contract
- [ ] Endpoint paths follow project conventions
- [ ] Response shapes are consistent with existing endpoints
- [ ] Integration summary is up to date
- [ ] Breaking changes are documented

### 7. Code Quality
- [ ] No commented-out code
- [ ] No debug prints or leftover logging
- [ ] Imports are clean (no unused)
- [ ] Linting passes (ruff/flake8)
- [ ] Type hints on function signatures

### 8. Development Environment
- [ ] `Dockerfile.dev` exists
- [ ] `docker-compose.yml` has the services for the project's blueprint tier — minimal: web + db; standard: + redis; full: + celery + celery-beat (check which tier the project was bootstrapped with)
- [ ] `Makefile` exists and wraps all commands via `docker compose exec`
- [ ] No `python manage.py` commands used directly on host

## Output
Produce a `verification-report.md`:
```markdown
# Verification Report: [Feature/Phase]
Date: [date]
Reviewer: Claude (automated)

## Summary: [PASS/WARN/FAIL]

## Details
### Tests: [PASS/WARN/FAIL]
- [notes]

### Models: [PASS/WARN/FAIL]
- [notes]

...

## Issues Found
1. [FAIL] Description + suggested fix
2. [WARN] Description + recommendation

## Recommended Actions
- [ ] Fix: ...
- [ ] Consider: ...
```
