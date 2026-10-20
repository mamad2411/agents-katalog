---
name: follow-lib-vue-migrate-vue2-to-3
description: Migrate Vue 2 → Vue 3 — composition API, breaking changes, incremental build
argument-hint: "[scope]"
related:
  - follow-lib-vue
  - follow-lib-pinia
  - follow-lib-vueuse
  - deep-analyze
  - use-astgrep
  - deep-review-codebase
  - report-before-after
---

## Goal

Migrate a Vue 2 application to Vue 3 safely — options→composition, breaking changes (filters, `$emit`, `v-model`), and incremental migration

## Scope

Use when migrating a Vue 2 codebase to Vue 3 — covers the migration plan, build config, API changes, and incremental strategy (must be rollback-able, not done alongside feature work)

## Execute

### 1. Plan Migration

> Goal: identify from→to, impact, and the rollback path before starting

1. Read the official migration guide at `https://v3-migration.vuejs.org` — identify every breaking change that affects the codebase
2. Do `/deep-analyze` and `/scan-codebase` — map the places using Vue 2 APIs: filters, `$listeners`, `$children`, the old `v-model`, event bus, `Vue.extend`
3. Write a clear rollback path — split migration commits per step so it's bisectable
4. If the scope isn't clear → stop and report

### 2. Upgrade Build And Dependencies

> Goal: migrate config → deps before code

1. Upgrade `vue` to v3 and `@vue/compat` (the migration build) if you need incremental
2. Upgrade the ecosystem: `vue-router` 4, `pinia` (instead of Vuex) or `vuex` 4, and the build tool to Vite
3. Set the compat config `compatConfig: { MODE: 3 }` and per-feature flags according to the warnings
4. Separate commits: deps/config → don't mix with code changes

### 3. Migrate Code Patterns

> Goal: convert Vue 2 APIs to Vue 3 one pattern at a time

1. Options → Composition: convert `data`/`methods`/`computed`/`watch` to `<script setup>` + `ref`/`computed`/`watch` — do it one component at a time or use a codemod (`/use-astgrep`, `/migration-with-astgrep`)
2. Main breaking changes:
   - Filters are removed — convert `{{ x | filter }}` to a method/computed
   - `v-model`: a `modelValue` prop + an `update:modelValue` event instead of `value`/`input`; `.sync` → `v-model:propName`
   - `$listeners` merges into `$attrs` — the component uses an `emits` declaration
   - `$emit` → `defineEmits()` in setup
   - Event bus → use an external emitter (e.g. `mitt`) or Pinia
   - `Vue.use`/`Vue.mixin`/`Vue.component` → `app.*` APIs on the `createApp` instance
3. Global API: `new Vue()` → `createApp(App)`, mount with `app.mount('#app')`

### 4. Remove Compat And Finalize

> Goal: turn off compat mode once the warnings are gone

1. Fix all compat warnings first — gradually flip the feature flags to 3
2. Remove `@vue/compat` when there are no warnings left
3. Do `/deep-review-codebase` to check for leftover Vue 2 APIs

### 5. Verify

> Goal: lint/typecheck/tests and a runtime smoke test pass

1. Run all lint, typecheck, and tests
2. Runtime smoke test every main route/feature
3. If anything is left → create a clear TODO list; when done → `/report-before-after`, then report

## Rules

- Incremental only — use `@vue/compat` for a large codebase, never a big-bang rewrite
- Separate commit per step — never mix migration with feature work
- Use codemods/ast-grep instead of manual edits when available
- The Composition API is the final target — any remaining Options API during migration must have a plan
- Use `/follow-lib-vue` for the Vue 3 target standards

## Expected Outcome

- The application runs on Vue 3 with no compat warnings
- Vue 2 APIs (filters, `$listeners`, event bus, `.sync`) are fully converted
- Tests/lint/typecheck all pass
- Migration commits are cleanly separated and bisectable
