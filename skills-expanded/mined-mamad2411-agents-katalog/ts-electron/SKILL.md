---
name: ts-electron
description: Use when building desktop apps with Electron — main/renderer/preload, context isolation + IPC security, electron-builder packaging, auto-update.
metadata:
  added: 2026-05-23
  last_reviewed: 2026-05-23
  type: language
  languages: [typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-23"
  related: [typescript, node-essentials, ts-vite, security]
---

# TS Electron 42

**Iron Law: the renderer is hostile. `contextIsolation: true`, `sandbox: true`, `nodeIntegration: false` — non-negotiable. Expose a tiny typed surface through `contextBridge`, validate every IPC argument main-side, and never ship an unsigned auto-update.**

## Process model — three contexts, one trust boundary

| Process      | Runs                                            | Privilege                                                  | Holds                                           |
| ------------ | ----------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------- |
| **Main**     | Node.js, full OS access                         | Trusted — the only place with `fs`, `net`, `child_process` | `BrowserWindow`, `app`, `ipcMain`, your secrets |
| **Preload**  | Isolated context, limited Node before page load | Bridge — `contextBridge` only                              | The typed API you choose to expose              |
| **Renderer** | Chromium, your web app                          | Untrusted — treat like a browser tab                       | DOM, your UI, **whatever XSS gets injected**    |

The renderer can load remote content, run your bundled JS, or be hijacked by XSS. The main process is the trust boundary — exactly like a server. Preload is the _only_ legitimate channel between them, and it must hand the renderer a minimal, validated API — never raw `ipcRenderer`, never `require`.

## BrowserWindow — secure defaults

```ts
// main.ts
import { app, BrowserWindow, shell } from "electron";
import path from "node:path";

const isDev = !app.isPackaged;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true, // SEPARATE JS worlds — default since E12, keep it
      sandbox: true, // renderer runs in OS sandbox, no Node primitives
      nodeIntegration: false, // no require() in the page
      webSecurity: true, // never disable — turns off same-origin + CSP
    },
  });

  // Load your own app, not arbitrary URLs.
  if (isDev) win.loadURL("http://localhost:5173");
  else win.loadFile(path.join(__dirname, "../renderer/index.html"));

  // External links open in the OS browser, never a node-enabled window.
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("https://")) shell.openExternal(url);
    return { action: "deny" };
  });
  return win;
}

// One instance only — second launch focuses the existing window.
if (!app.requestSingleInstanceLock()) app.quit();
else {
  app.on("second-instance", () => {
    const [win] = BrowserWindow.getAllWindows();
    if (win) {
      if (win.isMinimized()) win.restore();
      win.focus();
    }
  });
  app.whenReady().then(createWindow);
  app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
  });
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
}
```

## IPC — typed `invoke`/`handle`, never raw bridge

Prefer request/response (`invoke`/`handle`) over fire-and-forget (`send`/`on`): you get a typed return value and error propagation. Expose named methods, never `ipcRenderer` itself.

```ts
// preload.ts — the entire renderer-visible API
import { contextBridge, ipcRenderer } from "electron";

const api = {
  readNote: (id: string) => ipcRenderer.invoke("note:read", id) as Promise<string>,
  saveNote: (id: string, body: string) => ipcRenderer.invoke("note:save", id, body) as Promise<void>,
  // Subscriptions: wrap, strip the IpcRendererEvent, return an unsubscribe fn.
  onSync: (cb: (n: number) => void) => {
    const h = (_e: unknown, n: number) => cb(n);
    ipcRenderer.on("sync:progress", h);
    return () => ipcRenderer.off("sync:progress", h);
  },
};
contextBridge.exposeInMainWorld("desktop", api);
export type DesktopApi = typeof api; // import in renderer for `window.desktop` types
```

```ts
// main.ts — handlers are the trust boundary. Validate EVERYTHING.
import { app, ipcMain } from "electron";

ipcMain.handle("note:save", (event, id: unknown, body: unknown) => {
  // 1. Sender check — only frames YOU loaded may call privileged IPC.
  const url = event.senderFrame?.url ?? "";
  // file:// is the packaged renderer; allow localhost ONLY in dev (Vite), never in a shipped build.
  const ok = url.startsWith("file://") || (!app.isPackaged && url.startsWith("http://localhost:"));
  if (!ok) throw new Error("unauthorized sender");
  // 2. Argument validation — args cross a process boundary; assume hostile.
  if (typeof id !== "string" || !/^[a-z0-9-]{1,64}$/.test(id)) throw new Error("bad id");
  if (typeof body !== "string" || body.length > 1_000_000) throw new Error("bad body");
  return db.saveNote(id, body); // resolves to renderer; rejects propagate as a rejected Promise
});
```

Errors thrown in a handler reject the renderer's `invoke` Promise — return generic messages, log details main-side. Never interpolate IPC strings into `fs` paths or shell commands without validation; that's how a renderer XSS becomes arbitrary file write.

## Bundling — esbuild for main + preload

Main and preload are Node/CommonJS and must be bundled separately from the renderer (the renderer goes through Vite — `Skill(devkit:ts-vite)`).

```bash
# Bundle main + preload; renderer is built by Vite.
esbuild src/main.ts src/preload.ts \
  --bundle --platform=node --format=cjs \
  --external:electron --outdir=dist
```

`--external:electron` keeps Electron's built-ins out of the bundle. Preload runs in the isolated world: keep it tiny — no app logic, just the bridge.

## CSP — lock the renderer down

Set a strict policy via `session.defaultSession.webRequest.onHeadersReceived` or a `<meta>` tag. No `unsafe-inline`, no `unsafe-eval`, no wildcard `connect-src`:

```ts
session.defaultSession.webRequest.onHeadersReceived((details, cb) => {
  cb({
    responseHeaders: {
      ...details.responseHeaders,
      "Content-Security-Policy": [
        "default-src 'self'; connect-src 'self' https://api.example.com; img-src 'self' data:",
      ],
    },
  });
});
```

## Packaging — electron-builder 26

```jsonc
// electron-builder.json (or "build" key in package.json)
{
  "appId": "com.example.app",
  "productName": "MyApp",
  "files": ["dist/**/*", "package.json"],
  "mac": { "target": ["dmg", "zip"], "hardenedRuntime": true, "category": "public.app-category.productivity" },
  "win": { "target": ["nsis"] },
  "linux": { "target": ["AppImage", "deb"], "category": "Utility" },
  "publish": { "provider": "github" },
}
```

Run `electron-builder --mac --win --linux` (cross-target needs the right host or CI). **Code signing is mandatory for distribution**: macOS needs a Developer ID cert + notarization (`hardenedRuntime: true`, `afterSign` notarize hook) or Gatekeeper blocks the app; Windows needs an Authenticode cert (EV avoids SmartScreen warnings) — set `CSC_LINK`/`CSC_KEY_PASSWORD` in CI. Linux AppImage needs no signing.

## Auto-update — electron-updater 6

```ts
// main.ts — checks the GitHub Releases (`publish.provider: github`) feed.
import { autoUpdater } from "electron-updater";

app.whenReady().then(() => {
  autoUpdater.checkForUpdatesAndNotify();
});
autoUpdater.on("update-downloaded", () => autoUpdater.quitAndInstall());
```

electron-updater verifies the **code signature** of the downloaded artifact before applying it — which is exactly why unsigned builds are a security hole: a tampered update installs silently. The GitHub provider reads `latest.yml`/`latest-mac.yml` that `electron-builder` publishes alongside the binaries. Never roll your own download-and-exec; that's a self-inflicted RCE.

## Anti-patterns

- `nodeIntegration: true` — any renderer XSS gets `require("child_process")`. Game over.
- `contextIsolation: false` — preload and page share a JS world; the page can rewrite your bridge.
- Loading remote/3rd-party content in a node-enabled or non-sandboxed renderer — that's a browser with OS access.
- `ipcMain.on("do-thing", handler)` with no `event.senderFrame` check and no arg validation — any frame, any payload.
- `webSecurity: false` / `allowRunningInsecureContent` "for dev" — disables same-origin + CSP; ships to prod.
- Exposing `ipcRenderer` or `require` through `contextBridge` — defeats the entire bridge.
- Shipping unsigned auto-updates — a MITM or compromised release serves a backdoor to every install.
- Secrets (API keys, signing tokens) bundled into the renderer — extractable with devtools in seconds; keep them main-side.
- `shell.openExternal(userControlledUrl)` without a scheme allow-list — `file://`/custom-scheme abuse.

## Red flags

| Thought                                          | Reality                                                    |
| ------------------------------------------------ | ---------------------------------------------------------- |
| "It's a desktop app, the renderer is mine"       | The renderer is a browser tab — XSS there = code on the OS |
| "I'll just enable nodeIntegration, it's simpler" | You traded the entire OS for five lines saved in preload   |
| "Sender checks are overkill for a local app"     | Sub-frames and injected iframes call your IPC too          |
| "We'll sign the build before 1.0"                | Unsigned auto-update = silent RCE on every machine, now    |
| "CSP breaks my inline scripts, I'll drop it"     | Inline scripts are exactly the XSS vector CSP stops        |

## Hand-off

For the renderer's Vite build (dev server, env vars, manual chunks): `Skill(devkit:ts-vite)`. For the main-process Node side (event loop, ESM/CJS interop, profiling): `Skill(devkit:node-essentials)`. For TypeScript strict-mode rules the typed bridge depends on: `Skill(devkit:typescript)`. For the threat model behind these defaults (XSS, supply chain, signing): `Skill(devkit:security)`.
