---
name: svelte-implementation
description: "Implement Svelte/SvelteKit changes to components, routes, data flow, forms, SSR, or accessibility."
---

# Svelte Implementation

Build Svelte code around clear component boundaries, typed data, trusted server-side validation, accessible states, and measurable performance.

## Trigger boundary

Use this skill when a Svelte/SvelteKit change alters component or route behavior, load/data flow, forms, SSR/hydration, accessibility, browser security, or measured UI performance.

Do not load it for a small local rename, comment, formatting change, or mechanical edit that does not change user-visible or server/browser boundaries; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Założenia techniczne; Zasady ogólne
- [02-load-i-pobieranie-danych.md](./references/02-load-i-pobieranie-danych.md) - `load` i pobieranie danych; Komunikacja z API; Runtime config i zmienne środowiskowe; Autoryzacja i sesja
- [03-dostepnosc.md](./references/03-dostepnosc.md) - Dostępność; Performance UI i rendering; Bundle size i zależności frontendowe; Obrazy, fonty i assets
- [04-ci-lint-i-formatowanie.md](./references/04-ci-lint-i-formatowanie.md) - CI, lint i formatowanie; Review zależności; Deployment i hosting; SPA z osobnym API
