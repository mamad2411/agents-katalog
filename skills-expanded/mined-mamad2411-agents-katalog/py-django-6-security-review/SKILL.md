---
name: py-django-6-security-review
description: Reviews Django 6.0 settings, views, templates, sessions, cookies, authentication, authorization, uploads, CSP, CSRF, and deployment readiness. Use for security-sensitive Django changes or release preparation.
license: MIT
compatibility: Requires Django 6.0 and Python 3.12, 3.13, or 3.14.
---

# py-django-6 Security Review

## When to Use

Use this skill when working on:

- Production settings.
- Authentication or authorization.
- Session and cookie behavior.
- CSRF, CORS, CSP, clickjacking, redirects, or host validation.
- File uploads and media serving.
- Raw SQL and user-controlled queries.
- Admin exposure.
- Deployment readiness.

## Workflows

- `workflows/security-review-workflow.md`
- `workflows/deployment-readiness-workflow.md`

## Resources and Scripts

- `resources/security-settings-checklist.md`
- `scripts/django-security-check.sh`

Run scripts with `--help` before using them.

## Review Guidance

1. Identify the threat model for the changed code.
2. Check whether the change handles untrusted input.
3. Check authentication and authorization at the server boundary.
4. Check whether object-level permissions are enforced.
5. Check template escaping and unsafe HTML handling.
6. Check SQL construction and ORM usage.
7. Check cookie, session, CSRF, HTTPS, and host settings.
8. Check file upload validation and serving.
9. Check logging for sensitive data leaks.
10. Run or recommend `python manage.py check --deploy` for production-facing changes.

## Django 6.0 CSP Guidance

- Prefer Django’s built-in CSP settings and middleware.
- Use nonces where inline scripts cannot be eliminated.
- Avoid broad `unsafe-inline` and `unsafe-eval` policies.
- Use report-only mode before enforcement when changing an existing production app.
