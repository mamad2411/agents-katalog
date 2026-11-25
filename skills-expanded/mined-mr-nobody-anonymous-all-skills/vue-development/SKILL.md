---
name: vue-development
description: "Build Vue 3 applications: Composition API, script setup, reactivity boundaries, Pinia state, routing and Vitest component tests."
type: procedural
category: web
domain: web
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - vue 3 composition api
  - pinia store design
  - vue reactivity bug
  - vue router guard
  - vitest component test
keywords:
  - vue
  - vue3
  - composition-api
  - pinia
  - vitest
  - vite
source: custom
enabled: true
---

# Vue 3 Development

## Purpose

Build Vue 3 applications: Composition API, script setup, reactivity boundaries, Pinia state, routing and Vitest component tests.

## When to Use

- You are implementing or refactoring a Vue 3 component or composable.
- Reactivity is not updating, or a watcher loops.
- State must be shared across routes and tested in isolation.

## When NOT to Use

- The codebase is Vue 2 Options API and cannot migrate yet.
- The task is framework-agnostic CSS/layout work.
- You need server-rendering decisions better handled by the Nuxt-specific guidance.

## Capabilities

- Write composables with explicit inputs and outputs instead of hidden state.
- Choose `ref` vs `reactive` vs `shallowRef` deliberately.
- Structure Pinia stores around domain actions rather than arbitrary state.
- Test components with Vitest and Testing Library rather than implementation details.

## Inputs

- Vue version and build tool (Vite, Nuxt, Laravel mix).
- The component tree and where shared state lives.
- The bug report: expected vs actual UI behaviour.

## Workflow

1. Read the component and its store usage to find the reactivity boundary.
2. Prefer `script setup` with typed props and emits.
3. Extract reusable logic into a composable with a single responsibility.
4. Replace ad-hoc event buses with a Pinia action when state is cross-cutting.
5. Cover the behaviour with a component test that fails before the fix.

## Tools

- vite
- vitest + @vue/test-utils
- vue devtools

## Examples

- `npm run test -- --run src/components/OrderTable.spec.ts`
- `npm run build`
- `vue-tsc --noEmit`

## Safety

- Destructuring a `reactive` object loses reactivity; use `toRefs` or `ref`.
- Watchers that write the value they watch create infinite loops.
- Direct DOM access bypasses reactivity; use refs and lifecycle hooks.

## Source

All-Skills canonical library (`skills/web/vue-development`). First-party skill, maintained in this repository.

## Notes

- `v-model` on a custom component needs both prop and emit declared.
- Keep server data in a store, component-local UI state in the component.
- Pairs with: `web/frontend-design`, `development/testing`.
