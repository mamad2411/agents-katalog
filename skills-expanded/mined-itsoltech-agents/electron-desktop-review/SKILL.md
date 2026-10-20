---
name: electron-desktop-review
description: "Review Electron process and IPC boundaries, storage, updates, packaging, and release risk."
---

# Electron Desktop Review

Review Electron as a desktop system, not only as a frontend diff. A renderer XSS, broad preload bridge, unsafe file path, or broken updater can become a local compromise or failed rollout.

## Process

1. Inspect changed files, dependency pins, package scripts, builder config, window creation, preload, IPC handlers, storage, network calls, updater code, tests, and release notes.
2. For an existing repo, detect the repo-pinned Electron and packaging tool versions before judging APIs or defaults. For a new project, use latest stable. For version, security, signing, updater, or platform behavior decisions, verify official docs through `itsol-current-tech-context`.
3. Build a review coverage map: architecture boundaries, IPC contracts, security hardening, storage/secrets, API/network/offline behavior, auto-update/release impact, tests, and QA evidence.
4. Lead with findings by severity, with concrete exploit, data-loss, rollout, or user-impact scenarios and file references.
5. Treat missing packaged-app smoke tests, unsigned release paths, unvalidated IPC, renderer access to Node/Electron, and untested storage migrations as explicit review risks.

## Evidence

Prefer code, tests, config, lockfiles, CI logs, packaged-app behavior, and official Electron/tooling docs over assumptions.

## Focused References

- [01-architecture-boundaries.md](./references/01-architecture-boundaries.md) - main, preload, renderer, utility process, multi-window, and performance boundaries.
- [02-ipc-security-contracts.md](./references/02-ipc-security-contracts.md) - IPC contracts, preload API shape, sender checks, events, errors, and abuse cases.
- [03-storage-api-network.md](./references/03-storage-api-network.md) - local storage, secrets, API placement, offline sync, cache isolation, and logs.
- [04-update-tests-qa-release-risk.md](./references/04-update-tests-qa-release-risk.md) - auto-update, packaging review, test coverage, QA edge cases, and release blockers.
