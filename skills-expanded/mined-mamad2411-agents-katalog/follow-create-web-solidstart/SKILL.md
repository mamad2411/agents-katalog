---
name: follow-create-web-solidstart
description: "Build SolidStart SSR apps via nitro/vite — streaming HTML, assets, hydration"
argument-hint: "[project-name]"
related:
  - follow-lib-solidjs
  - follow-create-plugins
  - follow-tool-vite
  - use-bun-native-api
  - follow-create-web
  - deep-review-codebase
  - run-dev

---

## Goal

Build a SolidStart application that does SSR through the Vite plugin `nitro/vite`, following the nitro.build example `vite-ssr-solidstart`, to get streaming HTML, asset management, and client hydration

## Scope

Use for creating SolidStart (SolidJS meta-framework) projects that use Vite as the build tool and Nitro as the server engine via `@solidjs/start` v2 + `nitro` v3 — see https://nitro.build/examples/vite-ssr-solidstart

- Packages: `@solidjs/start`, `@solidjs/router`, `@solidjs/meta`, `solid-js`, `nitro` (v3 has the `nitro/vite` plugin), `vite` — always verify the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Confirm the stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Confirm the use of SolidJS + SolidStart + Nitro + Vite
3. Follow `/follow-lib-solidjs` for component patterns

### 2. Setup Project

> Goal: Create the project structure and install dependencies

1. Create `package.json` with `"type": "module"` and the scripts `dev: "vite dev"`, `build: "vite build"`
2. Install dependencies with `bun add @solidjs/start @solidjs/router @solidjs/meta solid-js nitro vite` (`@solidjs/start` 2.x is stable — no need for `@alpha`; `nitro` v3 ships the `nitro/vite` plugin — check the latest version with `/deep-research`)
3. Set `engines.node >= 22`

### 3. Configure Vite And TypeScript

> Goal: Configure `vite.config.ts` and `tsconfig.json`

1. Create `vite.config.ts` with the `solidStart()` plugin from `@solidjs/start/config` and `nitro()` from `nitro/vite`
2. Configure `tsconfig.json` with `jsx: "preserve"`, `jsxImportSource: "solid-js"`, `moduleResolution: "bundler"`, `strict: true`
3. Add `types: ["@solidjs/start/env"]` and the path alias `"~/*": ["./src/*"]`

### 4. Create App Shell

> Goal: Create the app component that runs on both server and client

1. Create `src/app.tsx` with `Router` from `@solidjs/router` and `FileRoutes` from `@solidjs/start/router`
2. Wrap the root with `MetaProvider` + `Title` from `@solidjs/meta` and `Suspense`
3. Create `src/app.css` for global styles

### 5. Create Server And Client Entries

> Goal: Create entry points for SSR and hydration

1. Create `src/entry-server.tsx` with `createHandler` + `StartServer` from `@solidjs/start/server` — render the document shell with `assets`, `children`, and `scripts`
2. Create `src/entry-client.tsx` with `mount` + `StartClient` from `@solidjs/start/client` — hydrate at `#app`
3. Put `// @refresh reload` on the first line of both entries

### 6. Create Routes

> Goal: Create file-based routes

1. Create `src/routes/index.tsx` for the home page
2. Create `src/routes/[...404].tsx` for the catch-all with `HttpStatusCode` from `@solidjs/start`
3. Use `Title` from `@solidjs/meta` in every route

### 7. Run And Verify

> Goal: The dev server and build work

1. Run `bun run dev` (or `vite dev`) and open the browser to check the SSR HTML
2. Run `bun run build` to produce the production output via Nitro — the output lands in `.output/` and runs with `bun .output/server/index.mjs`
3. Verify hydration works (view-source shows server-rendered HTML)

## Rules

### 1. Entry Points

- `src/entry-server.tsx` must export `createHandler(() => <StartServer ... />)`
- `src/entry-client.tsx` must call `mount(() => <StartClient />, document.getElementById("app")!)`
- Put `// @refresh reload` on the first line of every entry file

### 2. Plugins

- Always use `nitro()` from `nitro/vite` in `vite.config.ts` — Nitro serves as the server engine
- Use `solidStart()` from `@solidjs/start/config` together with `nitro()`
- Never add dev server middleware outside Nitro hooks — see `/follow-create-nitro-plugin`

### 3. SolidJS Patterns

- Follow `/follow-lib-solidjs` for reactivity (`createSignal`, `createStore`, `createResource`)
- Use `FileRoutes` for file-based routing; don't hand-build route config
- Always use `Suspense` in the root layout

### 4. Bun Native APIs

- Always use Bun as the package manager and script runner (`bun install`, `bun run dev`, `bun run build`)
- If you must write your own server code outside Nitro (e.g. scripts, tools) → use Bun native APIs per `/use-bun-native-api` (`Bun.serve`, `Bun.file`, `Bun.spawn`, `$` shell)
- The Nitro production output runs directly with Bun (`bun .output/server/index.mjs`)

### 5. Safety

- Never commit secrets to the repository — use environment variables
- If there are destructive changes → dry run first

- Use /follow-lib-solidjs if needed
- Use /follow-create-web if needed
- Use /follow-tool-vite if needed
- Use /follow-create-nitro-plugin if needed
- Use /deep-review-codebase if needed
- Use /use-bun-native-api if extra Bun APIs work are needed
- Use /run-dev if needed
- Use /follow-create-plugins if needed


## Expected Outcome

- A SolidStart + Nitro SSR project that runs a dev server and builds
- SSR streaming HTML works and client hydration succeeds
- File-based routing with a 404 catch-all route
- TypeScript strict mode with the `~/*` alias
