---
name: electron-security
description: "The Electron hardening checklist — context isolation, sandbox, no nodeIntegration, strict CSP, navigation/window.open allowlists, IPC input validation, and safe handling of remote content. USE WHEN auditing or hardening an Electron app, reviewing webPreferences, or before shipping. Follows Electron's official security recommendations."
cluster: electron
version: 1.0.0
origin: "skill-clusters (original)"
---

# Electron Security

The renderer runs web content with a powerful process behind it; a single XSS in a misconfigured
window can become full RCE on the user's machine. This is the checklist (aligned with Electron's
official "Security" guidance).

## Window configuration (every BrowserWindow)

- ✅ `contextIsolation: true` — never disable.
- ✅ `nodeIntegration: false` (and `nodeIntegrationInWorker/InSubFrames: false`).
- ✅ `sandbox: true`.
- ✅ `webSecurity: true` (never disable to "fix" CORS).
- ❌ No `@electron/remote`.

## Content & navigation

- **Strict CSP** via response headers or `<meta>` — no `unsafe-inline`/`unsafe-eval`; allowlist sources.
- **Allowlist navigation**: handle `will-navigate` and `setWindowOpenHandler` — `deny` by default, open external URLs in the user's browser (`shell.openExternal` after validating the URL).
- **Only load content you trust.** Prefer bundled local files; if you must load remote content, treat it as hostile and never give it Node/IPC power.
- Validate any URL passed to `shell.openExternal` (no `file:`/arbitrary schemes).

## IPC & data

- **Validate every IPC argument in main** (type, range, path). The renderer is the attacker.
- No path traversal: resolve and confine file paths to expected roots.
- Don't expose privileged operations as generic ("runCommand") bridge methods.

## Process & supply chain

- Keep **Electron up to date** — you inherit Chromium/V8 CVEs; track the supported release line.
- Audit dependencies (renderer deps run in the page); pin and review native modules.
- Set `app.enableSandbox()` early; consider a fuse/`@electron/fuses` to disable `runAsNode` etc.

## Pre-ship checklist

- [ ] All windows: contextIsolation✓ nodeIntegration✗ sandbox✓ webSecurity✓
- [ ] Minimal typed `contextBridge` API; no raw ipc/Node on `window`
- [ ] Strict CSP; navigation + `window.open` deny-by-default
- [ ] All IPC inputs validated in main
- [ ] Electron on a current supported version; deps audited
- [ ] App signed + notarized (`electron-builder-packaging`)

## Guardrails

If any item above is unchecked, the app is not ship-ready. Hardening is not optional for an app
that ships Chromium + Node to end users.
