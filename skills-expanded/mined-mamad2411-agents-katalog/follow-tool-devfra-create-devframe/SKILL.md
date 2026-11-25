---
name: follow-tool-devfra-create-devframe
description: Scaffold a new devtool with Devframe — install, defineDevframe, RPC, SPA, run dev/build/mcp
argument-hint: "[tool-id]"
related:
  - follow-tool-devfra
  - follow-lib-zod
  - follow-create-cli
  - run-check
  - resolve-errors
  - suggest-next-action
---

## Goal

Scaffold a new devtool with Devframe until it really runs — `my-tool` dev server, `build` static, `mcp` agent — first-time setup only

## Scope

- Use when the project has no `DevframeDefinition` yet (if present → verify only)
- Covers: install, definition, RPC function, SPA wiring, cac CLI entry
- Does not cover hub composition, framework kits (`@devframes/vite|nuxt|next` hosting), or embedded — see the parent `SKILL.md`

## Execute

### 1. Check Precondition

> Goal: check the environment before scaffolding

1. Read `package.json` — if `devframe` is already there → skip to verify; check the version against the parent SKILL.md `### 4. Version Notes`
2. Identify the SPA stack to use (Vue/Nuxt/React) and the runtime (Bun/Node)
3. If the project is a brand-new CLI → do `/follow-create-cli` for the skeleton first

### 2. Install

> Goal: install the minimal packages

1. Run `bun add devframe cac` — `cac` is the CLI adapter's optional peer
2. Run `bun add valibot` (or `zod` — do `/follow-lib-zod`) for RPC schemas
3. Confirm all of them are in `dependencies`

### 3. Write Definition And RPC

> Goal: `defineDevframe` + 1 callable RPC function

1. Create `src/rpc.ts` with `defineRpcFunction` — `type: 'query'`, declare the `args`/`returns` schemas
2. Create `src/cli.ts` with `defineDevframe({ id, name, version, packageName, importMetaUrl, homepage, description, icon, clientAssets, cli, setup })`
3. In `setup(ctx)` → `const my = ctx.scope('<id>')` then `my.rpc.register(fn)`
4. Source `version`/`packageName`/`homepage`/`description` from `package.json` (`import pkg from '../package.json' with { type: 'json' }`)
5. Set `cli: { command: '<id>', port, open: true }` — `open` embeds the OTP so the tab arrives authenticated

### 4. Wire SPA

> Goal: `clientAssets` points at the real built UI

1. Build the SPA and point `clientAssets` at the output — Nuxt: `modules: ['@devframes/nuxt/single']`, `ssr: false`, nitro `preset: 'static'`; Next: `output: 'export'`, `assetPrefix: '.'`, `trailingSlash: true`
2. On the browser side use `connectDevframe()` from `devframe/client` or `$rpc` (the Nuxt helper)
3. Call `my.rpc.call('<fn>', args)` — bare names resolve through the scope automatically
4. If there is no UI yet → `clientAssets` may point at an empty dir temporarily, but build the SPA before shipping

### 5. Add CLI Entry And Run

> Goal: `my-tool` runs dev/build/mcp

1. Create `bin.mjs` (shebang + `import './dist/cli.mjs'`) and wire `"bin"` in `package.json`
2. At the end of `src/cli.ts`: `await createCac(myDevframe).parse(process.argv)`
3. Smoke: `my-tool` → the dev server comes up at `http://localhost:<port>/`, RPC calls work through the scoped client
4. Smoke: `my-tool build --out-dir dist-static` → the static deploy is produced; `my-tool mcp` → a stdio MCP server

### 6. Verify

> Goal: pass the checks before finishing

1. Run `/run-check` (lint + typecheck) — if it fails → run `/resolve-errors` for max 3 rounds, then stop and report
2. Confirm `static`/`snapshot` functions bake correctly into `dist-static/` (open the SPA from static serving and call them)
3. Passing → `/suggest-next-action`

## Rules

- Idempotent — if the scaffold already exists, verify only; never overwrite the original definition
- Always use `ctx.scope('<id>')` — bare `ctx.rpc.register` only when cross-tool is intended
- `importMetaUrl: import.meta.url` is required when `clientAssets` resolves from own deps
- Declare `args`/`returns` for every RPC function that takes/returns data — any Standard Schema validator works
- Never `auth: false` unless it is truly a localhost single-user tool

## Expected Outcome

- `devframe` + `cac` installed; a `DevframeDefinition` with scoped RPC functions
- `my-tool` (dev server), `my-tool build` (static), and `my-tool mcp` (stdio MCP) all work
- The SPA connects via `connectDevframe()` or `$rpc`; ready to extend with adapters/the hub per the parent `SKILL.md`
