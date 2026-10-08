---
name: rails-skills
description: Ruby on Rails framework patterns, best practices, and implementation guides
category: stacks/backend/rails
applies_to: rails
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Ruby on Rails Skills

Full-stack web framework for database-backed applications.

## Sub-Skills

### Database
- [active-record.md](database/active-record.md) - Active Record patterns
- [associations.md](database/associations.md) - Model associations
- [scopes.md](database/scopes.md) - Named scopes
- [migrations.md](database/migrations.md) - Database migrations

### Security
- [authentication.md](security/authentication.md) - Devise auth
- [authorization.md](security/authorization.md) - Pundit/CanCanCan
- [api-authentication.md](security/api-authentication.md) - API auth

### API
- [serializers.md](api/serializers.md) - JSON serialization
- [controllers.md](api/controllers.md) - API controllers
- [versioning.md](api/versioning.md) - API versioning

### Error Handling
- [exception-handling.md](error-handling/exception-handling.md) - Exception handling
- [logging.md](error-handling/logging.md) - Rails logging

### Testing
- [rspec.md](testing/rspec.md) - RSpec patterns
- [factory-bot.md](testing/factory-bot.md) - Factory Bot
- [integration.md](testing/integration.md) - Integration tests

### Performance
- [caching.md](performance/caching.md) - Rails caching
- [background-jobs.md](performance/background-jobs.md) - Sidekiq/ActiveJob

## Detection
Auto-detected when project contains:
- `Gemfile` with `rails`
- `config/routes.rb`
- `ApplicationController` class
