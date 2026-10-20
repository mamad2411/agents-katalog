---
applyTo: "**/*.{vue,ts}"
---

# Vue 3 Coding Standards

## Composition API (Mandatory)

- ALWAYS use `<script setup lang="ts">` — no Options API
- Use `defineProps<T>()` and `defineEmits<T>()` with TypeScript generics
- Use `ref()` for primitives, `reactive()` for complex objects
- Use `computed()` for all derived state — never duplicate state manually
- Use `watch()` / `watchEffect()` sparingly; prefer computed when possible
- Use `defineExpose()` only when component internals must be accessed by parent

## State Management: Pinia

- One store per domain concern (e.g., `useAuthStore`, `useProjectStore`)
- Define stores with the Setup Store syntax (composition style)
- Never mutate store state directly from components — use actions
- Use `storeToRefs()` to destructure store state reactively
- Persist sensitive state in `sessionStorage`, never `localStorage`

## Component Design

- Single File Components: `<script setup>` → `<template>` → `<style scoped>`
- Props are readonly — never mutate props
- Emit events for parent communication; `provide`/`inject` for deep trees
- Keep components under 200 lines; extract composables for logic reuse
- Name components with PascalCase multi-word names (e.g., `UserProfileCard.vue`)
- Prefix base/shared components with `Base` (e.g., `BaseButton.vue`, `BaseModal.vue`)

## TypeScript

- Strict mode enabled; no `any` types
- Define `interface` for all props, emits, and API response shapes
- Use `type` for unions/intersections, `interface` for object shapes
- Export shared types from `src/types/` directory
- Use `as const` assertions for literal types and enums

## API Integration

- Centralized API client in `src/api/client.ts` (axios instance with interceptors)
- One file per API domain in `src/api/` (e.g., `users.ts`, `projects.ts`)
- Composables for data fetching: `useUsers()`, `useProjects()`
- Handle loading/error/data states in every async composable
- Use `AbortController` for request cancellation on component unmount

## Routing

- Lazy-load route components: `() => import('./pages/Dashboard.vue')`
- Use named routes for navigation; never hardcode paths in components
- Route guards in `router/guards/` — separate auth, role, and feature guards
- Use `meta` for route-level metadata (auth required, title, breadcrumbs)

## Styling

- Use `<style scoped>` for component styles; avoid global CSS
- CSS custom properties for theming; no hardcoded colors
- Use CSS Grid for layouts, Flexbox for alignment
- Mobile-first responsive design with `min-width` media queries

## Project Structure

```
frontend/
├── src/
│   ├── api/           # API client and endpoint functions
│   ├── assets/        # Static assets (images, fonts)
│   ├── components/    # Reusable UI components
│   │   └── base/      # Base/shared components
│   ├── composables/   # Shared composition functions
│   ├── layouts/       # Layout wrapper components
│   ├── pages/         # Route-level page components
│   ├── router/        # Vue Router configuration + guards
│   ├── stores/        # Pinia stores
│   ├── types/         # Shared TypeScript interfaces
│   ├── utils/         # Pure helper functions
│   ├── App.vue
│   └── main.ts
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```
