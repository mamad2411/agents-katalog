---
name: effect-typescript-debugging
description: "Diagnose Effect TS failures involving errors, layers, schemas, fibers, retries, or resources."
---

# Effect TypeScript Debugging

Trace Effect failures through Cause, Exit, requirements, layer composition, runtime boundaries, concurrency, and resource scope before patching symptoms.

## Trigger boundary

Use this skill when an Effect TS symptom may involve Cause/Exit, typed errors, Context/Layer composition, runtime schemas, fibers, concurrency, retries, streams, or resource scope.

Do not load it for a small local edit with a deterministic cause and no Effect boundary or runtime behavior change; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Granice uruchamiania Effect; Error model; Cause, Exit i diagnostyka błędów
- [02-schema-i-walidacja-runtime.md](./references/02-schema-i-walidacja-runtime.md) - Schema i walidacja runtime; Services, Context i Layer; Layer composition; Konfiguracja i sekrety
- [03-resource-management-i-scope.md](./references/03-resource-management-i-scope.md) - Resource management i Scope; Retry, timeouty i Schedule; Concurrency; Fibers i lifecycle
- [04-frontend-i-svelte-sveltekit.md](./references/04-frontend-i-svelte-sveltekit.md) - Frontend i Svelte/SvelteKit; Backend, CLI i workery; Testowanie; Wydajność
