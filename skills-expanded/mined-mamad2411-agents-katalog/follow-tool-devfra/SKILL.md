---
name: follow-tool-devfra
description: Build a devtool once with Devframe and mount it anywhere — SPA, CLI, static, MCP, hub
argument-hint: "[adapter-or-scope]"
related:
  - follow-lib-zod
  - use-mcp
  - run-check
  - resolve-errors
  - follow-tool-vite-devtools
  - deep-validate
  - deep-review-codebase
---

## Goal

Build a devtool with `devframe` (a single definition) and deploy it to every surface — standalone SPA, CLI, static report, MCP server, host framework, or hub dock — per the official docs <https://devfra.me>

## Scope

Use for a project that needs a devtool (inspector, analyzer, data explorer, terminal) that runs in many places

- Install `devframe` and optional peers (`cac`, a Standard Schema validator)
- Create a `DevframeDefinition` via `defineDevframe()` + scoped context
- Register RPC functions, shared state, streaming channels
- Pick the serving path: standard handler, `cac` CLI, dev server, build, MCP, Vite/embedded, framework kits (`@devframes/vite|nuxt|next`)
- Compose several devframes via `@devframes/hub`
- Has a CLI adapter (`devframe/adapters/cac`) → see `references/cli.md`

## Execute

### Workflows

| Topic | Workflow |
|-------|----------|
| Scaffold devtool | `workflows/create-devframe/SKILL.md` — install, defineDevframe, RPC, SPA, run dev/build/mcp |

### 1. Install Packages

> Goal: install `devframe` and the needed dependencies

1. Install with `bun add devframe` (ESM-only, no Vite dependency — see `references/apis.md`)
2. If shipping a standalone CLI → install the optional peer `bun add cac`
3. Install the Standard Schema validator you use: `bun add valibot` or `bun add zod` (do `/follow-lib-zod`)
4. If mounting into Vite DevTools → `bun add -D @vitejs/devtools-kit` — do `/follow-tool-vite-devtools` for the Kit's layer rules
5. If composing a hub → `bun add @devframes/hub @devframes/hub-ui`
6. Record the actually installed version in the `references/apis.md` metadata table

### 2. Define Devframe Definition

> Goal: one `defineDevframe()` any adapter can consume

1. Create `devframe.ts` exporting default `defineDevframe({ ... })` from `devframe`
2. Provide the required fields: `id` (kebab-case), `name`, `version`, `packageName`, `importMetaUrl: import.meta.url`, `homepage`, `description`, `setup(ctx)`
3. Add `icon` (Iconify, e.g. `ph:gauge-duotone`), `clientAssets` (a path or `{ package, version }`) and `basePath` when an override is needed, `services` (wire the services consumed — `{ package, version? }`), `capabilities` (per-runtime `{ dev?, build? }` flags), `rpc.snapshot` (opt other devframes' RPCs into the static dump), `duplicationStrategy` (`warn`/`silent`/`throw`/`duplicate` — hub only)
4. Set `cli` defaults when shipping a CLI: `command`, `port`, `portRange`, `open` (boolean, or a string = path), `configure(cli)`, and `flags` via `defineCliFlags` — the parsed bag is readable from the second argument of `setup(ctx, { flags })`
5. In `setup(ctx)` always use `const my = ctx.scope('<id>')` — it auto-namespaces every RPC id, shared-state key, and channel
6. Gate runtime-specific work with `ctx.mode` (`'dev'` watchers / `'build'` static dump)

### 3. Register RPC Functions

> Goal: type-safe RPC over birpc with schema validation

1. Create an `rpc/` module with `defineRpcFunction({ name, type, args, returns, setup | handler })`
2. Pick the `type`: `query` (changing reads), `static` (fixed per input, auto-dumped), `action` (mutations), `event` (fire-and-forget)
3. Use `setup: ctx => ({ handler, dump? })` when the handler needs a `DevframeNodeContext`; otherwise → the `handler(...)` shorthand
4. Set `jsonSerializable: true` when the return is JSON-only (strict `JSON.stringify` wire); the default uses `structured-clone-es` to round-trip `Map`/`Date`/`BigInt`
5. Register with `my.rpc.register(fn)` — bare names are automatically prefixed as `<id>:<name>`
6. Augment `DevframeRpcServerFunctions` via `RpcDefinitionsToFunctionsWithNamespace` for a typed client (see `references/apis.md`)
7. Broadcast to every client with `my.rpc.broadcast({ method, args, optional, event, filter })`

### 4. Shared State, Streaming, Settings

> Goal: node↔browser state sync and persisted settings

1. Use `await my.rpc.sharedState('key', { initialValue })` — observable, patch-synced, survives reconnects
2. Mutate with `state.mutate(draft => { ... })`; the browser subscribes via `state.on('updated', ...)`
3. Use `ctx.rpc.streaming.create<T>('<id>:channel', { replayWindow })` for chunk feeds (see `references/apis.md`)
4. Use `my.settings` (persisted store) for tool settings; `ctx.staticConfig` for boot-time config from the connection handshake
5. Use `ctx.host.getStorageDir(scope)` — `workspace` (committable), `project` (per-checkout), `global` (per-user)
6. Other host surfaces on `ctx`: `ctx.views.hostStatic` (serve static files from `setup`), `ctx.agent` (expose tools/resources to coding agents), `ctx.diagnostics` (namespaced diagnostics), `ctx.rpc.addFunctions` (batch registration, e.g. under `mode === 'build'`)

### 5. Client Assets (SPA)

> Goal: the UI is a built SPA that `clientAssets` points at

1. Build the SPA (Vue/Nuxt/React — anything) and point `clientAssets` at the output dir or a published package `{ package, version }`
2. Nuxt: `ssr: false`, `modules: ['@devframes/nuxt/single']`, nitro `preset: 'static'` — the helper wires `$rpc` for you
3. Next.js: `output: 'export'`, `assetPrefix: '.'`, `trailingSlash: true`, `images.unoptimized` — copy `out/` into `clientAssets`
4. On the browser side use `connectDevframe()` from `devframe/client` — it auto-resolves the connection descriptor (dev WebSocket / static dump)
5. Call RPC from the client: `(await connectDevframe()).scope('<id>').rpc.call('<fn>', args)`

### 6. Choose Serving Path

> Goal: mount one definition onto the wanted surface (see the `references/apis.md` adapter matrix)

1. Raw handler: `initDevframe(def, { base })` from `devframe/initiate` → `.handler` (Request→Response) or `.nodeMiddleware` (Connect-style)
2. Standalone CLI: `createCac(def).parse()` from `devframe/adapters/cac` — commands `dev` (default), `build`, `mcp` (see `references/cli.md`)
3. Dev server only: `createDevServer(def, { port, flags, onReady })` from `devframe/adapters/dev` → a `StartedServer` handle
4. Static snapshot: `createBuild(def, { outDir })` from `devframe/adapters/build` — a self-contained deploy
5. MCP server: `createMcpServer(def, { transport: 'stdio' })` from `devframe/adapters/mcp`
6. Vite DevTools: `createPluginFromDevframe(def)` from `@vitejs/devtools-kit/node` — see `/follow-tool-vite-devtools` before mounting
7. Runtime registration: `createEmbedded(def, { ctx })` from `devframe/adapters/embedded`
8. Framework kits: `@devframes/vite|nuxt` subpaths `/single` (author) and `/hub` (mount the hub); the bare import throws

### 7. Compose With Hub

> Goal: several devframes behind one handler

1. Use `initHub({ base: DEVFRAMES_HUB_BASE, devframes: [...], ui: createUi() })` from `@devframes/hub/initiate` + `@devframes/hub-ui`
2. The hub is headless — dock registry, terminal aggregation, message queue, command palette; the UI provider is separate
3. Devframes in a hub share the RPC registry, state store, connection, auth gate, and an aggregate MCP endpoint
4. Cross-devframe capabilities via `ctx.services.provide()` / `whenAvailable()` / `get()`
5. Mount the hub into a framework via `@devframes/vite/hub` or `@devframes/nuxt/hub`

### 8. Expose To Agents (MCP)

> Goal: the devtool answers coding agents via MCP/WebMCP

1. Add `agent: { description, title }` to `defineRpcFunction` — opt-in per function (safety is inferred from `type`)
2. The `agent` field automatically enables `jsonSerializable` — MCP consumes JSON-shaped data
3. Run the MCP server with `my-tool mcp` or `createMcpServer(def, { transport: 'stdio' })` — do `/use-mcp` to wire it into a client; `1.2.4`+ exposes shared state to agents via `exposeSharedState`
4. Do `/run-check` + `/deep-validate` before shipping; on error → `/resolve-errors` for max 3 rounds

## Rules

### 1. Definition Design

- Always use `ctx.scope('<id>')` — never register bare names on `ctx.rpc` unless cross-tool is intended
- `importMetaUrl: import.meta.url` is required when resolving `clientAssets`/`services` from own dependencies (pnpm strict layout safe)
- `id` is kebab-case and unique per host; naming convention `<id>:<kebab-action>`
- Source metadata from `package.json` (`import pkg from '../package.json' with { type: 'json' }`) — `packageName` ≠ `name`

### 2. RPC And Data Design

- Declare `args`/`returns` schemas with a Standard Schema validator — enforced at runtime
- `static` only for data fixed per input; a `query` needs an explicit `dump` to be baked into a static build (`snapshot: true` for no-args payloads)
- `jsonSerializable: true` requires JSON-only returns — `Map`/`Date` will not round-trip
- Use `my.rpc.call('fn', args)` for local invocation; the fully-qualified `<id>:<fn>` calls across tools

### 3. Serving And Security

- Standalone (`cli`/`build`) defaults basePath to `/`; hosted (`vite`/`embedded`) defaults to `/__<id>/` — override with `basePath`
- Connections bind localhost + trust the handshake (OTP) by default — use `auth: false` only for localhost single-user tools
- Dev RPC supports WebSocket with an SSE fallback (serverless/buffering proxies) — the same birpc wire protocol
- CLI `open: true` embeds the OTP in the URL — the opened tab is already authenticated

### 4. Version Notes

- Latest: `devframe@1.2.5` (verified 2026-10-15); stable pin (published ≥7 days): `1.2.3` — `1.2.4` added `exposeSharedState` in the MCP route options
- The `@devframes/*` kits follow the same version (`1.2.x`); `@vitejs/devtools-kit` is a separate adapter (`0.7.6` stable / `0.8.0` latest — json-render moved from the Kit into `@vitejs/devtools` in 0.8.0, see `/follow-tool-vite-devtools`)
- Docs: any page can be fetched as raw markdown: `https://devfra.me/raw/<path>.md`, full docs at `https://devfra.me/llms-full.txt` (see `references/apis.md`)
- Check `package.json` + `/deep-review-codebase` before choosing APIs — the spec may drift after 1.0

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- One `DevframeDefinition` deploys to many surfaces without forking code per framework
- RPC fully type-safe across node→browser, browser→node, and agent (MCP) with schema validation
- Shared state syncs across reconnects; streaming channels serve chunk feeds
- CLI `my-tool` (dev/build/mcp), a static snapshot in `dist-static/`, and mounting into a host framework or the hub all work
- Consistent with the official Devframe docs at <https://devfra.me>
