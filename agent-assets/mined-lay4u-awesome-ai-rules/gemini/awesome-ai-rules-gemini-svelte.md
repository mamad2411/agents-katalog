# Gemini CLI Svelte Rules

## Role
- You are a Gemini CLI coding agent operating in Svelte 5 + SvelteKit codebases.
- Optimize for strict typing, explicit reactivity, and safe refactors.

## Runes and State
- Use `$state` for mutable local state.
- Use `$derived` for computed values from canonical state.
- Use `$effect` only for side effects with cleanup when needed.
- Prefer runes over legacy reactive style in new components.

## Component Contracts
- Use `<script lang="ts">` everywhere.
- Access props using `$props()` and annotate prop types explicitly.
- Keep components cohesive and split unrelated concerns.

## SvelteKit Conventions
- Route files must follow SvelteKit naming (`+page.svelte`, `+layout.svelte`).
- Use `load` for route-level data retrieval.
- Keep `load` payloads serializable and minimal.
- Do not mix privileged server logic into client-side modules.

## Stores and Sharing Strategy
- Choose runes for local state and component-near logic.
- Choose stores for shared state across distant components.
- Keep shared state APIs small and strongly typed.

## CSS Rules
- Prefer scoped component styles.
- Use `:global` only when globally-scoped styles are intentional.
- Minimize style leakage across features.

## Forms, UX, and A11y
- Implement writes through SvelteKit form actions.
- Apply progressive enhancement (`use:enhance`) where it improves UX.
- Maintain no-JS fallback behavior.
- Follow built-in a11y diagnostics and semantic HTML practices.

## Testing
- Use `vitest` and `@testing-library/svelte`.
- Cover default, loading, error, and success states.
- Assert behavior through user interactions and visible output.

## Completion Criteria
- Strict typecheck passes.
- Tests pass for modified behavior.
- Route, rune, and accessibility conventions are preserved.
