---
name: follow-lib-pinia
description: Guidelines for using Pinia v4 for state management in Vue 3
argument-hint: "[scope]"
related:
  - follow-lib-vue
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Define guidelines for using Pinia v4 for state management in Vue 3 efficiently and to a standard

## Scope

Use with Vue 3 that needs state management via Pinia v4 — covers setup stores, getters, actions, persistence, and testing

- No own CLI — used via the Vue app/Nuxt module (thus none)
- Latest: `pinia@4.0.3` / `@pinia/nuxt@1.0.2` / `pinia-plugin-persistedstate@4.7.1` (verified 2026-09-13)
- References: [apis](references/apis.md) 
## Execute

### 1. Install Pinia

> Goal: install Pinia v4 in a Vue or Nuxt project

1. Install `pinia` with `bun add pinia`
2. Install `@vue/devtools-api` since Pinia v4 requires this peer dependency
3. For Nuxt, install `@pinia/nuxt` with `bun add -D @pinia/nuxt` or `bunx nuxi@latest module add pinia`
4. Create a `stores/` directory to hold store files
5. Remember that Pinia v4 is ESM-only

### 2. Create Pinia Instance

> Goal: create and configure the Pinia instance

1. Use `createPinia()` to create the instance
2. Install it in the Vue app with `app.use(pinia)`
3. For Nuxt, add `@pinia/nuxt` to `modules` in `nuxt.config.ts`
4. Configure `pinia.storesDirs` in Nuxt if the store directory isn't in the default location

### 3. Define Setup Store

> Goal: design stores with the Composition API style

1. Use the setup function pattern as the primary: `defineStore('id', setupFn, options?)`
2. Clearly define state, getters, and actions
3. Use `ref`, `reactive`, `computed` for state and getters
4. Use arrow functions for actions
5. Split stores by domain/feature with meaningful names

### 4. Implement State, Getters And Actions

> Goal: manage state, derived state, and side effects

1. Use `ref` or `reactive` for state
2. Create getters with `computed`
3. Implement actions for async logic using `async/await`
4. Use `$patch` for batch state updates
5. Avoid mutating state outside actions

### 5. Use Stores In Components

> Goal: access stores in components while preserving reactivity

1. Use `storeToRefs` when destructuring reactive state
2. Access stores in `<script setup>` components
3. Call actions directly through the store instance
4. Use `$subscribe` or `$onAction` for subscriptions if needed

### 6. Add Persistence (Optional)

> Goal: configure the persisted state plugin to keep state across sessions

1. Install `pinia-plugin-persistedstate`
2. Define persist strategies with `pick` and `serializer`
3. Choose the fields to persist
4. Handle serialization and SSR compatibility

### 7. Test Stores

> Goal: test stores with Vitest and `setActivePinia`

1. Write unit tests for stores with Vitest
2. Use `setActivePinia(createPinia())` in `beforeEach`
3. Test actions, getters, and state changes
4. Mock external dependencies appropriately

### Workflows

- Install + `createPinia` + store patterns (setup vs options) → `workflows/setup-pinia/SKILL.md`

## Rules

### 1. Setup Store Pattern

- Use the setup function pattern as the primary (option stores not recommended for new projects)
- Use arrow functions for actions
- Return only the necessary state and members
- Use `const` for store definitions

### 2. State Naming

- Use descriptive names for state properties
- Avoid generic names like `data`, `value`
- Use the `isLoading`, `hasError` pattern for async states
- Group related state together

### 3. Action Conventions

- Use `async/await` for async actions
- Handle errors completely
- Return values from actions when appropriate
- Don't mutate state outside actions

### 4. Getters Usage

- Use getters for derived state
- Avoid duplicate computations
- Pass parameters via closure if needed
- Cache expensive computations with `computed`

### 5. Pinia v4 Requirements

- Pinia v4 requires installing `@vue/devtools-api` yourself
- Pinia v4 is ESM-only
- Use TypeScript 5 or newer
- `defineStore({ id })` and `PiniaStorePlugin` are not supported (removed in v3/v4)

### 6. Nuxt Integration

- Use `@pinia/nuxt` v1.0+ for Nuxt 3/4
- Configure `pinia.storesDirs` if needed
- Use auto-imports for `defineStore` and `storeToRefs`

### 7. Testing

- Use `setActivePinia(createPinia())` before each test
- Mock API calls in actions
- Verify reactivity after state changes
- Test edge cases

- Use `/follow-lib-vue` if needed
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Well-structured Pinia v4 stores
- Predictable state management
- Type-safe store usage
- Tested store logic
- Documentation for store patterns
