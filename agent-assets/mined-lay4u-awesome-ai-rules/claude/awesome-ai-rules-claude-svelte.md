# Svelte + TypeScript Project Rules

## Scope
- Applies to Svelte 5 and SvelteKit projects using TypeScript.
- Optimize for maintainability, explicit state flow, and accessible interfaces.

## Core Architecture
- Prefer Svelte 5 rune APIs for all new component logic.
- Keep route boundaries thin and move heavy logic to reusable modules.
- Use feature-oriented folders for larger applications.

## Runes and Reactivity
- Use `$state` for mutable local state.
- Use `$derived` for computed values from source state.
- Use `$effect` only for external side effects and cleanup.
- Avoid reactive anti-patterns such as duplicating derivable state.

## Props and TypeScript
- Every component script uses `lang="ts"`.
- Read component inputs via `$props()`.
- Type props explicitly and keep public prop APIs small.
- Avoid `any`; narrow unknown external input at boundaries.

## SvelteKit Routing and Load
- Route entries must use `+page.svelte` and `+layout.svelte` conventions.
- Use `load` for route-level data acquisition.
- Keep `load` return payloads serializable and intentionally shaped.
- Keep privileged data access on server-side entry points.

## Stores, Context, and Sharing
- Default to runes for local and near-local state.
- Use writable/derived stores for truly cross-tree shared state.
- Prefer explicit data flow over hidden global state.

## Styling and Accessibility
- Use component-scoped CSS as the default style boundary.
- Use `:global` only when global cascade is required.
- Treat Svelte accessibility warnings as blockers unless justified.
- Ensure semantic structure and keyboard operability.

## Forms and Testing
- Use SvelteKit form actions for writes and server validation.
- Use progressive enhancement patterns to keep no-JS fallback working.
- Test with `vitest` plus `@testing-library/svelte`.
- Cover loading, error, empty, and success behavior.

## Definition of Done
- Typecheck and tests pass.
- Route/file conventions are respected.
- New UI is accessible and progressively enhanced.
