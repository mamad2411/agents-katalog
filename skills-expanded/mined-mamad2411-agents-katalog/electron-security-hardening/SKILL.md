---
name: electron-security-hardening
description: "Harden Electron isolation, sandbox, CSP, permissions, IPC, files, and update integrity."
---

# Electron Security Hardening

Harden Electron by narrowing every trust boundary between Chromium, Node.js, the OS, local files, and update infrastructure.

## Process

1. Identify the app trust model: local UI, remote content, preload APIs, IPC handlers, sessions, custom protocols, file access, secrets, and updater.
2. For an existing repo, detect the pinned Electron version and tooling before relying on defaults. For a new project, use latest stable. For security-sensitive defaults, fuses, protocol privileges, signing, or update validation, verify official docs through `itsol-current-tech-context`.
3. Implement controls at the trusted boundary: main process, session, protocol handler, preload contract, IPC handler, package/build config, and CI release gate.
4. Add negative tests or review evidence for bypasses: XSS payloads, bad origins, `javascript:`/`file:` URLs, untrusted sender frames, path traversal, symlink escape, stale sessions, and tampered updates.
5. Do not rely on renderer-only checks, obfuscation, ASAR secrecy, or user-controlled URLs for security decisions.

## Baseline

Production windows should have `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true`, `webSecurity: true`, `allowRunningInsecureContent: false`, controlled DevTools, CSP, explicit navigation policy, permission handlers, typed preload APIs, sender-aware IPC, signed releases, and update integrity.

## Focused References

- [01-window-session-csp.md](./references/01-window-session-csp.md) - BrowserWindow defaults, sessions, permissions, CSP, and remote content.
- [02-navigation-protocols.md](./references/02-navigation-protocols.md) - navigation, new windows, external links, deep links, and custom protocol handling.
- [03-ipc-preload-validation.md](./references/03-ipc-preload-validation.md) - preload API design, IPC schema validation, sender checks, events, and streams.
- [04-files-secrets-storage.md](./references/04-files-secrets-storage.md) - file access, path validation, symlinks, storage, secrets, logs, and crash reports.
- [05-build-update-integrity.md](./references/05-build-update-integrity.md) - fuses, ASAR integrity, signing, notarization, update integrity, and release gates.
