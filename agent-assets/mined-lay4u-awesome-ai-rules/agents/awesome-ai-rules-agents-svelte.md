# Codex Svelte Rules

## Role
- You are an OpenAI Codex agent working in Svelte 5 + SvelteKit repositories.
- Optimize for correctness, maintainability, and low-surprise behavior.

## Reactivity Model
- Default to runes in new code.
- Use `$state` for mutable local state.
- Use `$derived` for deterministic computed values.
- Use `$effect` only when syncing with external systems.
- Do not use effects for pure calculations.

## TypeScript and Props
- Every Svelte component must use `<script lang="ts">`.
- Inputs are read via `$props()` and typed explicitly.
- Avoid `any`; prefer `unknown` plus narrowing at boundaries.
- Keep component APIs small and stable.

## SvelteKit Structure
- Respect route conventions (`+page.svelte`, `+layout.svelte`).
- Use `load` functions for route data hydration and shaping.
- Keep load results serializable and intentional.
- Keep server-only work on server-safe modules/routes.

## Stores vs Runes
- Prefer runes for local state and collocated logic.
- Use stores for cross-route or wide shared state.
- Keep stores typed and narrowly scoped.

## Styling
- Use component-scoped CSS by default.
- Use `:global` only for explicit global overrides.
- Avoid leaking styles through broad selectors.

## Forms and Progressive Enhancement
- Implement mutations through SvelteKit form actions.
- Use `use:enhance` to improve UX without breaking no-JS flow.
- Handle pending, success, and error states explicitly.

## Accessibility and Testing
- Preserve built-in accessibility safeguards.
- Prefer semantic elements and keyboard-reachable controls.
- Use `vitest` and `@testing-library/svelte` for UI tests.
- Test user-visible behavior, not internal implementation details.

## Definition of Done
- Typecheck and tests pass.
- New code follows rune-first, route-convention, and accessibility rules.
