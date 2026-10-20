---
name: electron-bun-dev-orchestrator
description: Cross-platform Electron dev launcher that parallel-builds main/preload/MCP subprocess bundles, waits for file stability, watches with esbuild's JS API, and spawns Vite + Electron - replaces a fragile tree of npm scripts.
category: electron
version: 1.0.0
version_origin: extracted
tags: [electron, bun, esbuild, vite, dev-tooling]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/electron-dev.ts
imported_at: 2026-04-18T00:00:00Z
---

# Electron + Bun dev orchestrator

## When to use
- Electron app with separate main / preload / renderer / MCP-subprocess bundles.
- Team on mixed macOS + Windows + Linux dev machines (you want ONE dev script).
- Running multiple local instances side-by-side (e.g. beta vs stable).
- Need watch rebuild + verify-before-launch to avoid Electron starting on a half-written `main.cjs`.

## How it works
1. **Instance detection** (`detectInstance`, line 68): parses trailing `-N` off the project folder name to set `CRAFT_VITE_PORT=${N}173`, `CRAFT_CONFIG_DIR=~/.craft-agent-${N}`, a unique app name, and a unique deep-link scheme. Lets you clone the repo into `craft-agents-1/`, `craft-agents-2/` for parallel instances.
2. **Port cleanup**: `killProcessOnPort(vitePort)` handles both `lsof -ti:PORT | xargs kill -9` (unix) and `netstat -ano | findstr :PORT` -> `taskkill /PID x /F` (windows).
3. **Initial one-shot build** of `main.cjs`, `bootstrap-preload.cjs`, `browser-toolbar-preload.cjs` via `esbuild.build()` with `platform: 'node', format: 'cjs', external: ['electron']`. Run in `Promise.all` for parallelism.
4. **File-stability gate**: after build, `waitForFileStable(path, 10_000)` polls size every 100ms, only returning `true` after 3 consecutive unchanged readings. Prevents Electron from picking up a half-flushed binary.
5. **Syntax verification**: shell out to `node --check <file>` before launching. If it fails, fail fast - much better DX than Electron crashing later.
6. **Watch mode via esbuild JS API**: `ctx = await esbuild.context({...}); await ctx.watch();` - keep contexts in an array to `dispose()` on shutdown.
7. **Vite dev server** is a separate `spawn(['vite', 'dev', '--port', N, '--strictPort'])` - strictPort means it fails loudly rather than silently shifting.
8. **Launch Electron** last (`spawn([ELECTRON_BIN, 'apps/electron'])`) with env wired: `VITE_DEV_SERVER_URL=http://localhost:${port}`, `CRAFT_CONFIG_DIR`, `CRAFT_APP_NAME`, etc.
9. **Clean shutdown**: SIGINT/SIGTERM handler disposes esbuild contexts, kills all `Subprocess`es.

## Example
```ts
// Watch main + preload with esbuild's context API
const mainCtx = await esbuild.context({
  entryPoints: [join(ROOT, 'apps/electron/src/main/index.ts')],
  bundle: true, platform: 'node', format: 'cjs',
  outfile: join(ROOT, 'apps/electron/dist/main.cjs'),
  external: ['electron'],
  define: oauthDefines,
});
await mainCtx.watch();
// after initial build + verify, spawn Electron
spawn([ELECTRON_BIN, 'apps/electron'], {
  env: { ...process.env, VITE_DEV_SERVER_URL: `http://localhost:${port}` },
});
```

## Gotchas
- Must build MCP subprocess bundles (e.g. `packages/session-mcp-server`) even in dev - the Electron main process spawns them at runtime from `dist/`.
- Pi-SDK uses ESM-only packages; `bun build --target=bun --format=esm` is the ONLY bundler combo that works (esbuild `packages:external` leaves broken `require()` calls).
- `waitForFileStable` matters more than you think - Electron on Windows will happily launch with an empty `.cjs`.
- `node --check` doesn't work for Electron-specific packages (e.g. `@sentry/electron`) because it evaluates top-level code. Use file-exists + non-empty check instead for preload.
