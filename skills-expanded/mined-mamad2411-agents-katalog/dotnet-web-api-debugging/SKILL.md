---
name: dotnet-web-api-debugging
description: "Diagnose .NET failures across middleware, auth, persistence, jobs, caching, or deployment."
---

# Dotnet Web API Debugging

Debug through middleware, endpoint, validation, domain, data, integration, cache, job, and deployment layers using logs and traces before changing code.

## Trigger boundary

Use this skill when a .NET symptom crosses middleware, endpoint, validation, domain, persistence, integration, cache, job, health, or deployment behavior and needs evidence to isolate.

Do not load it for a small local edit with a deterministic cause and no runtime, data, auth, or deployment behavior change; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Program.cs i składanie aplikacji; Middleware; Dependency injection
- [02-data-protection-i-wiele-instancji.md](./references/02-data-protection-i-wiele-instancji.md) - Data Protection i wiele instancji; Komunikacja HTTP z innymi usługami; EF Core i dostęp do danych; Transakcje i spójność
- [03-debugowanie-produkcyjnych-problemow.md](./references/03-debugowanie-produkcyjnych-problemow.md) - Debugowanie produkcyjnych problemów; Wydajność aplikacji; Skalowanie aplikacji; Rodzaje testów
- [04-migracje-bazy.md](./references/04-migracje-bazy.md) - Migracje bazy; Kiedy przemyśleć refactor; Upgrade do nowszej wersji .NET
