---
name: electron-port-kickoff
description: >
  This skill should be used when the user wants to port an existing Node.js +
  Vite + React (or similar modern web) application into a desktop Electron app.
  Triggers on phrases like "port to electron", "make this an electron app",
  "electron-ify", "electron port", "turn this into a desktop app", "bundle as
  desktop", "ship as .dmg / .exe / .AppImage", or when the user references an
  existing web codebase and wants it packaged for desktop distribution.
version: 0.1.0
---

# Electron Port Kickoff

## When this skill is loaded

The user has an existing web app — usually Node + (Vite or Webpack) + (React, Vue, Svelte, or Solid) + (TypeScript or JS) — and wants to ship it as a desktop Electron binary. This skill guides the first 60 minutes: scaffold choice, main/renderer split, Express or local-server integration, and a runnable local binary.

## The one rule that saves weeks

**Do not hand-wire Electron from scratch.** Start from a maintained scaffold and import the user's code into it. Scaffolds have already solved the main/renderer/preload split, Vite integration, HMR for both processes, CI, and electron-builder config. Starting from scratch means rediscovering every one of those problems yourself.

## Scaffold recommendation decision tree

| Existing stack | Recommended scaffold | Why |
|---|---|---|
| React + Vite + Tailwind + shadcn/ui | `luanroger/electron-shadcn` | Near-1:1 fit; CI preconfigured; trust 9.9 |
| React + Vite (plain) | `electron-vite/electron-vite-react` | Canonical Vite + Electron + React |
| Vue + Vite | `electron-vite/electron-vite-vue` | Same story, Vue flavor |
| Svelte or Solid + Vite | `alex8088/electron-vite` (base) | Use the base, pick your framework |
| Opinionated, large-app, plugin-based | `electron/forge` | Canonical but heavier; better if you need Forge's plugin ecosystem |

See `references/scaffolds.md` for a deeper comparison.

## Architecture — what the port actually looks like

```
your-app/
├── src/
│   ├── main/            # Electron main process (Node + Chromium)
│   │   ├── main.ts      # App lifecycle, window management, auto-updater wiring
│   │   └── preload.ts   # Trust boundary — minimal code exposing APIs to renderer
│   ├── renderer/        # Your existing Vite + React/Vue/Svelte app lives here
│   │   ├── index.html
│   │   └── src/…
│   └── server/          # (Optional) Your existing Express/Fastify server
│       └── index.ts     # Spawned as child process from main.ts
├── electron-builder.yml # Build + package config
└── package.json
```

**Three process types to internalize:**

1. **Main process** — Node + Chromium lifecycle. Opens windows, owns the menu bar, talks to the OS. Can spawn the Express server (as a child process or inline).
2. **Renderer process** — Chromium window running your UI. In dev, loads from the Vite dev server (`http://localhost:5173` or similar). In prod, loads from a bundled `file://` path OR from `http://localhost:<port>` if your Express server is still running.
3. **Preload script** — A small trusted script that runs in the renderer context with access to Node APIs. Used with `contextBridge.exposeInMainWorld()` to give the UI safe access to specific capabilities.

For type-safe IPC, prefer `electron-trpc` over raw `ipcMain`/`ipcRenderer`. It's worth the 20 minutes of setup.

## The 60-minute kickoff path

1. **Clone the chosen scaffold** into a scratch directory outside your repo. `pnpm install`. `pnpm dev`. **Confirm the baseline app window opens.** If this step fails, you have a toolchain problem — fix Xcode CLTs, Python, node-gyp, whatever it is — before going further.

2. **Run the scaffold's package step end-to-end** (usually `pnpm package` or `pnpm make`). Confirm a `.dmg` or `.app` appears in `dist/` or `out/`. This one-time sanity check saves hours later.

3. **Create an `electron-port` branch** in the user's target repo.

4. **Import the UI** — copy the existing Vite + React source into the scaffold's `src/renderer/`. Reconcile import paths. Expect some Tailwind config merging if both use it.

5. **Wire the server** (if applicable) — if the app has an Express/Fastify server:
   - Option A (simplest): Spawn it as a child process in `src/main/main.ts` on `app.whenReady()`. Kill it in `app.on('before-quit')`. Renderer hits `http://localhost:<port>` as before.
   - Option B (cleaner): Require and boot the server inline in the main process. Avoid if the server has heavy startup.
   - Option C (type-safe, no local HTTP): Replace HTTP with `electron-trpc`. Bigger refactor but eliminates the localhost port.

6. **Fix filesystem paths.** Anything that reads from `./data`, `process.cwd()`, or a relative path will break. Use `app.getPath('userData')` for user-specific data and `process.resourcesPath` for bundled read-only assets.

7. **Rebuild native modules.** If the app uses `better-sqlite3`, `keytar`, `bcrypt`, `node-pty`, or anything with `binding.gyp`, run `pnpm add -D @electron/rebuild && pnpm rebuild`. Add it as a postinstall.

8. **Smoke test.** `pnpm dev` → app window opens → renders the board → hits the local server → gets a 200 from `/api/health` (or equivalent). That's your baseline.

9. **Commit to `electron-port` branch.** Push. Celebrate.

## Common rookie mistakes — in order of frequency

1. **Hardcoded paths.** `./data/app.db` works in dev, breaks once packaged. Fix: `path.join(app.getPath('userData'), 'data', 'app.db')`.
2. **Native modules against wrong Node ABI.** Fix: `@electron/rebuild`, always, after every `pnpm install`.
3. **CORS in dev.** Dev renderer on `:5173`, server on `:3100`. Fix: enable CORS in the server for dev only, OR load the renderer through the server's origin.
4. **Turning off `contextIsolation`.** Don't. It's the 2025 security default. Use `contextBridge` instead.
5. **Blocking the main process with long work.** DB migrations, AI calls, file scans — use worker threads or child processes, not the main process directly.
6. **Assuming dev assets == prod assets.** In dev, Vite serves with HMR. In prod, assets are bundled. The scaffold handles this, but if you hand-edit Vite config you can break the prod build.
7. **Not testing the packaged build early.** Run `pnpm package` once a week minimum during the port. Regressions against packaged mode hide easily.

## Handoff to packaging

After the 60-minute kickoff passes, move on to:
- `electron-code-signing` skill for signing + notarization
- `electron-auto-update` skill for the release pipeline

For packaging config (electron-builder targets, icons, installer settings), see `references/packaging.md`.

## Port checklist — paste into the user's plan doc

```
- [ ] Scaffold cloned and running baseline
- [ ] Scaffold's package step produces a binary on this machine
- [ ] electron-port branch created in target repo
- [ ] UI imported and rendering
- [ ] Local server (if any) spawned and reachable from renderer
- [ ] Filesystem paths replaced with app.getPath('userData') / resourcesPath
- [ ] Native modules rebuilt with @electron/rebuild
- [ ] Smoke test: app window opens, UI renders, /api/health returns 200
- [ ] Committed and pushed to electron-port branch
- [ ] Baseline packaged build runs on this machine outside of dev
```

## References

- `references/scaffolds.md` — detailed scaffold comparison with pros/cons
- `references/packaging.md` — electron-builder config cheat sheet
