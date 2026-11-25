---
name: nuxt-skills
description: Nuxt.js framework patterns, SSR/SSG, and best practices
category: stacks/frontend/nuxt
applies_to: nuxt
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Nuxt.js Skills

Vue.js framework for hybrid static & server rendering.

## Sub-Skills

### Architecture
- [project-structure.md](architecture/project-structure.md) - Project organization
- [modules.md](architecture/modules.md) - Nuxt modules
- [plugins.md](architecture/plugins.md) - Plugin patterns

### Rendering
- [universal.md](rendering/universal.md) - Universal rendering
- [ssr.md](rendering/ssr.md) - Server-side rendering
- [ssg.md](rendering/ssg.md) - Static generation
- [hybrid.md](rendering/hybrid.md) - Hybrid rendering

### Data Fetching
- [useFetch.md](data-fetching/useFetch.md) - useFetch composable
- [useAsyncData.md](data-fetching/useAsyncData.md) - useAsyncData
- [server-routes.md](data-fetching/server-routes.md) - Server routes

### Routing
- [file-routing.md](routing/file-routing.md) - File-based routing
- [middleware.md](routing/middleware.md) - Route middleware
- [layouts.md](routing/layouts.md) - Layout patterns
- [navigation.md](routing/navigation.md) - Navigation patterns

### State Management
- [pinia.md](state/pinia.md) - Pinia integration
- [composables.md](state/composables.md) - State composables

### Performance
- [lazy-loading.md](performance/lazy-loading.md) - Component lazy loading
- [image-optimization.md](performance/image-optimization.md) - nuxt/image
- [caching.md](performance/caching.md) - Caching strategies

### Authentication
- [nuxt-auth.md](authentication/nuxt-auth.md) - Nuxt Auth
- [middleware-auth.md](authentication/middleware-auth.md) - Auth middleware

### Testing
- [vitest.md](testing/vitest.md) - Vitest patterns
- [e2e.md](testing/e2e.md) - E2E testing

## Detection
Auto-detected when project contains:
- `nuxt.config.ts` or `nuxt.config.js`
- `nuxt` package
- `defineNuxtConfig` or `useNuxtApp` patterns
