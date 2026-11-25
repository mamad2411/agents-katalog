---
name: django-rest-framework-3-17-security-review
description: Reviews Django REST Framework 3.17.x APIs for authentication, authorization, object permissions, serializer field exposure, throttling, schema exposure, and unsafe commands. Use during API security reviews.
license: MIT
compatibility: Requires a Django project using Django REST Framework 3.17.x.
---

# Django REST Framework 3.17 Security Review

Use this skill when reviewing or hardening DRF 3.17.x endpoints.

## Review Priorities

1. Authentication and permission defaults.
2. Object-level authorization and tenant/user scoping.
3. Serializer field exposure and over-posting.
4. Input validation, nested writes, and file upload handling.
5. Throttling for expensive or abuse-prone endpoints.
6. Sensitive logging and exception behavior.
7. Schema, browsable API, and documentation exposure.
8. Dangerous database or migration commands proposed by agents.

## Helper Scripts

This skill includes:

- `scripts/drf-command-guard.py`

The script is designed for Antigravity hook usage but can be inspected with `--help`.

## Workflow References

- [api-security-review-workflow](workflows/api-security-review-workflow.md): Use for endpoint-level security review.

## Resource References

- [security-review-checklist](resources/security-review-checklist.md): Use as a security checklist.
- [permission-antipatterns](examples/permission-antipatterns.md): Use as examples of patterns to avoid.
