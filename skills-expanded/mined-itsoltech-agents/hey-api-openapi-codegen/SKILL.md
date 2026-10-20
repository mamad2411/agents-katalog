---
name: hey-api-openapi-codegen
description: "Generate Hey API clients when OpenAPI contracts, generator config, or client integrations change."
---

# Hey API OpenAPI Codegen

Treat OpenAPI as the contract and generated code as an artifact; keep config versioned, output isolated, and contract checks in CI.

## Trigger boundary

Use this skill when an OpenAPI document, Hey API generator configuration, generated client/schema output, runtime validation, query integration, or contract CI changes.

Do not load it for a small local rename, comment, formatting change, or mechanical edit outside the contract and generated-artifact boundary; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Założenia; Instalacja i wersjonowanie
- [02-output-i-wygenerowane-pliki.md](./references/02-output-i-wygenerowane-pliki.md) - Output i wygenerowane pliki; OpenAPI jako kontrakt; Jakość schematów danych; Parser, patch, filters i transforms
- [Shared Fetch client](../_shared/references/hey-api/fetch-client.md) - wspólne fakty dla codegen: auth, komunikacja, runtime validation, Zod i TanStack Query
- [04-svelte-i-sveltekit.md](./references/04-svelte-i-sveltekit.md) - Svelte i SvelteKit; Vite plugin; Multi API, monorepo i wiele outputów; Bezpieczeństwo generowanego klienta
- [05-testy.md](./references/05-testy.md) - Testy; CI i kontrola kontraktu; Migracje kontraktu API; Publikacja wygenerowanego klienta jako paczki
