---
name: django-skills
description: Django framework patterns, best practices, and implementation guides
category: stacks/backend/django
applies_to: django
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Django Skills

Python web framework for perfectionists with deadlines.

## Sub-Skills

### Database
- [model-patterns.md](database/model-patterns.md) - Django model patterns
- [queryset-patterns.md](database/queryset-patterns.md) - QuerySet optimization
- [migrations.md](database/migrations.md) - Migration strategies

### Security
- [authentication.md](security/authentication.md) - Django auth system
- [permissions.md](security/permissions.md) - Permission classes
- [csrf-protection.md](security/csrf-protection.md) - CSRF protection

### API
- [drf-serializers.md](api/drf-serializers.md) - DRF serializer patterns
- [viewsets.md](api/viewsets.md) - ViewSet patterns
- [pagination.md](api/pagination.md) - Pagination patterns

### Error Handling
- [exception-handling.md](error-handling/exception-handling.md) - Exception handling
- [logging.md](error-handling/logging.md) - Logging configuration

### Testing
- [unit-testing.md](testing/unit-testing.md) - Django test framework
- [fixtures.md](testing/fixtures.md) - Test fixtures

### Performance
- [caching.md](performance/caching.md) - Django cache framework
- [query-optimization.md](performance/query-optimization.md) - Query optimization

## Detection
Auto-detected when project contains:
- `manage.py`
- `settings.py`
- `django` package
