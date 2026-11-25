---
name: tanstack-query-svelte-implementation
description: "Implement Svelte TanStack Query changes to keys, cache, mutations, SSR, or version-specific reactivity."
---

# TanStack Query Svelte Implementation

Model server state explicitly: stable keys, version-aware Svelte reactivity, safe cache invalidation, cancellation, typed API errors, and SSR-aware hydration.

## Trigger boundary

Use this skill when a Svelte TanStack Query change alters query keys/functions, cache invalidation, mutations, cancellation, SSR hydration, or v5/v6 reactivity. Detect `@tanstack/svelte-query` and `svelte` versions from `package.json` and lockfiles before choosing patterns.

Do not load it for a small local rename, comment, formatting change, or mechanical edit outside query/server-state behavior; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [10-version-policy-and-v6-migration.md](./references/10-version-policy-and-v6-migration.md) - Version gate; wybór v5/v6; wymagania v6; migracja z v5 do v6
- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Kiedy używać TanStack Query; Instalacja
- [02-prefetch-w-sveltekit-przez-initialdata.md](./references/02-prefetch-w-sveltekit-przez-initialdata.md) - Prefetch w SvelteKit przez `initialData`; Prefetch w SvelteKit przez `prefetchQuery`
- [03-domyslne-zachowania-v5.md](./references/03-domyslne-zachowania-v5.md) - Domyślne zachowania v5/v6; Query keys; Query options factory
- [04-createquery.md](./references/04-createquery.md) - `createQuery`; Reaktywność w Svelte; Statusy query w v5/v6; `enabled` i queries zależne
- [Shared API client and fetch](../_shared/references/tanstack-query-svelte/api-client-fetch.md) - wspólne fakty dla implementacji requestów, cancellation i `select`
- [Shared mutations](../_shared/references/tanstack-query-svelte/mutations.md) - wspólne fakty dla implementacji statusów, invalidacji, cache update i optimistic rollback
- [07-usemutationstate.md](./references/07-usemutationstate.md) - `useMutationState`; Paginacja; Infinite queries; Polling, refetch i realtime
- [Shared error handling](../_shared/references/tanstack-query-svelte/error-handling.md) - wspólne fakty dla błędów, formularzy, URL params, TypeScript, performance i offline cache
- [09-devtools.md](./references/09-devtools.md) - Devtools; ESLint plugin query; Testy; CI
