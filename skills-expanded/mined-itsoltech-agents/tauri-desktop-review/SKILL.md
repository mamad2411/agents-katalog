---
name: tauri-desktop-review
description: "Review Tauri contracts, commands, capabilities, updater, platform behavior, and tests."
---

# Tauri Desktop Review

Review Tauri as a desktop system with a Rust application core, a WebView UI, explicit capabilities, native packaging, and platform-specific runtime behavior.

## Process

1. Inspect changed files, dependency pins, package manager, `src-tauri/Cargo.toml`, lockfiles, `tauri.conf.*`, capabilities, Rust commands, frontend Tauri adapters, storage, updater, tests, CI, and QA notes.
2. For an existing repo, detect repo-pinned Tauri, Rust, npm/package-manager, frontend framework, and plugin versions before judging APIs or defaults. For a new project, use latest stable. For version, capability, updater, signing, or platform behavior decisions, verify official docs through `itsol-current-tech-context`.
3. Build a review coverage map: architecture boundaries, command/IPC contracts, capabilities and security posture, storage/secrets, updater/release impact, platform behavior, tests, and QA evidence.
4. Lead with findings by severity, with concrete exploit, data-loss, rollout, or user-impact scenarios and file references.
5. Treat missing packaged-app smoke tests, unvalidated commands, broad capabilities, unsafe filesystem/shell scopes, untested migrations, and unsigned or unverified updater paths as explicit review risks.

## Evidence

Prefer code, tests, config, lockfiles, CI logs, packaged-app behavior, platform QA, and official Tauri/Rust/frontend docs over assumptions.

## Focused References

- [01-architecture-boundaries.md](./references/01-architecture-boundaries.md) - frontend, WebView, Rust core, state ownership, windows, sidecars, and performance boundaries.
- [02-commands-ipc-contracts.md](./references/02-commands-ipc-contracts.md) - command API shape, DTOs, validation, typed errors, events, progress, and cancellation.
- [03-capabilities-storage-security.md](./references/03-capabilities-storage-security.md) - capabilities review, filesystem/shell scope, secrets, local data, CSP, auth, and logs.
- [04-updater-platform-tests-qa.md](./references/04-updater-platform-tests-qa.md) - updater, platform behavior, packaged-app tests, CI gates, QA matrix, and review risk.
