# Nuxt Skill

You are working on a Nuxt 3 project. Apply these conventions.

## Project Structure

- Pages live in `pages/` — file-based routing is automatic.
- Shared components in `components/` are auto-imported, no explicit imports needed.
- Composables in `composables/` and utils in `utils/` are also auto-imported.
- Server routes live in `server/api/` and `server/routes/`.
- Static assets go in `public/`; processed assets go in `assets/`.

## Data Fetching

- Use `useFetch('/api/…')` or `useAsyncData('key', () => $fetch('…'))` in pages/components.
- These composables are SSR-aware: they run on server, then hydrate on client without double-fetching.
- Use `$fetch` inside server routes and event handlers — never use `useFetch` server-side outside composables.
- Use `lazy: true` option in `useFetch` to defer loading and avoid blocking navigation.
- Call `refreshNuxtData('key')` to manually invalidate cached data.

## Server Routes

- Create server endpoints in `server/api/[name].ts` — export a default `defineEventHandler(async (event) => { … })`.
- Use `readBody(event)` for POST bodies, `getQuery(event)` for query params, `getRouterParam(event, 'id')` for route params.
- Use `createError({ statusCode: 404, statusMessage: 'Not Found' })` for HTTP errors.

## State & Composables

- Use `useState('key', () => defaultValue)` for SSR-safe shared state.
- Create composables that return reactive refs for shared logic across components.
- Use `useRuntimeConfig()` to access environment variables — server-only vars under `.runtimeConfig`, public under `.runtimeConfig.public`.

## Auto-imports & TypeScript

- Run `nuxi prepare` to regenerate `.nuxt/` type declarations after adding new composables or components.
- Prefix component names to avoid conflicts: `TheHeader.vue`, `AppButton.vue`.
- Types for pages are in `.nuxt/types/`; use `NuxtPage`, `NuxtLayout`, etc.

## nuxt.config.ts

- Configure modules in `modules: []`; they auto-register plugins and composables.
- Use `runtimeConfig` for environment variables; never hardcode secrets.
- Use `routeRules` for per-route rendering strategies (SSR, SWC, prerender, ISR).
