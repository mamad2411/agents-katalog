---
name: nestjs-skills
description: NestJS framework patterns, best practices, and implementation guides
category: stacks/backend/nestjs
applies_to: nestjs
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# NestJS Skills

Progressive Node.js framework for building efficient, reliable and scalable server-side applications.

## Sub-Skills

### Architecture
- [modular-architecture.md](architecture/modular-architecture.md) - NestJS modular patterns
- [clean-architecture.md](architecture/clean-architecture.md) - Clean architecture implementation
- [cqrs-pattern.md](architecture/cqrs-pattern.md) - CQRS with @nestjs/cqrs

### Database
- [prisma-patterns.md](database/prisma-patterns.md) - Prisma ORM patterns
- [typeorm-patterns.md](database/typeorm-patterns.md) - TypeORM patterns
- [repository-pattern.md](database/repository-pattern.md) - Repository pattern

### Security
- [authentication.md](security/authentication.md) - JWT authentication
- [authorization.md](security/authorization.md) - RBAC/ABAC patterns
- [guards-strategies.md](security/guards-strategies.md) - Guard strategies

### Validation
- [dto-validation.md](validation/dto-validation.md) - DTO validation with class-validator
- [custom-validators.md](validation/custom-validators.md) - Custom validation decorators

### Error Handling
- [exception-filters.md](error-handling/exception-filters.md) - Exception filter patterns
- [error-responses.md](error-handling/error-responses.md) - Standardized error responses

### Testing
- [unit-testing.md](testing/unit-testing.md) - Unit testing patterns
- [e2e-testing.md](testing/e2e-testing.md) - E2E testing with supertest

### Performance
- [caching.md](performance/caching.md) - Caching strategies
- [queue-processing.md](performance/queue-processing.md) - Queue processing with Bull

## Detection
Auto-detected when project contains:
- `nest-cli.json`
- `*.module.ts` files
- `@nestjs/core` or `@nestjs/common` packages
