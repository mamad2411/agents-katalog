---
name: follow-create-desktop-tauri
description: Create desktop apps with Tauri, Solid + TanStack Router, and a Rust backend
argument-hint: "[scope]"
related:
  - follow-create-web
  - follow-create-plugins
  - follow-create-mobile
  - follow-lib-native-sdk
  - follow-best-practice
  - setup-cicd
  - deep-review-codebase

---

## Goal

Build a Tauri desktop application that pairs a web frontend with a Rust backend for cross-platform desktop apps — the frontend uses Solid + TanStack Router per `/follow-solid-framework`

## Scope

Used to create, improve, and build Tauri desktop apps with Bun and Vite

- Check prerequisites (Rust, Bun, WebView2)
- Install dependencies and the Tauri CLI
- Configure Vite and `tauri.conf.json`
- Create IPC commands between the frontend and the Rust backend
- Add plugins as needed
- Build and test on target platforms

- Packages: `tauri`, `@tauri-apps/cli`, `@tauri-apps/api` — always confirm the latest versions via `/deep-research` + `/follow-best-practice` (no pins in this file — per `/update-devin-global-skills`); v2 uses capabilities files (`src-tauri/capabilities/*.json`) instead of the v1 allowlist and supports mobile targets

- Boundary: if true native is required — no WebView/JS runtime in the binary (TS core + `.native` markup, AOT via Zig) → use `/follow-lib-native-sdk` instead of Tauri

## Execute

### 1. Setup Environment

> Goal: verify prerequisites for Tauri development

1. Confirm Rust is installed: `rustc --version`
2. Confirm Bun is installed: `bun --version`
3. Verify WebView2 on Windows (auto-installed on first run)
4. Run `/deep-research` + `/follow-best-practice` to confirm `tauri`/`@tauri-apps/*` versions and the latest v2 API

### 2. Install Dependencies

> Goal: install dependencies for the Tauri app

1. Creating a project from scratch: `bunx create-tauri-app` (pick template/package manager as desired), then skip to Configure
2. Run `bun install`
3. Install the Tauri API: `bun add @tauri-apps/api`
4. Install the Tauri CLI: `bun add -D @tauri-apps/cli`

### 3. Configure Vite

> Goal: set up `vite.config.ts` to match the Tauri dev server

1. Set port 5173
2. Configure `server.fs.deny` or ignore `src-tauri/`
3. Set `envPrefix` to allow `VITE_` and `TAURI_`

### 4. Configure Tauri

> Goal: set up `tauri.conf.json` and capabilities

1. Edit `src-tauri/tauri.conf.json`: set `productName`, `identifier`, `devUrl: http://localhost:5173`, `beforeDevCommand: bun run dev`, `beforeBuildCommand: bun run build`
2. Define capabilities in `src-tauri/capabilities/default.json`: `["core:default", "fs:allow-read-file", "dialog:allow-open"]`

### 5. Develop IPC Commands

> Goal: create Rust commands and call them from the frontend

1. Create a Rust command in `src-tauri/src/lib.rs`
2. Register the command with `tauri::Builder::default().invoke_handler(...)`
3. Call it from the frontend with `invoke('command', args)`

### 6. Add Plugins

> Goal: install official or community plugins as needed

1. Install official plugins with `bun run tauri add <plugin-name>`
2. Install community plugins with `bun add @tauri-apps/plugin-<plugin-name>`
3. Update `tauri.conf.json` and capabilities for each added plugin

### 7. Build And Test

> Goal: build and test the Tauri app

1. Development mode: `bun run tauri dev`
2. Production build: `bun run tauri build`
3. Platform specific: `bun run tauri build --target <triple>`

## Rules

### Project Structure

```text
desktop-apps/{project}/
├── src/                    # Frontend
│   ├── components/
│   ├── hooks/
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/              # Rust backend
│   ├── src/
│   │   ├── main.rs
│   │   └── lib.rs
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   └── capabilities/
├── vite.config.ts
├── package.json
└── index.html
```

### Standards

- Use `bun` for all commands
- The Vite port must match `tauri.conf.json` (default: 5173)
- Vite must ignore `src-tauri/`
- IPC uses `invoke()` for frontend → backend
- Define capabilities in `tauri.conf.json`

### IPC Pattern

| Direction | Method |
|-----------|--------|
| Frontend → Backend | `invoke('command', args)` |
| Backend → Frontend | Events |

### Plugins

- Add only plugins that are truly needed
- Update `src-tauri/capabilities/default.json` for plugin permissions
- Never grant permissions broader than necessary

- Use /follow-solid-framework for the frontend (Solid + TanStack Router + UnoCSS)
- Use /follow-create-tauri-plugin if needed
- Use /follow-create-mobile-cross-with-capacitor if needed (create desktop tauri)
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /deep-review-codebase if needed
- Use /follow-create-plugins if needed


## Expected Outcome

- Tauri project created successfully
- Dev server runs via `bun run tauri dev`
- Frontend and Rust backend communicate through IPC
- Production build produces executables
- Capabilities follow least privilege
