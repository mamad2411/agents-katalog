---
name: tauri-security-capabilities
description: "Harden Tauri v2 capabilities, command validation, scopes, secrets, CSP, and updater integrity."
---

# Tauri Security Capabilities

Harden Tauri by narrowing each trust boundary between the WebView frontend, Rust core, OS APIs, local files, process execution, secrets, and update infrastructure.

## Process

1. Identify the trust model: windows/webviews, local UI, any remote content, capabilities, permissions, custom commands, plugin scopes, filesystem, shell/process, sidecars, secrets, auth/session, CSP, deep links, and updater.
2. For an existing repo, detect pinned Tauri, plugins, Rust, npm/package-manager, and frontend versions before relying on defaults. For a new project, use latest stable. For security-sensitive defaults, capability semantics, command scopes, updater signatures, signing, or CSP behavior, verify official docs through `itsol-current-tech-context`.
3. Implement controls at the trusted boundary: capability files, permission scopes, Rust command validation, storage adapters, CSP, release config, and CI gates.
4. Add negative tests or review evidence for bypasses: bad window/webview access, malformed payloads, path traversal, symlink escape, untrusted deep links, remote content, tampered updates, and leaked secrets.
5. Do not rely on frontend-only checks, obscurity, bundled asset secrecy, user-controlled URLs, or UI-disabled controls for security decisions.

## Baseline

Production Tauri apps should use per-window capabilities, minimal permissions, scoped plugin access, typed and validated Rust commands, restrictive CSP, secure secret storage, controlled deep links, signed sidecars where applicable, signed update artifacts, dependency checks, and packaged-app security smoke tests.

## Focused References

- [01-capabilities-permissions.md](./references/01-capabilities-permissions.md) - Tauri v2 capabilities, permissions, scopes, window/webview assignment, and least privilege review.
- [02-command-validation.md](./references/02-command-validation.md) - Rust command DTOs, validation, authorization, typed errors, event safety, and command-scope enforcement.
- [03-files-shell-secrets.md](./references/03-files-shell-secrets.md) - filesystem paths, shell/process/sidecar controls, local storage, secure storage, logs, and diagnostics.
- [04-csp-auth-updater-supply-chain.md](./references/04-csp-auth-updater-supply-chain.md) - CSP, remote content, deep links, auth/session, updater integrity, signing, and dependency gates.
