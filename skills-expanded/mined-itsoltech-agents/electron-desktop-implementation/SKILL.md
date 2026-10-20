---
name: electron-desktop-implementation
description: "Implement Electron boundaries, typed IPC, windows, sessions, storage, packaging, and tests."
---

# Electron Desktop Implementation

Implement Electron desktop apps with explicit process boundaries, narrow preload APIs, validated IPC, hardened windows and sessions, deliberate storage/API choices, and verification that includes packaged-app behavior.

## Process

1. Inspect repo conventions, `.itsol.md`, package manager, Electron/builder versions, frontend framework, existing `main`/`preload`/`renderer` layout, test commands, packaging target, and release channel.
2. For existing repos, use the repo-pinned Electron and tooling versions unless the task includes an approved upgrade. For new projects, use latest stable Electron and current stable tooling.
3. Use `itsol-current-tech-context` for Electron, Electron Forge, electron-builder, WebdriverIO, Playwright Electron, signing, auto-update, or version decisions that depend on current official docs.
4. Decide the smallest architecture that matches the product: single-window MVP, modular medium app, or workspace/monorepo for large multi-window/offline apps.
5. Keep renderer as web UI, preload as a narrow typed bridge, main as system/lifecycle/OS boundary, and utility processes/workers for CPU-heavy or crash-prone work.
6. Define IPC contracts, storage ownership, error handling, logout/tenant cleanup, offline behavior, and QA scenarios before editing broad cross-process behavior.
7. Verify with the repo's typecheck, lint, unit/integration tests, build/package command, and a packaged-app smoke test when the change touches preload paths, storage, signing, updater, native modules, or production flags.

## Coordination

Use with `itsol-current-tech-context`, `security-frontend-browser-review`, `security-files-integrations-review`, `security-secrets-config-review`, `ui-frontend-testing-qa`, `ui-accessibility-motion`, and framework-specific frontend skills as relevant.

## Reference Routing

- Architecture, project layout, process ownership, TypeScript config, and cross-window state: read [01-architecture-and-processes.md](./references/01-architecture-and-processes.md).
- Preload APIs, IPC contracts, validation, event subscriptions, streaming, cancellation, and error mapping: read [02-ipc-and-contracts.md](./references/02-ipc-and-contracts.md).
- BrowserWindow hardening, sessions, permissions, navigation, external links, CSP, custom protocol, and threat model checks: read [03-windows-sessions-security.md](./references/03-windows-sessions-security.md).
- Local storage, secrets, API-from-renderer vs API-through-main, offline queues, sync, logout, tenant separation, and migrations: read [04-storage-api-offline.md](./references/04-storage-api-offline.md).
- OS integrations, packaging, auto-update, signing, performance, utility process, tests, QA, and release verification: read [05-os-packaging-performance-tests.md](./references/05-os-packaging-performance-tests.md).

## Version Policy

- Existing repo: detect and respect pinned `electron`, builder, Forge, test runner, and frontend package versions from lockfiles and config.
- New project: use latest stable Electron and stable ecosystem tooling.
- Version-sensitive decisions: check current official docs through `itsol-current-tech-context` before recommending APIs, defaults, update tooling, signing flow, or test runners.

## Minimum Feature Definition

For any desktop feature, define:

- affected layers: renderer, preload, main, storage, API, OS integration
- IPC channels, request/response/error schemas, timeout/cancellation behavior
- security and privacy impact, including XSS-after-compromise behavior
- storage location, schema version, migrations, and cleanup on logout/user/tenant change
- offline behavior when network, VPN, proxy, TLS, or server schema changes
- verification: unit/integration/E2E/manual packaged smoke as appropriate
