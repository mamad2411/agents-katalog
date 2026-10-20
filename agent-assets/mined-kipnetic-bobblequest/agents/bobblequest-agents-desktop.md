# AGENTS.md -- apps/desktop

Electron desktop client for the template monorepo. Scope: everything under `apps/desktop/`.
Root-level rules at C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md apply in full;
this file adds desktop-specific constraints only.

## What This Is

Electron 32 + electron-vite desktop app. TypeScript in the main process, React 19 + Tailwind v4 in
the renderer, context-isolated preload bridge in between. Auth via Clerk (`@clerk/clerk-react`);
tRPC calls to `apps/api` with a Bearer JWT attached by `authHeaderLink`.

## Tech Stack

| Layer | Technology | Version |
| --- | --- | --- |
| Runtime | Electron | ^32.0.0 |
| Build tool | electron-vite | ^2.0.0 |
| Renderer framework | React + React DOM | ^19.0.0 |
| Renderer bundler plugin | @vitejs/plugin-react | ^4.0.0 |
| Styling | Tailwind CSS v4 + @tailwindcss/vite | ^4.0.0 |
| Auth | @clerk/clerk-react | ^5.61.3 |
| Data layer | tRPC v11 + @tanstack/react-query | ^11 / ^5 |
| Linter/formatter | Biome | ^2.x |
| Tests | Vitest | ^2.1.0 |
| Installer | electron-builder | ^25.0.0 |

## Entry Points

```text
src/main/index.ts        Main process — BrowserWindow, ipcMain, electron-store
src/main/composition.ts  Composition root — buildContainer() / getContainer()
src/preload/index.ts     Preload (sandboxed) — contextBridge.exposeInMainWorld('api', ...)
src/preload/index.d.ts   Ambient type for window.api
src/renderer/main.tsx    Renderer root — React 19 StrictMode mount
src/renderer/App.tsx     Session gate → SignIn | Dashboard, TrpcProvider + ClerkProvider
```

Output: `dist-electron/{main,preload,renderer}/`. Installers: `release/`.

## Run / Test / Build Commands

```bash
bun run --filter @t/desktop dev          # electron-vite dev (HMR)
bun run --filter @t/desktop build        # electron-vite build
bun run --filter @t/desktop start        # electron-vite preview
bun run --filter @t/desktop dist         # electron-builder (full installer)
bun run --filter @t/desktop pack         # electron-builder --dir (unpacked only)
bun run --filter @t/desktop typecheck    # tsc --noEmit
bun run --filter @t/desktop check        # biome check
bun run --filter @t/desktop format       # biome check --write
bun run --filter @t/desktop test         # vitest run
bun run --filter @t/desktop test:watch   # vitest (watch)
bun run --filter @t/desktop test:coverage  # vitest run --coverage
```

## App-Specific Conventions

**Main vs renderer separation**

| Concern | Main | Preload | Renderer |
| --- | --- | --- | --- |
| Node APIs (`fs`, `shell`) | Yes | No | No |
| BrowserWindow lifecycle | Yes | — | — |
| `ipcMain.handle` channel definitions | Yes | — | — |
| `contextBridge.exposeInMainWorld` | — | Yes (sole bridge) | — |
| `window.api` consumer | — | — | Yes |
| React / Tailwind | — | — | Yes |
| Clerk (`@clerk/clerk-react`) | — | — | Yes |
| tRPC client | — | — | Yes |

**IPC pattern** — all cross-boundary calls go through `window.api` (typed via
`src/preload/index.d.ts`). Add channels in `ipcMain.handle` (main) and expose them through
`contextBridge` (preload). The renderer never calls `ipcRenderer` directly.

**Env vars** — renderer vars are `VITE_*` (build-time injected by Vite). Main-process vars
(`NODE_ENV`, `LOG_LEVEL`, `PORT`) are validated at boot by `DesktopConfigValuesSchema` inside
`composition.ts`. Missing required vars surface an `Electron.dialog.showErrorBox` and quit; no
silent fallbacks.

**Auth flow** — Clerk headless email-code sign-in (OAuth redirects fail under `file://`). Session
state lives inside the Clerk client. JWT attached via `useAuth().getToken()` in `authHeaderLink`
(providers.tsx). No IPC bridge required for current auth; `ipcMain` session helpers are optional
stubs for future offline support.

## Banned in This Scope

- `nodeIntegration: true` — never enable; breaks the security model
- `contextIsolation: false` — never disable; required for the typed `window.api` bridge
- `remote` module (`@electron/remote`) — use IPC + contextBridge instead
- Calling `ipcRenderer` directly in renderer code — always go through `window.api`
- Node APIs (`fs`, `path`, `child_process`) in renderer or preload — main process only
- `any`, `@ts-ignore`, `eslint-disable` — enforced by Biome/tsc strict
- `axios` — use native `fetch`
- Prisma / Supabase JS client — not applicable; desktop has no direct DB access

## Links

Architecture doc: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\apps\desktop.md
