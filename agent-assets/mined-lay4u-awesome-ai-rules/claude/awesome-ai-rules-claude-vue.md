# Vue Project Rules

## Scope
- Applies to all Vue 3 applications and packages in this repository.
- Prioritize explicit typing, composability, and predictable rendering.

## Composition API First
- New components must use `<script setup lang="ts">`.
- Options API is legacy-only and must not be introduced in new modules.
- Share non-trivial logic through composables (`useFeature`).
- Keep composables framework-aware but domain-centered.

## TypeScript and Component Contracts
- Define props with typed `defineProps<T>()`.
- Define events with typed `defineEmits<T>()`.
- Export shared interfaces for reused prop/event contracts.
- Disallow `any` in component, store, and composable code.

## Reactivity Guidance
- Use `ref` for scalar values and nullable slots.
- Use `reactive` for tightly related object state.
- Preserve reactivity with `toRefs`/`storeToRefs` when destructuring.
- Prefer `computed` for derived data and cached transformations.

## State and Routing
- Use Pinia as the single state management solution.
- Keep stores small and domain-scoped.
- Follow Vue Router conventions with route-level code splitting.
- Validate and normalize route params before use in business logic.

## Naming and Structure
- Component filenames: PascalCase.
- Template usage: kebab-case tags.
- Composables: `useXxx.ts` naming.
- Group files by feature area rather than by technical layer only.

## Testing Standards
- Use Vitest and Vue Test Utils for component and composable tests.
- Test user-visible behavior, not internal implementation details.
- Cover emits, async loading states, and failure rendering.
- Keep tests deterministic with minimal mocking.

## Tooling
- Use `unplugin-auto-import` and `unplugin-vue-components` for controlled auto-import.
- Keep auto-import declarations committed and reproducible.
- Maintain lint and formatting consistency across SFCs and TS files.

## Completion Criteria
- Type-check, lint, and tests pass for changed code.
- New features use Composition API + Pinia + typed contracts.
- Routing, naming, and reactivity rules are respected.
