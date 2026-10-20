---
name: tauri-desktop-debugging
description: "Debug Tauri WebView, Rust commands, IPC, capabilities, sidecars, updater, and bundling."
---

# Tauri Desktop Debugging

For bugfix authorization and plan prerequisites, defer to `itsol-workflow-mode`; retain evidence, root-cause analysis, proportionate verification, and final review in every mode.

Debug Tauri by locating the failing boundary first: WebView UI, frontend adapter, IPC contract, Rust command/service, capability/permission, storage/filesystem, sidecar/process, updater, bundle, or platform integration.

## Process

1. State expected behavior, actual behavior, impact, OS, architecture, app version/channel, dev/debug/release mode, Tauri/Rust/frontend versions, and the smallest reproducible symptom.
2. Inspect repo-pinned Tauri, Rust, npm/package-manager, frontend framework, plugins, bundler, test runner, and CI versions. For new-project or upgrade-sensitive advice, use latest stable only after checking official docs through `itsol-current-tech-context`.
3. Gather evidence before changing code: WebView console, Rust logs/stdout/stderr, command name and payload, event/channel listeners, capability files, `tauri.conf.*`, sidecar paths/output, updater metadata, packaged build logs, and platform logs.
4. Reproduce in the mode that fails. If a packaged app fails, do not rely on `tauri dev`; build or run a packaged-like artifact with isolated app data.
5. Fix one boundary at a time. Add a regression test when the repo supports it; otherwise document the narrowest reliable manual verification.
6. Use `itsol-bug-debugging` for user-facing defects and follow its Technical Fix Plan gate when required by the resolved workflow mode.

## Coordination

Use with `itsol-current-tech-context`, `itsol-bug-debugging`, `security-files-integrations-review`, `security-frontend-browser-review`, `infra-observability`, `ui-performance-stability`, and the frontend framework debugging skill used by the WebView.

## Reference Routing

- Evidence matrix, repro isolation, version detection, and dev-vs-packaged triage: read [01-evidence-and-triage.md](./references/01-evidence-and-triage.md).
- Frontend/WebView, CSP, adapter, `invoke`, events/channels, listeners, and cross-window symptoms: read [02-frontend-webview-ipc.md](./references/02-frontend-webview-ipc.md).
- Rust command registration, command handlers, state, async locks, panics, serialization, logs, and service-layer failures: read [03-rust-commands-state-logs.md](./references/03-rust-commands-state-logs.md).
- Capabilities/permissions, filesystem, shell/process, deep links, storage, and sidecar failures: read [04-permissions-fs-shell-sidecars.md](./references/04-permissions-fs-shell-sidecars.md).
- Packaged-only failures, updater, signing/notarization, bundle assets, installers, and platform-specific failures: read [05-bundling-updater-platforms.md](./references/05-bundling-updater-platforms.md).

## Version Policy

- Existing repo: debug against pinned `tauri`, Tauri plugins, Rust toolchain, package manager, frontend framework, bundler, test runner, and CI/release configuration.
- New or upgrade-sensitive advice: use latest stable only after checking official docs through `itsol-current-tech-context`.
- Symptoms involving Tauri v2 capabilities/permissions, command registration, updater, WebDriver, sidecars, signing, or plugin APIs require current official docs before recommending version-specific fixes.
