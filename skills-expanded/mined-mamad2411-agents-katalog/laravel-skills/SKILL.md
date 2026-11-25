---
name: laravel-skills
description: Laravel framework patterns, best practices, and implementation guides
category: stacks/backend/laravel
applies_to: laravel
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Laravel Skills

PHP web framework with expressive, elegant syntax.

## Sub-Skills

### Database
- [eloquent-patterns.md](database/eloquent-patterns.md) - Eloquent ORM patterns
- [relationships.md](database/relationships.md) - Model relationships
- [query-scopes.md](database/query-scopes.md) - Query scopes
- [migrations.md](database/migrations.md) - Migration patterns

### Security
- [authentication.md](security/authentication.md) - Laravel auth
- [authorization.md](security/authorization.md) - Gates and policies
- [api-auth.md](security/api-auth.md) - API authentication

### API
- [resources.md](api/resources.md) - API resources
- [controllers.md](api/controllers.md) - Controller patterns
- [validation.md](api/validation.md) - Request validation

### Error Handling
- [exception-handling.md](error-handling/exception-handling.md) - Exception handling
- [logging.md](error-handling/logging.md) - Logging patterns

### Testing
- [feature-testing.md](testing/feature-testing.md) - Feature tests
- [unit-testing.md](testing/unit-testing.md) - Unit tests
- [factories.md](testing/factories.md) - Model factories

### Performance
- [caching.md](performance/caching.md) - Laravel cache
- [queues.md](performance/queues.md) - Queue processing

## Detection
Auto-detected when project contains:
- `artisan` file
- `composer.json` with `laravel/framework`
- `Illuminate\\` namespace
