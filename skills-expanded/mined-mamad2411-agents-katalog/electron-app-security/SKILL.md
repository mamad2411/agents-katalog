---
name: electron-app-security
description: >
  Authorized Electron desktop app security review: nodeIntegration,
  contextIsolation, sandbox, preload bridges, shell.openExternal, navigation and
  webview risks, and renderer XSS to OS/code execution. Use when assessing
  Electron BrowserWindow / webPreferences on apps you own or are scoped to harden.
---

# Electron App Security

## Scope And Authorization

- **In scope:** Electron apps you own, ship, or are contracted to review with written scope.
- **Out of scope:** Weaponizing client apps against third parties; reverse-engineering competitors without authorization.
- Treat renderer XSS as RCE-adjacent when isolation is weak—test only in lab builds.
- Redact license keys, update tokens, and user data from reports.
- Pair code changes with `code-quality-standards` and deeper skills for fuses/asar/isolation.

## When To Use

- Security review of main/renderer/preload architecture.
- Hardening `webPreferences` defaults across all `BrowserWindow` / `BrowserView` / `webview` tags.
- Auditing `shell.openExternal`, custom protocols, and IPC surfaces.
- Mapping XSS → privilege paths before shipping.
- Baseline before specialized work on fuses, asar integrity, or contextIsolation refactors.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| contextIsolation + preload API design only | `electron-context-isolation` |
| Electron fuses flip/verify | `electron-fuses` |
| asar integrity / unpack risks | `electron-asarsecurity` |
| Generic web XSS | `xss-cross-site-scripting` |
| Implementation quality baseline | `code-quality-standards` |
| Auto-update package signing detail | packaging/signing skills |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Renderer | `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true` |
| Preload | Minimal `contextBridge` API; validate all IPC |
| Navigation | Deny unexpected `will-navigate` / `setWindowOpenHandler` |
| External | Allowlist schemes/hosts for `openExternal` |
| Content | Prefer local `loadFile`/`loadURL` app origin; CSP |
| WebView | Avoid or isolate; never guest with nodeIntegration |

## Workflow

### 1. Confirm scope and success criteria

1. Electron major version, packaging (electron-builder/forge), update channel.
2. Success: secure defaults on every window; no privileged IPC from untrusted HTML; external open allowlisted.

### 2. Inventory windows and preferences

```bash
# Find BrowserWindow / webPreferences
rg -n "BrowserWindow|webPreferences|nodeIntegration|contextIsolation|sandbox" --glob '!node_modules'
rg -n "shell\\.openExternal|webview|registerSchemesAsPrivileged" --glob '!node_modules'
```

1. List every place windows are created (including hidden/background).
2. Note remote content loading (http(s) marketing pages inside the shell).

### 3. Baseline threat paths

| Path | Risk if misconfigured |
| --- | --- |
| XSS in renderer + nodeIntegration | Arbitrary Node/OS commands |
| XSS + weak preload | Abuse exposed IPC to main |
| openExternal(user) | Open attacker `file:`/`smb:`/`evil:` handlers |
| Unchecked navigation | Phishing page inside trusted chrome |
| Disabled webSecurity | Cross-origin reads / weakened isolation |

### 4. Apply secure defaults

```js
const win = new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
    contextIsolation: true,
    nodeIntegration: false,
    nodeIntegrationInWorker: false,
    sandbox: true,
    webSecurity: true,
    allowRunningInsecureContent: false,
  },
});

win.webContents.setWindowOpenHandler(({ url }) => {
  // open external browser only for allowlisted https
  return { action: 'deny' };
});

win.webContents.on('will-navigate', (e, url) => {
  if (!isAllowedAppUrl(url)) e.preventDefault();
});
```

```js
// main: validate before openExternal
const { shell } = require('electron');
function openSafe(url) {
  const u = new URL(url);
  if (u.protocol !== 'https:' || !ALLOW.has(u.hostname)) {
    throw new Error('blocked external url');
  }
  return shell.openExternal(u.toString());
}
```

1. Enable CSP on loaded documents where possible.
2. Prefer IPC with schema validation (zod/io-ts) over free-form strings.
3. Do not enable `experimentalFeatures` or disable `webSecurity` for convenience.

### 5. Review preload and IPC

1. `contextBridge.exposeInMainWorld` only stable, narrow functions.
2. Main process handlers authenticate capability (which window / which user session).
3. Never pass Node module handles or `require` into the renderer.

### 6. Verify with evidence

```bash
npm audit --omit=dev
# Manual checklist signed off in PR
rg -n "nodeIntegration:\\s*true|contextIsolation:\\s*false|sandbox:\\s*false" --glob '!node_modules'
```

1. Attempt XSS in a lab page: confirm no Node access and limited IPC.
2. Confirm navigation to `https://evil.example` is blocked in-window.
3. Document any intentional exception (e.g. internal admin tool) with owner + expiry.

### 7. Hand off

1. Link to `electron-context-isolation`, `electron-fuses`, `electron-asarsecurity` for depth.
2. Dependency update policy for `electron` major versions.
3. Crash/telemetry redaction for security events.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| webPreferences | isolation + sandbox + no node | `nodeIntegration: true` |
| Content | Local app origin + CSP | Full remote site as main UI with Node |
| openExternal | Host allowlist | Pass through any string |
| IPC | Validated channels | `ipcRenderer.send` executes shell |
| WebView | Avoid / guest sandbox | nodeIntegration in webview |

## Output Checklist

- [ ] All BrowserWindow sites inventoried
- [ ] Secure webPreferences defaults applied
- [ ] Navigation and window-open handlers deny-by-default
- [ ] openExternal allowlisted
- [ ] Preload surface minimal and reviewed
- [ ] XSS-to-privilege lab notes captured
- [ ] Exceptions documented with owner/expiry
- [ ] Residual risk and Electron version noted

## Rules

- Authorized apps only.
- Renderer is untrusted; main is privileged—design boundaries accordingly.
- Never ship secrets in renderer bundles when avoidable.
- Use specialized Electron skills for fuses/asar/isolation deep dives.
- Evidence: config greps + test notes, not “we use Electron so it’s fine.”
