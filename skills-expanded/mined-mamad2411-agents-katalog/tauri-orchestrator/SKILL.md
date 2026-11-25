---
name: tauri-orchestrator
description: "Route a Tauri task to the right skill among 40 Tauri specialists — scaffolding, the security/capability model, IPC and the Rust↔frontend bridge, windows/UI chrome, sidecars, plugins, building, signing, per-platform distribution, debugging, and migration. USE WHEN a user is building, configuring, securing, or shipping a Tauri v2 desktop/mobile app but hasn't named the specific concern."
cluster: tauri
version: 1.0.0
---

# Tauri Orchestrator

The single entry skill for Tauri v2 work. It locates the task on the **lifecycle ×
concern** map and delegates to one of 40 specialist spokes. The cross-cutting model every
Tauri app shares — the capability / permission / scope security system, the IPC trust
boundary, the process model, and the v2 conventions — lives in `tauri-core`; read it before
configuring permissions or wiring IPC.

## Routing map (intent → spoke)

**Scaffold & understand**
- New project / first run → `setting-up-tauri-projects`, `tauri-v2`
- "How does Tauri actually work?" → `understanding-tauri-architecture`, `understanding-tauri-process-model`, `understanding-tauri-runtime-authority`, `understanding-tauri-lifecycle-security`, `understanding-tauri-ecosystem-security`

**Configure the app**
- App/config knobs → `configuring-tauri-apps`
- **Security surface** (the heart of Tauri) → `configuring-tauri-capabilities`, `configuring-tauri-permissions`, `configuring-tauri-scopes`, `configuring-tauri-csp`, `configuring-tauri-http-headers`  *(model in `tauri-core`)*
- Windows / chrome → `customizing-tauri-windows`, `adding-tauri-splashscreen`, `adding-tauri-system-tray`
- Bundled files → `managing-tauri-app-resources`

**IPC & the Rust ↔ frontend bridge**
- Concept → `understanding-tauri-ipc`
- JS → Rust (commands) → `calling-rust-from-tauri-frontend`
- Rust → JS (emit/invoke) → `calling-frontend-from-tauri-rust`
- Events → `listening-to-tauri-events`
- Wiring a frontend → `integrating-tauri-js-frontends`, `integrating-tauri-rust-frontends`

**Extend**
- Sidecars / external binaries → `embedding-tauri-sidecars`, `running-nodejs-sidecar-in-tauri`
- Plugins → `developing-tauri-plugins`, `managing-tauri-plugin-permissions`

**Build, sign, ship**
- Optimize / CI → `optimizing-tauri-binary-size`, `building-tauri-with-github-actions`
- Sign → `signing-tauri-apps`
- Per-platform → `distributing-tauri-for-macos`, `distributing-tauri-for-windows`, `packaging-tauri-for-linux`, `distributing-tauri-for-ios`, `distributing-tauri-for-android`
- Managed pipeline → `using-crabnebula-cloud-with-tauri`

**Operate & maintain**
- Debug → `debugging-tauri-apps`
- Test → `testing-tauri-apps`
- Upgrade / migrate → `updating-tauri-dependencies`, `migrating-tauri-apps`

## Standard Operating Flow

1. Locate the task: which lifecycle stage (scaffold → configure → bridge → extend → ship → operate) and which concern.
2. If it touches **permissions, scopes, IPC, or CSP**, pull the model from `tauri-core` first — these are interlocking, not independent.
3. Delegate to the spoke(s). Multi-step asks fan out in lifecycle order (e.g. "ship to all desktops" → sign → macos + windows + linux).
4. Return: chosen spoke(s), the capability/permission changes implied, target platform(s), and the next action.

## Guardrails

See `tauri-core`. In short: **default-deny** — grant the narrowest capability/permission/scope
that works; keep the CSP strict; never expand the IPC allowlist or filesystem scope without
saying so explicitly; confirm signing identities and per-platform requirements before a release
build. Tauri's value is the locked-down security boundary — don't quietly widen it.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
