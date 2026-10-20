---
name: electron-main-renderer-ipc
description: "Wire safe IPC between Electron's main and renderer processes via a preload contextBridge — ipcMain.handle/ipcRenderer.invoke, typed channels, and event streams. USE WHEN exposing main-process capability to the UI, designing an IPC API, or migrating off nodeIntegration/@electron/remote."
cluster: electron
version: 1.0.0
origin: "skill-clusters (original)"
---

# Electron Main ↔ Renderer IPC

The renderer is untrusted (see `electron-core`), so it reaches the main process only through a
**preload `contextBridge`** that exposes a small, typed API — never raw Node or `ipcRenderer`.

## The pattern

**Preload** (`preload.js`) — the only place page and Node-ish power meet:
```js
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('api', {
  readConfig: () => ipcRenderer.invoke('config:read'),         // request/response
  saveConfig: (cfg) => ipcRenderer.invoke('config:save', cfg),
  onProgress: (cb) => ipcRenderer.on('job:progress', (_e, p) => cb(p)), // stream
});
```

**Main** — validate every argument; you are the trust boundary:
```js
ipcMain.handle('config:save', (_e, cfg) => {
  if (!isValidConfig(cfg)) throw new Error('invalid config'); // never trust the renderer
  return writeConfig(cfg);
});
```

**Renderer** — calls the typed surface only: `await window.api.saveConfig(cfg)`.

## Rules

- **`invoke`/`handle`** for request→response (returns a Promise); **`on`/`send`** for fire-and-forget streams (main→renderer or renderer→main).
- Expose **named methods**, not channels — don't hand the page `ipcRenderer.send`/`invoke` directly (it could hit any channel).
- **Validate & authorize** every payload in main; the channel name is not a capability check.
- Namespace channels (`config:read`, `job:progress`); keep a typed `.d.ts` for the bridge.
- **Do not use `@electron/remote`** (formerly `remote`) — it punches through the boundary; it's removed from core for this reason.
- Senders: prefer `ipcMain.handle` over manual `event.reply`; for renderer→renderer, route through main.

## Guardrails

Minimal typed bridge; validate in main; no raw `ipcRenderer`/Node on `window`; no `@electron/remote`.
Pairs with `electron-security` (the surrounding hardening) and `electron-core` (the process model).
