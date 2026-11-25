---
name: follow-create-nitro-plugin
description: Build Nitro plugins for Nuxt with defineNitroPlugin and hooks
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - follow-create-web
  - follow-lang-typescript
  - run-test
  - deep-review-codebase
  - report

---
## Goal

Build a Nitro plugin package for Nuxt/Nitro with `definePlugin` (v3) / `defineNitroPlugin` (v2), hooks, middleware, storage, and tests

## Scope

Use when creating plugins that extend the Nitro runtime in Nuxt 3/4 or a standalone Nitro project, supporting both project plugins (`server/plugins/`) and npm packages

- Packages: `nitro` (v3 — formerly `nitropack`), `h3` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`); v3 breaking: `defineNitroPlugin` → `definePlugin`, no auto-imports (explicit `nitro/*`), H3 v2 (`defineHandler`, `HTTPError`, `event.req`), Node ≥20
- Nitro v3 breaking changes: package `nitropack` → `nitro`, `defineNitroPlugin` → `definePlugin`, auto-imports removed (explicit imports from `nitro/*` required), H3 v2 (`defineHandler`, `HTTPError`, `event.req` web APIs), Node.js >= 20

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create nitro plugin)
3. Record the rationale for the chosen stack and libraries for future reference (create nitro plugin)

### 2. Choose Plugin Type

> Goal: decide how the plugin will be used

1. For a single project: create `server/plugins/{name}.ts` in the Nuxt project
2. For reuse as a package: create a separate `packages/{plugin-name}/`
3. Define the hooks you need: `render:html`, `request`, `close`, or custom hooks

### 3. Setup Package

> Goal: scaffold the plugin package structure

1. Create `package.json` with `name: nitro-{name}`
2. Put `nitro` (v3) or `nitropack` (v2) in `peerDependencies` per the supported major version
3. Create `tsconfig.json`, `src/index.ts`, `test/plugin.test.ts`
4. Install `unbuild` or `tsup` for the build

### 4. Implement Plugin

> Goal: write the Nitro plugin

1. Create `src/index.ts`:
   - v3: `import { definePlugin } from "nitro"` then `export default definePlugin((nitroApp) => { ... })`
   - v2: `export default defineNitroPlugin((nitroApp) => { ... })`
2. Use `nitroApp.hooks.hook('render:html', (html, { event }) => { ... })` to modify HTML
3. Use `nitroApp.hooks.hook('close', async () => { ... })` for cleanup
4. For storage, call `useStorage()` inside a hook (v3: `import { useStorage } from "nitro/storage"` — auto-imports were removed in v3)

### 5. Register Middleware Or Handlers

> Goal: add middleware or route handlers

1. Use `nitroApp.h3App.use(...)` for global middleware
2. Or create separate `server/middleware/` and `server/routes/` in the Nuxt project
3. Avoid side effects outside the `defineNitroPlugin` callback

### 6. Configure Types

> Goal: support TypeScript types

1. Use types from `nitropack/types` (v2) or `nitro` (v3)
2. If the module needs options, use the `ModuleOptions` type
3. Pass generics through `NitroApp` if needed
4. Declare runtime types with `declare module 'nitropack'` (v2) or `declare module 'nitro'` (v3) when adding custom hooks

### 7. Build Package

> Goal: build the plugin for npm

1. Create `build.config.ts` or `tsup.config.ts` for ESM/CJS
2. Mark `nitro`/`nitropack` as external
3. Run `bun run build`
4. Verify `dist/index.mjs` and `dist/index.d.ts`

### 8. Test

> Goal: test the plugin

1. Create a Nuxt fixture or Nitro fixture
2. Use `await $fetch('/')` via the `setup` of `@nuxt/test-utils`
3. Verify HTML, headers, or storage
4. Run `bun test`

### 9. Ship

> Goal: deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

- Use `definePlugin` from `nitro` (v3) or `defineNitroPlugin` from `nitropack/runtime` (v2)
- The plugin function is synchronous, but hooks may be async
- No global side effects outside the callback
- Call `useRuntimeConfig()` inside hooks, not in the plugin body (v3: `import { useRuntimeConfig } from "nitro/runtime-config"`)
- Declare `nitro` or `nitropack` as a peer dependency per version
- v3: always import utilities explicitly, e.g. `defineHandler` and `HTTPError` from `nitro`; `useDatabase` from `nitro/database`; `defineTask` from `nitro/task`

- Use /follow-create-sdk if needed
- Use /follow-create-web if needed
- Use /follow-create-web-nextjs if needed
- Use /follow-lang-typescript if needed
- Use /run-test if needed
- Use /report if needed

## Expected Outcome

- The Nitro plugin registers hooks
- Middleware or handlers work
- The package builds successfully
- Tests pass
- It can be used in a Nuxt project

