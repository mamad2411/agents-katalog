---
name: hey-api-openapi-contract-debugging
description: "Diagnose divergence between OpenAPI, Hey API generation, client types, validation, or contract CI."
---

# Hey API OpenAPI Contract Debugging

Trace failures from OpenAPI input through generator config, output directory, generated types, runtime validation, API usage, and CI diff checks.

## Trigger boundary

Use this skill when OpenAPI input, generator configuration, generated output, runtime validation, API usage, or contract CI diverges and the failing boundary needs evidence.

Do not load it for a small local edit with a deterministic cause and no contract, generated-artifact, validation, or CI behavior change; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Instalacja i wersjonowanie; Podstawowa konfiguracja; Input specyfikacji
- [02-parser-patch-filters-i-transforms.md](./references/02-parser-patch-filters-i-transforms.md) - Parser, patch, filters i transforms; Plugin TypeScript; Plugin SDK; Klient Fetch
- [03-runtime-validation-i-zod.md](./references/03-runtime-validation-i-zod.md) - Runtime validation i Zod; TanStack Query plugin; Svelte i SvelteKit; Vite plugin
- [04-error-handling.md](./references/04-error-handling.md) - Error handling; Review wygenerowanego kodu; Testy; CI i kontrola kontraktu
