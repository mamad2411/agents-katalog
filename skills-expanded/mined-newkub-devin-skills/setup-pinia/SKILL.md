---
name: follow-lib-pinia-setup-pinia
description: Install Pinia — createPinia, store patterns (setup vs options)
argument-hint: "[scope]"
related:
  - follow-lib-pinia
  - follow-lib-vue
  - run-install
  - run-test
  - resolve-errors
---

## Goal

Install and configure Pinia in a Vue 3 project — `createPinia`, store definition, and picking the setup vs options store pattern

## Scope

Use when setting up Pinia for the first time in a Vue 3 or Nuxt project — covers install, `createPinia`, `app.use(pinia)`, `defineStore` patterns, and a smoke test

## Execute

### 1. Install Pinia

> Goal: install Pinia and its peer dependencies

1. Install `bun add pinia` and `bun add -D @vue/devtools-api` (the peer dependency Pinia v4 requires)
2. For Nuxt: `bun add -D @pinia/nuxt` or `bunx nuxi@latest module add pinia`
3. If `package.json` already has pinia → verify the version only (idempotent)
4. Create a `stores/` directory for store files
5. Remember that Pinia v4 is ESM-only and requires TypeScript 5+

### 2. Create Pinia Instance

> Goal: create and mount the pinia instance

1. `const pinia = createPinia()` at the entry point (`main.ts`)
2. `app.use(pinia)` before `app.mount()`
3. Nuxt: add `@pinia/nuxt` to `modules` in `nuxt.config.ts` — the instance is auto-provided
4. Set `pinia.storesDirs` in Nuxt if the store directory isn't the default

### 3. Define First Store

> Goal: create the first store with the setup pattern

```ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubled = computed(() => count.value * 2)
  function increment() { count.value++ }
  return { count, doubled, increment }
})
```

1. Prefer the setup function pattern: `defineStore('id', setupFn)`
2. `ref`/`reactive` = state, `computed` = getters, functions = actions
3. Return only the members that need to be exposed
4. The options store `defineStore('id', { state, getters, actions })` works too, but the setup pattern is recommended for new projects — use options when aligning with an existing codebase

### 4. Use Store In Component

> Goal: access the store while preserving reactivity

1. Call `useCounterStore()` in `<script setup>` or a composable
2. Use `storeToRefs(store)` when destructuring state/getters — never destructure directly or reactivity breaks
3. Call actions on the store instance directly

### 5. Verify

> Goal: confirm the store behaves correctly

1. Run `/run-test` — write tests with `setActivePinia(createPinia())` in `beforeEach`
2. Run dev — state changes and the UI react correctly
3. If it breaks → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Create one pinia instance, at the entry point only
- Prefer the setup store pattern — options stores only to align with an existing codebase
- Use `storeToRefs` when destructuring — never destructure state directly
- Split stores by domain/feature — don't put everything in one store
- Use `/follow-lib-pinia` for the full reference and persistence/testing

## Expected Outcome

- Pinia installed and mounted correctly in Vue/Nuxt
- The first store works with the setup pattern, with state/getters/actions
- Components access the store while keeping reactivity
- Tests pass with `setActivePinia`
