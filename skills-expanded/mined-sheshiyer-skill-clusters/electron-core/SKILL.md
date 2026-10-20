---
name: electron-core
description: "Shared reference for the Electron cluster: the main/renderer/preload process model, the context-isolation security boundary (the one decision everything turns on), app lifecycle, native-module ABI notes, and the Electron-vs-Tauri tradeoff. USE WHEN making Electron architecture or security decisions — the model every Electron spoke shares."
cluster: electron
version: 1.0.0
origin: "skill-clusters (original)"
---

# Electron Core

Shared model for the `electron` cluster. An Electron app is **Chromium (renderers) + Node.js
(main)** in one bundle. Every rule below follows from one fact: **the renderer runs web content
and is untrusted; the main process holds Node/OS power.**

## 1. The process model

- **Main process** (one) — Node.js. Owns the app lifecycle, native menus, windows
  (`BrowserWindow`), the OS APIs, and all privileged work. The trusted core.
- **Renderer process** (one per window) — Chromium. Runs your HTML/CSS/JS UI, sandboxed like a
  web page. **Untrusted** — treat it as hostile.
- **Preload script** — runs in the renderer *before* page load with access to a limited bridge.
  The **only** sanctioned channel to expose main-process capability to the renderer.

## 2. The security boundary (the decision everything turns on)

Default-secure `webPreferences` for every `BrowserWindow`:

```js
new BrowserWindow({ webPreferences: {
  contextIsolation: true,   // preload & page get separate JS contexts (mandatory)
  nodeIntegration: false,   // no Node in the renderer
  sandbox: true,            // OS-level renderer sandbox
}})
```

- **`contextIsolation: true`** — the preload's objects can't be tampered with by page scripts.
- **`nodeIntegration: false`** — the page cannot `require()` Node. Never turn this on for remote content.
- **`sandbox: true`** — renderer runs in the Chromium sandbox.
- Expose capability only via **`contextBridge.exposeInMainWorld`**, a small typed surface — never the raw `ipcRenderer`, `require`, or `process`. Details → `electron-main-renderer-ipc`.
- Full hardening list (CSP, navigation/`window.open` allowlists, no `@electron/remote`) → `electron-security`.

## 3. App lifecycle (main)

`app.whenReady()` → create windows; `window-all-closed` (quit except macOS); `activate`
(re-create on macOS dock click); `before-quit` for cleanup. Single-instance via
`app.requestSingleInstanceLock()`.

## 4. Native modules

Native Node addons must be compiled against **Electron's** ABI, not system Node — use
`electron-rebuild` / prebuilds; mismatched ABI is the classic "module did not self-register"
crash. This constrains packaging → `electron-builder-packaging`.

## 5. Electron vs Tauri (pick deliberately)

| Want | Lean |
|---|---|
| Mature ecosystem, heavy Node-native deps, one JS stack, Chromium parity | **Electron** |
| Tiny binary, hardened Rust core, OS webview, capability-based security | **Tauri** (see the `tauri` cluster) |

Electron ships a full Chromium+Node per app (larger binaries, broader attack surface) — the
security checklist is non-optional.

## 6. Shared guardrails

- Renderer is untrusted: `contextIsolation` on, `nodeIntegration` off, `sandbox` on — always.
- Expose a minimal typed `contextBridge` API; never leak `ipcRenderer`/Node/`process` to the page.
- Validate every IPC argument in main; allowlist navigation and `window.open`.
- Strict CSP; never load remote content with Node powers.
- Compile native modules against Electron's ABI (`electron-rebuild`).
- Sign + notarize before distribution and before auto-update.
