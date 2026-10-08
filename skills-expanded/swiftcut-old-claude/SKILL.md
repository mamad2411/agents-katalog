# SwiftCut

A lightweight, local-first video editor built with Tauri (Rust) + React. Core editing must work fully offline; keep cloud services and accounts out of the core flows.

## Architecture

pnpm monorepo orchestrated by **Nx**:

- `apps/desktop/`: the Tauri v2 desktop app.
  - `src-frontend/`: the React + Vite webview UI (TanStack Router/Query/Form, shadcn/ui).
  - `src-tauri/`: the Rust core (window, native access, and later the video pipeline).
- `packages/`: shared libraries. `ui` holds the shadcn/ui components; `lint-config` holds the shared oxlint/oxfmt config.
- `packages/supabase/` and `supabase/` are **dormant**. They stay in the repo for future cloud/AI features, but nothing imports them and the app runs fully local without them. Do not wire them into the core editor.

## Conventions

- Group frontend feature code by domain (vertical slices), not by technology.
- Use `pnpm`, never `npm` or `yarn`. Orchestrate tasks with Nx (`nx run-many -t <target>`, `nx run <project>:<target>`).
- To call Rust from the frontend, expose the functionality as a `#[tauri::command]` and invoke it with `invoke()` from `@tauri-apps/api/core`.

## Environment & secrets

- The app is local-only and currently requires no env vars. `apps/desktop/src-frontend/env.ts` validates env once with zod and exports a typed `env`; add `VITE_`-prefixed vars there when needed. Nothing else reads `import.meta.env` for config (Vite's built-in flags like `import.meta.env.DEV` are fine).

## Commands

See `scripts` in the root `package.json`. The main ones:

- `pnpm dev`: launch the desktop app (Tauri window).
- `pnpm dev:web`: run the frontend in a browser with fast HMR and no Rust rebuild.
- `pnpm build` builds the frontend; `pnpm bundle` produces a desktop installer.
- `pnpm lint`, `pnpm typecheck`, and `pnpm test` run via Nx across the workspace.

The Tauri commands (`pnpm dev`, `pnpm bundle`) need a Rust toolchain with `cargo` on PATH, plus the MSVC build tools on Windows.
