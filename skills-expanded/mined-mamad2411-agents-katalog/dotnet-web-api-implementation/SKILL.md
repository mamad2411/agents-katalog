---
name: dotnet-web-api-implementation
description: "Implement .NET changes to API contracts, validation, auth, persistence, or background jobs."
---

# Dotnet Web API Implementation

Keep architecture proportional: implement a clear API contract, validation, error handling, persistence boundary, observability, and tests without overbuilding patterns.

## Trigger boundary

Use this skill when a .NET change alters an API contract, validation or authorization boundary, EF Core/persistence behavior, background work, observability, or deployment-facing behavior.

Do not load it for a small local rename, comment, formatting change, or mechanical edit that does not change those boundaries; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Główna zasada; Dobór architektury do rozmiaru aplikacji
- [02-clean-architecture.md](./references/02-clean-architecture.md) - Clean architecture; DDD; CQRS; MediatR i pipeline handlers
- [Shared Program.cs and application composition](../_shared/references/dotnet-web-api/program-composition.md) - wspólne fakty dla implementacji: middleware, DI, options, DTO, validation i ProblemDetails
- [Shared API design](../_shared/references/dotnet-web-api/api-design.md) - wspólne fakty dla implementacji: OpenAPI, auth, browser security, secrets, HTTP, EF Core i transakcje
- [05-background-jobs.md](./references/05-background-jobs.md) - Background jobs; Cache; Rate limiting i abuse protection; Health checks
- [06-bezpieczenstwo-code-review.md](./references/06-bezpieczenstwo-code-review.md) - Bezpieczeństwo code review; Analizatory, warningi i jakość kodu; CI; Deployment i kontenery z perspektywy aplikacji
