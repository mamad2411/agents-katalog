---
name: svelte-debugging
description: "Diagnose Svelte/SvelteKit failures across data flow, reactivity, forms, auth, hydration, or SSR."
---

# Svelte Debugging

Debug Svelte problems by isolating whether the failure is data loading, reactivity, component state, browser behavior, API integration, or deployment mode.

## Trigger boundary

Use this skill when a Svelte/SvelteKit symptom crosses load/data flow, reactivity, component state, forms, auth/session, hydration/SSR, browser behavior, API integration, or deployment mode.

Do not load it for a small local edit with a deterministic cause and no user-visible, server/browser, or deployment behavior change; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Svelte 5 reactivity; Props, events, bind i snippets; State management
- [02-autoryzacja-i-sesja.md](./references/02-autoryzacja-i-sesja.md) - Autoryzacja i sesja; Formularze, Superforms i Zod; CSRF, CORS i cookies; Storage w przeglądarce
- [03-deployment-i-hosting.md](./references/03-deployment-i-hosting.md) - Deployment i hosting; SPA z osobnym API; SSR/SvelteKit server mode
