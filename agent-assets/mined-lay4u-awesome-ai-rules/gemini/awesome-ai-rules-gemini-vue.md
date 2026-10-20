# Gemini CLI Vue.js Rules

## Role
- You are a CLI coding agent for Vue 3 + TypeScript codebases.
- Deliver changes that are type-safe, testable, and architecture-consistent.

## Composition API Preference
- Build new components with `<script setup lang="ts">`.
- Treat Options API as legacy-only unless migration constraints require it.
- Extract shared feature logic into composables.
- Keep components lean by delegating heavy logic to composables/stores.

## Typed Component Interfaces
- Use `defineProps<T>()` for all non-trivial props.
- Use typed `defineEmits<T>()` for emitted event payloads.
- Avoid `any`; prefer explicit domain interfaces.
- Reuse shared types across components and stores.

## Reactivity Choices
- Use `ref` for primitive, optional, or replaceable values.
- Use `reactive` for grouped state objects with stable identity.
- Preserve reactivity on destructure with `toRefs` or `storeToRefs`.
- Use `computed` for derived values and memoized transformations.

## Pinia and Router Guidance
- Use Pinia for shared state and workflow orchestration.
- Keep stores domain-focused with explicit actions.
- Follow Vue Router conventions and lazy-load route components.
- Parse and validate route params/query close to route entry points.

## Naming Rules
- Component filenames are PascalCase.
- Component usage in templates is kebab-case.
- Composable names follow `useXxx.ts`.
- Keep directories feature-oriented for discoverability.

## Testing and Tooling
- Use Vitest and Vue Test Utils as the standard test stack.
- Cover props, emits, user interactions, and failure/loading states.
- Mock only external boundaries (network, router, time).
- Configure auto-import through `unplugin-auto-import` and `unplugin-vue-components`.
- Commit generated typing artifacts required for IDE/type-check support.

## Finish Criteria
- Lint, type-check, and test suites pass.
- Composition API, typed contracts, Pinia, and Router conventions are followed.
