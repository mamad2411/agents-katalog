---
name: follow-lib-vue
description: Vue 3.5+ application development guidelines per 2026 best practices
argument-hint: "[scope]"
related:
  - follow-lib-animejs
  - follow-lib-arktype
  - follow-lib-better-auth
  - follow-lib-pinia
  - follow-lib-vueuse
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Define guidelines for developing Vue.js applications with Vue 3.5+, the Composition API, TypeScript, and modern best practices

## Scope

For Vue 3 projects on either Vite 8 or Nuxt 4 (Vue 3.5.43 is the latest stable, Vue 3.6 is still in RC — `3.6.0-rc.8`)

- Latest: `vue@3.5.43` / `vue-router@5.3.1` / `pinia@4.0.3` / `vite@8.3.1` / `nuxt@4.5.2` (verified 2026-09-26)

## Execute

### 1. Setup And Configuration

> Goal: set up a Vue 3 project with the necessary dependencies and tools

1. Install Vue 3.5.42+ with Vite 8 or Nuxt 4.5+
2. Use TypeScript strict mode
3. Install Pinia 4 for state management
4. Install Vue Router 5 for routing
5. Install UnoCSS or Tailwind CSS for styling
6. Use Vite 8 as the build tool
7. Consider Vue 3.6 RC for Vapor Mode in cases with critical performance testing (not yet stable for production)
8. See additional details in the references

### 2. Component Development

> Goal: write Vue components per the Composition API standards

1. Use Single-File Components (SFC) with `<script setup lang="ts">`
2. Use the Composition API instead of the Options API (the Options API is legacy)
3. Always use multi-word component names
4. Declare prop types with `defineProps<T>()`
5. Use `defineEmits<T>()` for type-safe events
6. Always use a key with v-for
7. Use `useTemplateRef()` for template refs (Vue 3.5+)
8. Use `useId()` for SSR-safe unique IDs (Vue 3.5+)
9. Use `defineModel()` for two-way binding
10. Use `defineSlots<T>()` for type-safe slots

### 3. Composables And State

> Goal: organize logic and state with composables and Pinia

1. Move logic out of components into composables
2. All logic should live in composables
3. Use Pinia 4 for global state management
4. Organize stores by features/domains
5. Use computed getters for derived state
6. Use shared composables for local/branch-level state instead of creating a Pinia store
7. Use `provide`/`inject` with `InjectionKey<T>` for dependency injection
8. Use `effectScope` to clean up reactive effects in complex composables

### 4. Reactivity Best Practices

> Goal: use Vue reactivity efficiently

1. Use `shallowRef()` for large immutable data structures (saves memory)
2. Use `ref()` for primitive values
3. Use `reactive()` for object state that needs deep reactivity
4. Use `computed()` for derived values
5. Avoid creating unnecessary watchers (zombie effects)
6. Use `watchEffect` only when you want auto dependency tracking
7. Use `watch` when you want explicit dependency specification
8. Use `onWatcherCleanup()` and `onEffectCleanup()` for cleanup (Vue 3.5+)

### 5. Vapor Mode (Vue 3.6+)

> Goal: consider Vapor Mode for better performance

1. Use the `vapor` attribute in `<script setup>` to opt in to Vapor Mode (Vue 3.6+)
2. Or use the `.vapor.vue` file extension to opt in without editing the script
3. Start from leaf components (list items, table rows, icon buttons) first
4. Mixed trees work: a vdom parent can render Vapor children
5. Vapor Mode supports only the Composition API (not the Options API)
6. `Suspense` isn't yet supported in Vapor-only mode
7. Use Vue 3.6 RC only, and test before using it in production

### 6. Styling

> Goal: define component styles with the design system

1. Use the defined UnoCSS theme
2. Don't hard-code colors or spacing
3. Use utility classes instead of custom styles
4. Use `<style scoped>` for component-specific styles when necessary

### 7. Project Organization

> Goal: organize the project structure and conventions

1. Refactor reused components into `components/ui/`
2. Use import aliases (`~/`, `#app`, `#shared`) and avoid relative paths
3. Every `index.ts` only re-exports — no logic
4. Remove all `@deprecated` from the codebase
5. Use `useHead` in every page component for meta tags
6. Use `useSeoMeta` for declarative SEO meta tags

### Workflows

- Migrate Vue 2 → Vue 3 — options→composition, breaking changes, `@vue/compat` → `workflows/migrate-vue2-to-3/SKILL.md`

## Rules

### 1. Component Standards

- Use only the Composition API and `<script setup>` (required for Vapor Mode)
- Use TypeScript for type safety
- Component names are multi-word
- Props must have detailed definitions via `defineProps<T>()`
- Always use a key with v-for
- Avoid v-if with v-for on the same element
- Use `useTemplateRef()` instead of `ref` for template refs (Vue 3.5+)

### 2. Code Organization

- Move logic out of components into composables
- All logic should live in composables
- Reused components must live in `components/ui/`
- Use import aliases and avoid relative paths
- Every `index.ts` only re-exports — no logic
- Remove all `@deprecated` from the codebase

### 3. State Management

- Use Pinia 4 for global state management
- Organize stores by features/domains
- Use computed getters for derived state
- Use shared composables for local/branch-level state
- Use `InjectionKey<T>` for type-safe provide/inject

### 4. Reactivity

- Use `shallowRef()` for large immutable data structures
- Use `ref()` for primitive values
- Avoid zombie effects with `effectScope`
- Avoid unnecessary watchers
- Use `onWatcherCleanup()`/`onEffectCleanup()` for cleanup (Vue 3.5+)

### 5. Styling

- Use the defined UnoCSS theme
- Don't hard-code colors or spacing
- Styles are scoped when necessary

### 6. Performance

- Use computed properties efficiently
- Use `shallowRef` for large data to save memory
- Avoid unnecessary reactivity
- Use dynamic imports for lazy loading
- Consider Vapor Mode for component-heavy scenarios (Vue 3.6 RC)
- Use tree-shaking to its fullest

- Use `/follow-lib-animejs` if needed
- Use `/follow-lib-arktype` if needed
- Use `/follow-lib-better-auth` if needed
- Use `/follow-lib-pinia` if needed
- Use `/follow-lib-vueuse` if needed
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Vue 3 components structured correctly per the Composition API
- Logic separated from components into composables
- Reactivity using `shallowRef` for large data
- Better performance with Vapor Mode (if using Vue 3.6+)
- Full type safety with TypeScript
- Maintainable code
