---
name: electron-context-isolation
description: >
  Electron contextIsolation and sandbox for owned apps: separate isolated world,
  preload contextBridge APIs, IPC hardening, and migration off nodeIntegration.
  Use when contextIsolation, sandbox, preload.js, contextBridge, or renderer
  prototype-pollution-to-privilege concerns. Complements electron-app-security.
---

# Electron contextIsolation

## Scope And Authorization

- **In scope:** Refactors and reviews of Electron renderer isolation on apps you own.
- **Out of scope:** Bypassing isolation on third-party apps without authorization.
- Isolation assumes renderer content may be hostile (XSS, compromised deps).
- Redact real IPC payloads containing tokens from docs.
- Pair with `electron-app-security` for navigation/openExternal and `code-quality-standards`.

## When To Use

- Migrating legacy apps from `nodeIntegration: true` / `contextIsolation: false`.
- Designing a minimal preload API with `contextBridge.exposeInMainWorld`.
- Enabling `sandbox: true` and fixing preload constraints.
- Fixing bugs where renderer prototypes were polluted to reach Node.
- Reviewing third-party UI kits loaded into the renderer.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full app security checklist | `electron-app-security` |
| asar integrity | `electron-asarsecurity` |
| Electron fuses | `electron-fuses` |
| Generic XSS prevention | `xss-cross-site-scripting` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Isolation | `contextIsolation: true` (default in modern Electron—do not turn off) |
| Node in renderer | Always off in production windows |
| Preload | Runs with privileged APIs; keep tiny |
| Bridge | Expose functions/values only—no object graphs with methods from Node |
| Sandbox | Prefer on; adjust preload to be sandbox-compatible |
| IPC | Channel allowlists + argument validation in main |

## Workflow

### 1. Confirm scope and success criteria

1. List windows and whether any still need Node in renderer (goal: zero).
2. Success: all production windows isolated + sandboxed; feature parity via IPC.

### 2. Inventory current isolation state

```bash
rg -n "contextIsolation|nodeIntegration|contextBridge|preload" --glob '!node_modules'
```

1. For each `BrowserWindow`, record webPreferences.
2. List globals previously used from renderer (`require`, `process`, `fs`, etc.).

### 3. Baseline breakage

1. Run app with isolation enabled in a branch; catalog runtime errors.
2. Map each broken feature to a future IPC method.
3. Note any `remote` module usage (remove—deprecated/insecure patterns).

### 4. Implement preload bridge

```js
// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  getVersion: () => ipcRenderer.invoke('app:getVersion'),
  saveFile: (payload) => ipcRenderer.invoke('file:save', payload),
});
```

```js
// main.js
const { ipcMain, app } = require('electron');

ipcMain.handle('app:getVersion', () => app.getVersion());

ipcMain.handle('file:save', async (event, payload) => {
  assertSenderIsApp(event);
  validateSavePayload(payload); // schema!
  return writeInUserData(payload);
});
```

```js
// renderer (no Node)
const version = await window.api.getVersion();
```

1. Do **not** expose `ipcRenderer` wholesale.
2. Prefer `invoke`/`handle` over free-form `send` for request/response.
3. Validate sender frame URL when multiple origins exist.

### 5. Enable sandbox

```js
webPreferences: {
  preload: path.join(__dirname, 'preload.js'),
  contextIsolation: true,
  nodeIntegration: false,
  sandbox: true,
}
```

1. Sandboxed preloads cannot use some Node APIs—move logic to main.
2. Native modules generally do not belong in preload under sandbox.

### 6. Verify with evidence

```bash
rg -n "nodeIntegration:\\s*true|contextIsolation:\\s*false" --glob '!node_modules'
# In renderer DevTools (lab): typeof require === 'undefined'
```

1. XSS lab payload cannot call Node or expand bridge beyond exposed methods.
2. Fuzz IPC handlers with unexpected types/sizes.
3. Automated smoke: critical flows use `window.api.*` only.

### 7. Hand off

1. Document the public renderer API surface like a versioned SDK.
2. PR checklist: no new `nodeIntegration` exceptions without security review.
3. Cross-link fuses that lock runtime options where applicable.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Bridge | Few typed functions | `exposeInMainWorld('electron', process)` |
| Isolation | Always on | Off for “easier debugging” in prod |
| Validation | Schema in main | Trust renderer JSON blindly |
| remote | Removed | `@electron/remote` for convenience |
| Errors | Sanitized messages | Stack traces from main to web content |

## Output Checklist

- [ ] All windows use contextIsolation + no nodeIntegration
- [ ] Sandbox enabled or exception documented
- [ ] Preload API inventoried and minimal
- [ ] IPC handlers validate sender + payload
- [ ] Legacy `require` in renderer eliminated
- [ ] XSS/isolation lab evidence recorded
- [ ] Renderer API docs updated
- [ ] Residual risk noted

## Rules

- Owned apps only for invasive testing.
- Never re-enable nodeIntegration to “save time.”
- Treat preload as privileged code under review.
- Keep secrets in main process / OS secure storage, not renderer state.
- Route broader Electron issues to `electron-app-security`.
