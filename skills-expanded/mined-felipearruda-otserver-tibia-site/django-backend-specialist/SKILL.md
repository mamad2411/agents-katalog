---
name: django-backend-specialist
description: Use this skill when the task is primarily about Django backend work: modeling data, writing views, forms, URLs, admin, settings, authentication, business rules, migrations, tests, or debugging server-side behavior in a Django project.
---

# Django Backend Specialist

## Overview

This skill is for implementing and reviewing Django backend code with emphasis on maintainability, correctness, and testability.

## When To Use

Use this skill when the user asks for work involving:

- Django models, managers, querysets, signals, or migrations
- Views, forms, URLs, middleware, admin, or settings
- Authentication, permissions, sessions, and server-side validation
- API endpoints built in Django or Django REST Framework
- Backend tests, debugging, refactors, and performance issues in Django code

## Working Style

- Inspect the current app structure before editing code.
- Prefer native Django patterns over custom abstractions unless the project already uses them.
- Keep domain rules close to the domain layer: model methods, services already present in the repo, or clearly named helpers.
- Avoid burying business logic in templates or scattered view code.
- Add or update tests for behavioral changes whenever practical.

## Implementation Rules

- Model changes must consider migrations, existing data, admin impact, and tests.
- Query changes should avoid obvious N+1 issues; use `select_related` and `prefetch_related` where justified.
- Forms and serializers must validate input explicitly rather than relying on template constraints.
- Views should stay thin when logic becomes reusable or complex.
- Settings changes must be conservative and environment-aware.
- Prefer class-based or function-based views according to the existing codebase style; do not mix styles arbitrarily.

## Review Checklist

- Is the data model coherent and normalized enough for the use case?
- Are permission and authentication checks enforced server-side?
- Does the change introduce migration or backward-compatibility risks?
- Are queries efficient for expected usage paths?
- Are tests covering the main success path and at least one failure path?

