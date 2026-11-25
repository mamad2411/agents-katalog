---
name: follow-create-web-nuxt
description: Create or improve Nuxt 4 projects with Universal Rendering and Nitro
argument-hint: "[scope]"
related:
  - follow-create-web
  - follow-create-mobile
  - follow-best-practice
  - setup-cicd
  - deep-review-codebase
  - follow-lib-vue
  - run-dev
---

## Goal

Define guidelines for developing Nuxt 4 applications at peak performance

## Scope

Covers setup, directory structure, configuration, code standards, performance, plugins, assets, error handling, and verification for Nuxt 4 projects (Nuxt 3 EOL July 2026)

- Packages: `nuxt` 4.x (Node `^22.19.0 || ^24.11.0 || >=26.0.0`, Vue 3.5+, the Nitro server engine builds `.output` deployable to Node/serverless/edge), `nuxi` CLI, `@nuxt/ui` 4.x (Reka UI + Tailwind CSS + Tailwind Variants — run `bun add @nuxt/ui tailwindcss`, then `@import "tailwindcss"; @import "@nuxt/ui";` in `app/assets/css/main.css`) — always verify the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`)

## Execute

### 1. Setup

> Goal: Plan the project architecture

1. Identify the project location in the monorepo, e.g. `apps/web/`
2. Use Nuxt 4.x (Nuxt 3 EOL July 2026 — use Nuxt 4 only for new projects; Nuxt 4 uses the `app/` dir, Nuxt 3 uses root-level `pages/` `components/` `composables/`)
   - Scaffold with `bunx nuxi@latest init <project-name>` — add modules with `bunx nuxi@latest module add <name>`; nuxi supports `dev`, `build`, `generate`, `preview`, `analyze`, `prepare`, `typecheck`, `add`, `upgrade`, `cleanup`, `info`, `devtools`
3. Choose the Rendering Mode: SSR (default), SSG (`nuxt generate`), CSR (`ssr: false`), or Hybrid via `routeRules`
4. Decide whether a Database is needed (e.g. Drizzle ORM)
5. Pick the UI Framework: UnoCSS, Tailwind, or others
6. Define the Architecture: whether to use Layers and Modules
7. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns (docs: https://nuxt.com/docs)

### 2. Directory Structure

> Goal: Create the folder structure

1. Use the `app/` directory for Nuxt 4 (`app/pages/`, `app/components/`, `app/composables/`) plus `public/`, `server/`, `shared/`, `layers/`
2. Create `layers/` for feature-based architecture
3. Group components and composables by feature within each layer
4. Use auto-imports: `ref`, `computed`, `watch`, `useFetch`, `useAsyncData`, `useState`, `useHead`, `useStorage`, `navigateTo`, `useRoute`, `useRouter`, `useRuntimeConfig`, `useRequestFetch`, `defineNuxtPlugin`, `defineNuxtRouteMiddleware` — components in `app/components/` are auto-imported with a path prefix
5. Separate business logic into services and repositories under `server/` — Nitro conventions: `server/api/*`, `server/routes/*` (`defineEventHandler`, `[id].ts` dynamic params), `server/middleware/*`, `server/plugins/*` (`defineNitroPlugin`)

### 3. Configuration

> Goal: Set up config and scripts

1. Set up `nuxt.config.ts` (extends, modules, nitro, typescript)
2. Set up `package.json` scripts (build, dev, generate, lint, format, test)
3. Set up `tsconfig.json` with strict mode
4. Create barrel exports for every folder
5. Define the data flow: Pages → Components → Composables → Stores → API → Services → Repositories → DB

### 4. Code Standards

> Goal: Define coding standards

1. Vue components: use `script setup lang="ts"`, script above the template (see `/follow-lib-vue` for Vue standards)
2. Composables: names start with `use`, placed in `composables/` or `layers/[feature]/composables/`
3. Server API: use `defineEventHandler` or `defineNitroPlugin`
4. Types: no `any`, define clear types in `shared/types/`
5. Import: auto-import for Nuxt built-ins, barrel exports for shared code
6. Icons: use `@nuxt/icon` with the `mdi` preset only, never raw SVG
7. Components: import shared UI components only from `components/ui/`
8. Barrel Exports: every `index.ts` only re-exports, no logic
9. Deprecated: remove all `@deprecated` code, keep none in the codebase
10. SEO: use `useHead` in every page component for meta tags

### 5. Development

> Goal: Build the base project

1. Create the directory structure as planned
2. Install dependencies with `bun add`
3. Create base components, layouts, and composables
4. Create the server layer (API routes, services, repositories)
5. Create layers for each feature (if used)

### 6. Performance

> Goal: Tune performance

1. Lazy Loading Components — use the `Lazy` prefix for components that don't need to load immediately
   ```vue
   <!-- Bad: loads immediately -->
   <Modal v-if="showModal" />

   <!-- Good: loads when needed -->
   <LazyModal v-if="showModal" />
   ```
2. Lazy Hydration — use `hydrate-on-visible` for components that don't need to be interactive immediately
   ```vue
   <LazyMyComponent hydrate-on-visible />
   ```
3. Hybrid Rendering — use route rules for mixed rendering
   ```typescript
   export default defineNuxtConfig({
     routeRules: {
       '/': { prerender: true },
       '/products/': { swr: 3600 },
       '/blog': { isr: 3600 },
       '/admin/': { ssr: false },
     },
   })
   ```
4. NuxtLink Smart Prefetching — use `<NuxtLink>` instead of `<a>` tags everywhere
   ```vue
   <NuxtLink to="/about">About page</NuxtLink>
   ```
5. Data Fetching Optimization — use `useFetch` and `useAsyncData` with a key parameter
   ```typescript
   const { data } = useAsyncData('tracks', () => fetch(`/tracks/${id}`))
   ```
6. Built-in Storage — use `useStorage` for key-value storage
   ```typescript
   const storage = useStorage()
   await storage.setItem('session:token', sessionToken)
   ```

### 7. Plugins Best Practices

> Goal: Set up Nuxt plugins

1. Avoid costly plugin setup - avoid plugins with heavy computation or long initialization time
2. Use Composition whenever possible - use composables instead of plugins when feasible
3. Enable parallel for async plugins - use `true` for async plugins
   ```typescript
   export default defineNuxtPlugin({
     parallel: true,
     async setup() {
       // async initialization
     }
   })
   ```

### 8. Assets Management

> Goal: Manage assets

1. Use `~/assets` for files that need processing
   ```typescript
   import image from '~/assets/image.png'
   ```
2. Use `~/public` for files that don't need processing
   ```vue
   <img src="/image.png" />
   ```
3. `/assets` checks for missing files at build time

### 9. Error Handling

> Goal: Set up error boundaries

1. Use `NuxtErrorBoundary` to handle errors in different parts of the app
   ```vue
   <NuxtErrorBoundary>
     <NuxtPage />
     <template #error="{ error }">
       <p>Oh no, something broke!</p>
       <button @click="clearError(error)">Retry</button>
     </template>
   </NuxtErrorBoundary>
   ```

### 10. Verification

> Goal: Check quality

1. Run `nuxt typecheck` to check TypeScript errors
2. Run Biome and oxlint to check code quality
3. Run `nuxt build` and `nuxt generate` to confirm the build passes
4. Test that the dev server runs without errors
5. Verify that HMR and auto-imports work correctly

## Rules

### 1. Directory Conventions

- Use the `app/` directory for Nuxt 4
- Create `layers/` for feature-based architecture

### 2. Vue Components

- Vue components must use `script setup lang="ts"` only
- Composables must have the `use` prefix
- Use `<NuxtLink>` instead of `<a>` tags everywhere

### 3. Types And Imports

- Never use `any`
- Use barrel exports for every folder
- Use auto-imports for Nuxt built-ins
- No relative paths in cross-layer imports; use default import aliases (`~/`, `#server`, `#shared`)
- Every `index.ts` only re-exports, no logic

### 4. UI And Assets

- Use `@nuxt/icon` with the `mdi` preset for all icons — pick modules from the official catalog https://nuxt.com/modules, templates from https://ui.nuxt.com/templates
- Reusable components must be imported from `components/ui/`
- Use `~/assets` for processed files
- Use `~/public` for static files

### 5. Code Quality

- Remove all `@deprecated` items from the codebase
- Use `useHead` in every page component for SEO meta tags
- Use the `Lazy` prefix for lazy loading
- Avoid costly plugins

- Use /follow-create-mobile-cross-with-capacitor if needed (create web nuxt)
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /deep-review-codebase if needed
- Use /run-dev if needed

## File Structure

Canonical file structure + layer table: [templates/file-structure-web-nuxt.md](templates/file-structure-web-nuxt.md)

## Expected Outcome

- A correctly structured Nuxt 4 project
- Well-organized Layers and Modules
- Type-safe code with TypeScript
- Improved performance
- All builds and tests passing
- Solid error handling
- Correct assets management
