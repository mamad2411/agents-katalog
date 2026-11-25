---
name: svelte-development
description: "Build SvelteKit applications: runes and reactivity, load functions, form actions, adapters and component testing with Vitest."
type: procedural
category: web
domain: web
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - sveltekit load function
  - svelte runes state
  - sveltekit form action
  - svelte adapter deploy
  - svelte component test
keywords:
  - svelte
  - sveltekit
  - runes
  - vite
  - vitest
source: custom
enabled: true
---

# SvelteKit Development

## Purpose

Build SvelteKit applications: runes and reactivity, load functions, form actions, adapters and component testing with Vitest.

## When to Use

- You are implementing SvelteKit routes, load functions or form actions.
- Reactivity or hydration behaves differently on server and client.
- A deployment adapter must match the hosting target.

## When NOT to Use

- The project is Svelte 4 without runes and cannot upgrade yet.
- The task is purely a static marketing page with no framework behaviour.
- You need a backend service design unrelated to SvelteKit's server routes.

## Capabilities

- Use runes (`$state`, `$derived`, `$effect`) correctly, including SSR constraints.
- Separate server-only load logic from universal code.
- Implement progressive-enhancement form actions.
- Test components and load functions with Vitest.

## Inputs

- SvelteKit and Svelte versions, plus the adapter in use.
- The route tree and which data is server-only.
- The observed bug: hydration mismatch, stale state or failed deployment.

## Workflow

1. Identify what must run on the server (`+page.server.ts`) versus in the browser.
2. Model state with runes; keep derived values pure.
3. Move mutations into form actions with validation on the server.
4. Confirm secrets never enter universal load output.
5. Build with the production adapter and test the built output, not only dev mode.

## Tools

- vite
- svelte-check
- vitest + @testing-library/svelte

## Examples

- `npm run check`
- `npm run build && npm run preview`
- `npm run test -- --run`

## Safety

- Importing a server-only module into universal code can leak secrets into the client bundle.
- `$effect` runs after render; use it for side effects, never for derived data.
- Adapter choice determines runtime behaviour; do not assume Node APIs on edge targets.

## Source

All-Skills canonical library (`skills/web/svelte-development`). First-party skill, maintained in this repository.

## Notes

- `$derived` replaces most `$: ` reactive statements.
- Form actions degrade gracefully without JavaScript — keep them server-validated.
- Pairs with: `web/vue-development`, `web/frontend-design`.
