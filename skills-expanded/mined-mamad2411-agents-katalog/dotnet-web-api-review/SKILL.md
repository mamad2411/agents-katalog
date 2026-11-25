---
name: dotnet-web-api-review
description: "Review .NET changes to API contracts, auth, persistence, jobs, deployment, or behavior tests."
---

# Dotnet Web API Review

Review API changes for proportional architecture, contract clarity, validation, security, data consistency, async behavior, observability, and test coverage.

## Trigger boundary

Use this skill when a .NET diff changes an API contract, validation or authorization boundary, EF Core/data consistency, background work, observability, tests, or deployment behavior.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no API, runtime, data, security, or deployment impact; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Główna zasada; Dobór architektury do rozmiaru aplikacji; Vertical slice
- [02-ddd.md](./references/02-ddd.md) - DDD; CQRS; MediatR i pipeline handlers; Minimal APIs czy kontrolery
- [Shared Program.cs and application composition](../_shared/references/dotnet-web-api/program-composition.md) - wspólne fakty; oceń diff według review flow i zakresu tego skilla
- [Shared API design](../_shared/references/dotnet-web-api/api-design.md) - wspólne fakty; użyj ich jako rubryku kontraktu, bezpieczeństwa, danych i transakcji
- [05-background-jobs.md](./references/05-background-jobs.md) - Background jobs; Cache; Rate limiting i abuse protection; Health checks
- [06-deployment-i-kontenery-z-perspektywy-aplikacji.md](./references/06-deployment-i-kontenery-z-perspektywy-aplikacji.md) - Deployment i kontenery z perspektywy aplikacji; Migracje bazy; Kiedy przemyśleć refactor; Minimalny standard nowego API
- [07-przykladowy-szablon-pr.md](./references/07-przykladowy-szablon-pr.md) - Przykładowy szablon PR
