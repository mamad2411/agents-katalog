---
name: dotnet-skills
description: .NET Core/ASP.NET patterns, best practices, and implementation guides
category: stacks/backend/dotnet
applies_to: dotnet
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# .NET Backend Skills

Cross-platform framework for building modern cloud applications.

## Sub-Skills

### Architecture
- [clean-architecture.md](architecture/clean-architecture.md) - Clean architecture
- [mediator-pattern.md](architecture/mediator-pattern.md) - MediatR patterns
- [dependency-injection.md](architecture/dependency-injection.md) - DI patterns

### Database
- [ef-core-patterns.md](database/ef-core-patterns.md) - Entity Framework Core
- [repository-pattern.md](database/repository-pattern.md) - Repository pattern
- [unit-of-work.md](database/unit-of-work.md) - Unit of Work
- [migrations.md](database/migrations.md) - EF migrations

### Security
- [identity.md](security/identity.md) - ASP.NET Identity
- [jwt-auth.md](security/jwt-auth.md) - JWT authentication
- [authorization.md](security/authorization.md) - Policy-based auth
- [api-keys.md](security/api-keys.md) - API key auth

### Validation
- [fluent-validation.md](validation/fluent-validation.md) - FluentValidation
- [data-annotations.md](validation/data-annotations.md) - Data annotations

### Error Handling
- [problem-details.md](error-handling/problem-details.md) - Problem Details
- [global-exception.md](error-handling/global-exception.md) - Global handling
- [result-pattern.md](error-handling/result-pattern.md) - Result pattern

### Testing
- [xunit.md](testing/xunit.md) - xUnit patterns
- [integration.md](testing/integration.md) - Integration tests
- [moq.md](testing/moq.md) - Moq patterns

### Performance
- [caching.md](performance/caching.md) - Caching strategies
- [async-patterns.md](performance/async-patterns.md) - Async/await

## Detection
Auto-detected when project contains:
- `*.csproj` or `*.sln` files
- `Program.cs` file
- `using Microsoft.AspNetCore` imports
