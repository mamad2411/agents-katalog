---
name: py-django-6-project-setup
description: Creates or normalizes Django 6.0 project setup, dependency pins, settings layout, app structure, environment configuration, and first-run checks. Use when starting a Django 6 project or aligning an existing project with Django 6 conventions.
license: MIT
compatibility: Requires Django 6.0 and Python 3.12, 3.13, or 3.14.
---

# py-django-6 Project Setup

## When to Use

Use this skill when the user asks to:

- Create a Django 6.0 project or app.
- Review or normalize Django settings.
- Pin Django dependencies.
- Set up local development commands.
- Add baseline project structure, static files, templates, or environment configuration.
- Prepare a project for further Django feature work.

## Version Boundaries

- Target Django 6.0 only.
- Use Python 3.12, 3.13, or 3.14.
- Do not add optional dependencies unless the user asks or the project already uses them.

## Workflow

Use `workflows/new-project-setup-workflow.md` for repeatable setup tasks.

## Resources

- `resources/settings-baseline.md` summarizes safe settings expectations.
- `examples/pyproject-dependencies-example.md` shows minimal dependency pinning patterns.

## Instructions

1. Inspect existing package manager files before adding or changing dependencies.
2. Confirm the active Python version and Django version.
3. Prefer the repository’s existing package manager and lockfile.
4. Keep project settings environment-aware without hard-coding secrets.
5. Keep optional integrations out of the base setup unless explicitly requested.
6. Use Django-native commands for baseline validation:
   - `python manage.py check`
   - `python manage.py makemigrations --check --dry-run`
   - `python manage.py test`
7. For production-facing settings, also use:
   - `python manage.py check --deploy`

## Setup Conventions

Use a clear settings structure. Accept existing conventions, but prefer a pattern like:

```text
config/
├── settings/
│   ├── __init__.py
│   ├── base.py
│   ├── local.py
│   ├── test.py
│   └── production.py
├── urls.py
├── asgi.py
└── wsgi.py
```

Use project apps with explicit names, for example:

```text
apps/
└── billing/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    ├── models.py
    ├── tests/
    ├── urls.py
    └── views.py
```

## Safety Rules

- Do not run destructive management commands during setup.
- Do not overwrite existing settings or dependency files without inspecting them.
- Do not commit `.env` files with secrets.
- Do not enable production-only HTTPS settings in local settings unless the project supports local TLS.
