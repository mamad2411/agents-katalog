---
name: tauri-desktop-implementation
description: "Implement Tauri frontend/Rust boundaries, commands, state, storage, sidecars, and tests."
---

# Tauri Desktop Implementation

Implement Tauri desktop apps by treating the WebView as UI, Rust as the trusted system boundary, and Tauri IPC as a local API contract.

## Process

1. Inspect repo-pinned Tauri, Rust, npm/package-manager, frontend framework, plugin, bundler, test, and CI versions. For new projects, use latest stable choices only after checking official docs through `itsol-current-tech-context`.
2. Define the boundary: UI state in frontend, privileged/system work in Rust, stable DTOs across commands/events/channels, and explicit ownership for durable state.
3. Design Tauri v2 capabilities and permissions before wiring privileged features. Keep permissions per window/webview and review command scopes as part of the feature.
4. Implement thin `#[tauri::command]` handlers over testable Rust services, register commands explicitly, and expose a single frontend adapter instead of scattered raw `invoke` calls.
5. Add validation, typed errors, lifecycle handling, cancellation/progress for long work, and storage choices appropriate to data sensitivity.
6. Verify with frontend tests, Rust tests, command/service tests, and packaged-app smoke tests when the feature touches files, sidecars, updater, permissions, or platform behavior.

## Coordination

Use with `itsol-current-tech-context`, `security-files-integrations-review`, `security-auth-session-review`, `ui-frontend-testing-qa`, `ui-performance-stability`, the relevant frontend framework skill, and release/distribution skills when packaging, signing, updater, or CI artifacts are in scope.

## Reference Routing

- Version detection, app structure, frontend/Rust boundaries, and architecture sizing: read [01-context-and-architecture.md](./references/01-context-and-architecture.md).
- Commands, explicit registration, IPC DTOs, typed errors, events, channels, progress, and frontend adapters: read [02-commands-ipc-events.md](./references/02-commands-ipc-events.md).
- Tauri v2 capabilities, permissions, command scopes, CSP, filesystem, shell, storage, and secrets: read [03-capabilities-security-storage.md](./references/03-capabilities-security-storage.md).
- Rust state, long-running tasks, local persistence, offline/API sync, windows, tray, deep links, and sidecars: read [04-state-offline-sidecars.md](./references/04-state-offline-sidecars.md).
- Performance, observability, tests, packaged smoke tests, updater, signing, CI, and PR handoff: read [05-testing-performance-release.md](./references/05-testing-performance-release.md).

## Version Policy

- Existing repo: implement against pinned `tauri`, Tauri plugins, Rust toolchain, package manager, frontend framework, bundler, test runner, and platform targets.
- New project: use latest stable Tauri/Rust/npm/frontend choices after checking official docs through `itsol-current-tech-context`.
- Version-sensitive decisions, especially Tauri v2 capabilities/permissions, command registration, updater, WebDriver, signing, and plugin APIs, require official docs before finalizing.
