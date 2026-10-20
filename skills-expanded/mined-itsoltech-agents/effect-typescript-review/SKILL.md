---
name: effect-typescript-review
description: "Review Effect TS changes to errors, layers, schemas, cleanup, concurrency, or retries."
---

# Effect TypeScript Review

Review whether Effect is clarifying boundaries or hiding complexity, with typed errors, safe dependencies, resource cleanup, and observable failures.

## Trigger boundary

Use this skill when an Effect TS diff changes typed errors, schemas, Context/Layer dependencies, resource cleanup, concurrency/retries, or observable runtime failure behavior.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no Effect boundary or runtime impact; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Mental model Effect; Granice uruchamiania Effect; Error model
- [02-api-client-i-fetch.md](./references/02-api-client-i-fetch.md) - API client i fetch; Schema i walidacja runtime; Typy domenowe, Data i branded types
- [03-services-context-i-layer.md](./references/03-services-context-i-layer.md) - Services, Context i Layer; Layer composition; Konfiguracja i sekrety; Resource management i Scope
- [04-concurrency.md](./references/04-concurrency.md) - Concurrency; Fibers i lifecycle; Queue, PubSub i backpressure; Cache i batching
- [05-testowanie.md](./references/05-testowanie.md) - Testowanie; Wydajność; Organizacja projektu; Czytelność i styl
- [06-minimalny-zestaw-kontroli-w-ci.md](./references/06-minimalny-zestaw-kontroli-w-ci.md) - Minimalny zestaw kontroli w CI; Checklist skrócony do code review
