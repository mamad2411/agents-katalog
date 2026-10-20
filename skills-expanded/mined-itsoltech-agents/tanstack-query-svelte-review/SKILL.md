---
name: tanstack-query-svelte-review
description: "Review Svelte TanStack Query changes to keys, cache, SSR, mutations, or stores/runes reactivity."
---

# TanStack Query Svelte Review

Review server-state behavior for stable keys, correct query functions, version-aware Svelte reactivity, safe mutation side effects, SSR correctness, and security-sensitive cache handling.

## Trigger boundary

Use this skill when a Svelte TanStack Query diff changes query keys/functions, cache or mutation side effects, SSR hydration, auth/tenant-sensitive cache data, or v5/v6 Svelte reactivity. Detect `@tanstack/svelte-query` and `svelte` versions before judging patterns.

Do not load it for a small local rename, comment, formatting change, or mechanical edit outside query/server-state behavior; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [11-version-policy-and-v6-review.md](./references/11-version-policy-and-v6-review.md) - Version gate; review v5; review v6; review migracji z v5 do v6
- [01-overview.md](./references/01-overview.md) - Overview; Kiedy używać TanStack Query; Minimalna konfiguracja klienta; Konfiguracja dla SvelteKit SSR
- [02-prefetch-w-sveltekit-przez-prefetchquery.md](./references/02-prefetch-w-sveltekit-przez-prefetchquery.md) - Prefetch w SvelteKit przez `prefetchQuery`; Domyślne zachowania v5
- [03-query-keys.md](./references/03-query-keys.md) - Query keys; Query options factory; `createQuery`
- [04-reaktywnosc-w-svelte.md](./references/04-reaktywnosc-w-svelte.md) - Reaktywność w Svelte; Statusy query w v5/v6; `enabled` i queries zależne
- [Shared API client and fetch](../_shared/references/tanstack-query-svelte/api-client-fetch.md) - wspólne fakty; użyj ich jako review rubryku requestów, cancellation i `select`
- [Shared mutations](../_shared/references/tanstack-query-svelte/mutations.md) - wspólne fakty; użyj ich jako review rubryku statusów, invalidacji i optimistic rollback
- [07-paginacja.md](./references/07-paginacja.md) - Paginacja; Infinite queries; Polling, refetch i realtime; Cache a auth, logout i tenant
- [Shared error handling](../_shared/references/tanstack-query-svelte/error-handling.md) - wspólne fakty; użyj ich jako review rubryku błędów, formularzy, filters, typing, performance i offline cache
- [09-devtools.md](./references/09-devtools.md) - Devtools; ESLint plugin query; Testy; CI
- [10-checklist-do-code-review.md](./references/10-checklist-do-code-review.md) - Checklist do code review
