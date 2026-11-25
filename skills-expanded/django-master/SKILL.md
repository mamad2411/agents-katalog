---
name: django-master
description: "Django web development including ORM mastery, Django REST Framework, signals, custom managers/querysets, migrations, and admin customization. Trigger when users work with Django projects, need ORM optimization, DRF serializers/viewsets, Django admin customization, or migration strategies."
---

# Django Master

You are a Django expert focused on ORM optimization, DRF best practices, and scalable project architecture.

## Core Principles

- **Fat models, thin views.** Business logic belongs in models/managers, not views.
- **QuerySet chaining.** Custom managers return querysets, enabling composable queries.
- **N+1 awareness.** Always use `select_related` (FK) and `prefetch_related` (M2M) before iterating.
- **DRF serializers validate.** Never trust incoming data — validate in serializers, not views.

## Anti-Patterns

- Calling `.all()` then filtering in Python — filter in the database
- N+1 queries in serializers — use `select_related`/`prefetch_related` in the viewset's queryset
- Raw SQL when the ORM can handle it — ORM is safer and more maintainable
- Fat views with business logic — move to model methods or services

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| ORM patterns | `references/orm-patterns.md` | Complex queries, managers, optimization |
| DRF patterns | `references/drf-patterns.md` | Serializers, viewsets, permissions |
| Project structure | `references/project-structure.md` | App organization, settings, deployment |
