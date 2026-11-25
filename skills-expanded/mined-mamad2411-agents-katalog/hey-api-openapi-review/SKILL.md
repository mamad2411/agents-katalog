---
name: hey-api-openapi-review
description: "Review changed OpenAPI contracts, Hey API config or output, auth, validation, or contract CI."
---

# Hey API OpenAPI Review

Review whether generated client changes reflect a clear API contract, safe config, isolated output, runtime validation needs, security, and CI enforcement.

## Trigger boundary

Use this skill when a diff changes an OpenAPI contract, Hey API config or generated client/schema output, auth/runtime validation, output isolation, or contract CI.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no contract, generated-artifact, security, or CI impact; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Założenia; Instalacja i wersjonowanie; Struktura katalogów
- [02-openapi-jako-kontrakt.md](./references/02-openapi-jako-kontrakt.md) - OpenAPI jako kontrakt; Jakość schematów danych; Parser, patch, filters i transforms; Plugin TypeScript
- [Shared Fetch client](../_shared/references/hey-api/fetch-client.md) - wspólne fakty; oceń klienta zgodnie z review flow i publicznym kontraktem
- [04-svelte-i-sveltekit.md](./references/04-svelte-i-sveltekit.md) - Svelte i SvelteKit; Multi API, monorepo i wiele outputów; Bezpieczeństwo generowanego klienta; Error handling
- [05-ci-i-kontrola-kontraktu.md](./references/05-ci-i-kontrola-kontraktu.md) - CI i kontrola kontraktu; Migracje kontraktu API; Checklist do code review; Minimalny standard projektu
