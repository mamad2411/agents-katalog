---
name: electrobun-app-shell
description: "Windows, views, native UI, and system APIs for Electrobun desktop apps. Covers BrowserWindow, BrowserView, GpuWindow, Tray, ApplicationMenu, ContextMenu, clipboard, dialogs, notifications, paths, GlobalShortcut, Screen, Session. Use when creating windows, managing views, building native UI, or accessing system APIs."
---

# Electrobun App Shell — Windows, Views, Native UI & System APIs

> **Electrobun is NOT Electron.** It has its own APIs, Bun runtime, native FFI, and a fundamentally different architecture. Do not use Electron APIs (`ipcMain`, `app.on('ready')`, `BrowserWindow.loadURL()`, etc.).

## Decision Tree

| Need | Pattern |
|---|---|
| Create a window | `new BrowserWindow({ ... })` — auto-creates a `BrowserView` |
| Access the window's webview | `win.webview` (getter for the auto-created `BrowserView`) |
| Add extra views to a window | `new BrowserView({ windowId: win.id, ... })` |
| Embed web content in HTML | `<electrobun-webview src="...">` (OOPIF webview tag) |
| Need GPU rendering | `new GpuWindow({ ... })` — auto-creates a `WGPUView` |
| System tray icon | `new Tray({ ... })` with `tray.setMenu([...])` |
| App menu bar | `ApplicationMenu.setApplicationMenu([...])` |
| Right-click menu | `ContextMenu.showContextMenu([...])` |
| Clipboard read/write | `Utils.clipboardReadText()` / `Utils.clipboardWriteText(text)` |
| File open dialog | `Utils.openFileDialog({ ... })` |
| Alert / confirm dialog | `Utils.showMessageBox({ ... })` |
| Desktop notification | `Utils.showNotification({ ... })` |
| OS paths (home, appData) | `Utils.paths.home`, `Utils.paths.userData`, etc. |
| Global keyboard shortcut | `GlobalShortcut.register(accelerator, callback)` |
| Display/monitor info | `Screen.getPrimaryDisplay()`, `Screen.getAllDisplays()` |
| Cookie/storage management | `Session.defaultSession.cookies.get(...)` |
| Open URL in browser | `Utils.openExternal(url)` |
| Quit the app | `Utils.quit()` |

## Window ↔ View Relationship Model

```
BrowserWindow (native OS window)
  └── BrowserView (auto-created, fills window)
        ├── Loads URL/HTML, runs preload scripts
        ├── Has RPC bridge to Bun process
        └── Can contain <electrobun-webview> tags (OOPIFs)

GpuWindow (native OS window for GPU)
  └── WGPUView (auto-created, WebGPU surface)
```

- When you call `new BrowserWindow(opts)`, a `BrowserView` is **automatically created** and attached.
- Access it via `win.webview` — this returns the `BrowserView` instance.
- `BrowserWindow` has **no `loadURL()` method**. Use `win.webview.loadURL(url)` to navigate.
- URL is typically set at construction via `{ url: "views://viewname/index.html" }`.
- On window close, all attached views are cleaned up automatically.
- If `exitOnLastWindowClosed` is `true` (default), the app quits when all windows close.

## Canonical Patterns

### Import Paths

```ts
// Bun process (src/bun/*.ts) — ALWAYS use "electrobun/bun"
import { BrowserWindow, BrowserView, Tray, ApplicationMenu, ContextMenu,
         Utils, GlobalShortcut, Screen, Session } from "electrobun/bun";
import Electrobun from "electrobun/bun";

// View process (src/viewname/*.ts) — ALWAYS use "electrobun/view"
import Electrobun, { Electroview } from "electrobun/view";
```

### Basic Window

```ts
const win = new BrowserWindow({
  title: "My App",
  url: "views://mainview/index.html",
  frame: { width: 800, height: 600, x: 200, y: 200 },
});
```

### Custom Titlebar Window

```ts
const win = new BrowserWindow({
  title: "Custom Chrome",
  url: "views://mainview/index.html",
  titleBarStyle: "hidden",  // no native chrome
  frame: { width: 900, height: 700, x: 100, y: 100 },
});

// In HTML, make a region draggable:
// <div style="-webkit-app-region: drag">My Titlebar</div>
// Or use class: <div class="electrobun-webkit-app-region-drag">
// Opt-out within drag region: <button class="electrobun-webkit-app-region-no-drag">
```

### Transparent / Overlay Window

```ts
const overlay = new BrowserWindow({
  title: "Overlay",
  url: "views://overlay/index.html",
  transparent: true,
  passthrough: true,         // mouse clicks pass through transparent areas
  titleBarStyle: "hidden",
  frame: { width: 400, height: 300, x: 100, y: 100 },
});
```

### Hidden Inset Titlebar (macOS Traffic Lights)

```ts
const win = new BrowserWindow({
  title: "Inset Controls",
  url: "views://mainview/index.html",
  titleBarStyle: "hiddenInset",  // transparent titlebar, native controls inset
  frame: { width: 800, height: 600, x: 200, y: 200 },
});
```

### Window with RPC

```ts
import { BrowserWindow, BrowserView, type RPCSchema } from "electrobun/bun";

type MyRPC = {
  bun: RPCSchema<{
    requests: {
      getData: { params: { id: string }; response: { name: string } };
    };
    messages: {};
  }>;
  webview: RPCSchema<{
    requests: {};
    messages: {
      updateUI: { items: string[] };
    };
  }>;
};

const rpc = BrowserView.defineRPC<MyRPC>({
  maxRequestTime: 5000,
  handlers: {
    requests: {
      getData: ({ id }) => ({ name: "Item " + id }),
    },
    messages: {},
  },
});

const win = new BrowserWindow({
  title: "RPC App",
  url: "views://mainview/index.html",
  rpc,
  frame: { width: 800, height: 600, x: 200, y: 200 },
});

// Send message to view (after dom-ready)
win.webview.on("dom-ready", () => {
  win.webview.rpc?.send?.updateUI({ items: ["a", "b", "c"] });
});
```

### Window Events

```ts
// Instance events (scoped to a specific window)
win.on("close", (event) => { /* cleanup */ });
win.on("resize", (event) => {
  // event.data: { id, x, y, width, height }
});
win.on("move", (event) => {
  // event.data: { id, x, y }
});
win.on("focus", (event) => { /* window gained focus */ });
win.on("blur", (event) => { /* window lost focus */ });
win.on("keyDown", (event) => {
  // event.data: { id, keyCode, modifiers, isRepeat }
});
win.on("keyUp", (event) => {
  // event.data: { id, keyCode, modifiers, isRepeat }
});
```

### BrowserView Events

```ts
win.webview.on("will-navigate", (event) => { /* before navigation */ });
win.webview.on("did-navigate", (event) => { /* after navigation */ });
win.webview.on("did-navigate-in-page", (event) => { /* hash/pushState */ });
win.webview.on("did-commit-navigation", (event) => { /* committed */ });
win.webview.on("dom-ready", (event) => { /* DOM ready — safe to send data */ });

// Download events
win.webview.on("download-started", (event) => { });
win.webview.on("download-progress", (event) => { });
win.webview.on("download-completed", (event) => { });
win.webview.on("download-failed", (event) => { });
```

### BrowserView Operations

```ts
win.webview.loadURL("https://example.com");
win.webview.loadHTML("<h1>Hello</h1>");
win.webview.executeJavascript("document.title");
win.webview.openDevTools();
win.webview.closeDevTools();
win.webview.toggleDevTools();
win.webview.findInPage("search text", { forward: true, matchCase: false });
win.webview.stopFindInPage();
win.webview.setPageZoom(1.5);  // 150%
```

### Adding Extra Views to a Window

```ts
const extraView = new BrowserView({
  url: "views://sidebar/index.html",
  windowId: win.id,
  frame: { x: 0, y: 0, width: 300, height: 600 },
  autoResize: false,
});
```

### Sandbox Mode (Untrusted Content)

```ts
// Bun side — load remote URL in sandbox
const win = new BrowserWindow({
  url: "https://untrusted-site.com",
  sandbox: true,   // disables RPC, no bunBridge, no webview tags
  frame: { width: 800, height: 600, x: 200, y: 200 },
});

// HTML — sandbox a webview tag
// <electrobun-webview src="https://untrusted-site.com" sandbox></electrobun-webview>

// Use partition for storage isolation:
// <electrobun-webview src="..." sandbox partition="persist:untrusted"></electrobun-webview>
```

### Navigation Rules

```ts
// Allow only specific domains (last match wins)
const win = new BrowserWindow({
  url: "views://mainview/index.html",
  navigationRules: JSON.stringify([
    "^*",                        // block everything by default
    "https://myapp.com/*",       // then allow myapp.com
    "views://*",                 // allow views:// protocol
  ]),
  frame: { width: 800, height: 600, x: 200, y: 200 },
});

// Update rules dynamically on the view
win.webview.setNavigationRules([
  "^*",
  "https://allowed.com/*",
]);
```

### System Tray

```ts
const tray = new Tray({
  title: "My App",
  image: "views://assets/icon-template.png",
  template: true,    // macOS template image
  width: 16,
  height: 16,
});

tray.setMenu([
  { type: "normal", label: "Show Window", action: "show" },
  { type: "divider" },
  { type: "normal", label: "Settings", action: "settings", submenu: [
    { type: "normal", label: "General", action: "settings-general" },
    { type: "normal", label: "Advanced", action: "settings-advanced" },
  ]},
  { type: "divider" },
  { type: "normal", label: "Quit", action: "quit" },
]);

tray.on("tray-clicked", (event) => {
  switch (event.data?.action) {
    case "show": win.focus(); break;
    case "quit": tray.remove(); Utils.quit(); break;
  }
});

// Tray-only app: set exitOnLastWindowClosed: false in electrobun.config.ts
// runtime: { exitOnLastWindowClosed: false }
```

### Application Menu

```ts
ApplicationMenu.setApplicationMenu([
  {
    submenu: [
      { label: "About", role: "about" },
      { type: "separator" },
      { label: "Quit", role: "quit", accelerator: "q" },
    ],
  },
  {
    label: "Edit",
    submenu: [
      { role: "undo" },
      { role: "redo" },
      { type: "separator" },
      { role: "cut" },
      { role: "copy" },
      { role: "paste" },
      { role: "selectAll" },
    ],
  },
  {
    label: "Custom",
    submenu: [
      { label: "My Action", action: "my-action", accelerator: "CommandOrControl+T" },
      { label: "Disabled", action: "disabled", enabled: false },
      { label: "Checked", action: "checked", checked: true },
    ],
  },
]);

// Handle clicks (global event)
Electrobun.events.on("application-menu-clicked", (e) => {
  console.log(e.data.action, e.data.data);
});
```

### Context Menu

```ts
ContextMenu.showContextMenu([
  { label: "Copy", role: "copy" },
  { label: "Custom", action: "my-action", data: { key: "value" } },
  { type: "separator" },
  { label: "Submenu", submenu: [
    { label: "Sub Item", action: "sub-item" },
  ]},
]);

Electrobun.events.on("context-menu-clicked", (e) => {
  console.log(e.data.action, e.data.data);
});
```

### Clipboard

```ts
// Text
const text = Utils.clipboardReadText();      // string | null
Utils.clipboardWriteText("Hello clipboard");

// Image (PNG data)
const imgData = Utils.clipboardReadImage();  // Uint8Array | null
Utils.clipboardWriteImage(pngBytes);

// Inspect & clear
const formats = Utils.clipboardAvailableFormats();  // e.g. ["text", "image"]
Utils.clipboardClear();
```

### File Dialog

```ts
const paths = await Utils.openFileDialog({
  startingFolder: "~/Documents",
  allowedFileTypes: "*.txt;*.md",
  canChooseFiles: true,
  canChooseDirectory: false,
  allowsMultipleSelection: true,
});
// paths: string[]
```

### Message Box

```ts
const { response } = await Utils.showMessageBox({
  type: "question",
  title: "Confirm Delete",
  message: "Delete this file?",
  detail: "This cannot be undone.",
  buttons: ["Delete", "Cancel"],
  defaultId: 1,     // focused button index
  cancelId: 1,      // Escape key button index
});
if (response === 0) { /* user clicked Delete */ }
```

### Notifications

```ts
Utils.showNotification({
  title: "Download Complete",
  body: "myfile.zip has been saved",
  subtitle: "Downloads",  // macOS only
  silent: false,
});
```

### Global Shortcuts

```ts
GlobalShortcut.register("CommandOrControl+Shift+Space", () => {
  console.log("Shortcut triggered!");
});

GlobalShortcut.isRegistered("CommandOrControl+Shift+Space"); // true
GlobalShortcut.unregister("CommandOrControl+Shift+Space");
GlobalShortcut.unregisterAll();
```

### Paths API

```ts
// OS-level paths
Utils.paths.home;        // home directory
Utils.paths.appData;     // ~/Library/Application Support (macOS)
Utils.paths.config;      // ~/.config (Linux), ~/Library/Application Support (macOS)
Utils.paths.cache;       // ~/Library/Caches (macOS)
Utils.paths.temp;        // OS temp directory
Utils.paths.logs;        // ~/Library/Logs (macOS)
Utils.paths.documents;   // ~/Documents
Utils.paths.downloads;   // ~/Downloads
Utils.paths.desktop;     // ~/Desktop

// App-scoped paths (uses identifier + channel from version.json)
Utils.paths.userData;    // <appData>/<identifier>/<channel>
Utils.paths.userCache;   // <cache>/<identifier>/<channel>
Utils.paths.userLogs;    // <logs>/<identifier>/<channel>
```

### Screen API

```ts
const primary = Screen.getPrimaryDisplay();
// { id, bounds: {x,y,width,height}, workArea: {x,y,width,height}, scaleFactor, isPrimary }

const displays = Screen.getAllDisplays();  // Display[]
const cursor = Screen.getCursorScreenPoint();  // { x, y }
```

### Session / Cookies

```ts
const session = Session.defaultSession;  // or Session.fromPartition("persist:myapp")

session.cookies.set({
  name: "auth", value: "token123", domain: ".example.com",
  secure: true, httpOnly: true, sameSite: "lax",
});

const cookies = session.cookies.get({ domain: ".example.com" });
session.cookies.remove("https://example.com", "auth");
session.cookies.clear();

session.clearStorageData(["localStorage", "cookies"]);  // or "all"
```

### File Operations & Misc

```ts
Utils.openExternal("https://example.com");   // open in default browser
Utils.openPath("/path/to/file");             // open with default app
await Utils.moveToTrash("/path/to/file");
await Utils.showItemInFolder("/path/to/file");

// Dock (macOS)
Utils.setDockIconVisible(false);
Utils.isDockIconVisible();

// Quit with lifecycle hooks
Electrobun.events.on("app.beforeQuit", (event) => {
  event.response = { allow: false };  // cancel quit
});
Utils.quit();
```

## Menu Item Types

### ApplicationMenuItemConfig (ApplicationMenu & ContextMenu)

Items can have a `role` (native behavior) **or** an `action` (custom handler) — never both.

```ts
// Role-based (native handles it, label auto-fills)
{ role: "copy" }
{ role: "quit", accelerator: "q" }

// Action-based (custom handler via events)
{ label: "My Action", action: "do-thing", data: { key: "value" }, accelerator: "CommandOrControl+T" }

// Divider
{ type: "separator" }   // or "divider" — both accepted, normalized internally

// Common roles: about, quit, hide, hideOthers, showAll, minimize, zoom, close,
//   undo, redo, cut, copy, paste, pasteAndMatchStyle, delete, selectAll,
//   toggleFullScreen, startSpeaking, stopSpeaking, showHelp
```

### MenuItemConfig (Tray only)

Tray menus do **not** support `role` or `accelerator` — action-only.

```ts
{ type: "normal", label: "Click Me", action: "my-action", data: { id: 1 } }
{ type: "divider" }
```

## Non-Negotiable Rules

1. **Always import from `"electrobun/bun"` in the Bun process** and `"electrobun/view"` in webview code. Never cross-import.
2. **BrowserWindow has no `loadURL()` method.** Use `win.webview.loadURL(url)` to navigate the attached BrowserView.
3. **Use `views://` protocol for local HTML/assets.** Never use `file://` or absolute paths for view content. The `copy` config in `electrobun.config.ts` maps source → `views/` output.
4. **Always specify `frame: { width, height, x, y }`** when creating windows for predictable positioning.
5. **Tray-only apps must set `runtime.exitOnLastWindowClosed: false`** in `electrobun.config.ts` or the app quits immediately.
6. **Use `dom-ready` event to send initial data to views** — the view is not ready to receive messages before this.
7. **Menu items use `role` OR `action`, never both.** If `role` is set, native handles the action. If `action` is set, you must listen for the event.
8. **Sandbox mode disables RPC entirely.** Sandboxed views can only emit basic events — no `bunBridge`, no webview tags, no drag regions.
9. **Navigation rules use "last match wins" semantics.** Prefix with `^` to block. Default (no match) is allow.
10. **This is NOT Electron.** No `ipcMain`/`ipcRenderer`, no `app.on('ready')`, no `webContents`, no `protocol.registerSchemeAsPrivileged`.

## Platform Limitations

| Feature | macOS | Windows | Linux |
|---|---|---|---|
| ApplicationMenu | ✅ | ✅ | ❌ Not supported |
| ContextMenu | ✅ | ✅ | ❌ Not supported |
| Tray | ✅ | ✅ | ✅ |
| `titleBarStyle: "hiddenInset"` | ✅ (traffic lights) | Partial | Partial |
| `styleMask` options | ✅ (NSWindowStyleMask) | ❌ | ❌ |
| Dock icon control | ✅ | ❌ | ❌ |
| Notification subtitle | ✅ | ❌ | ❌ |
| `renderer: "native"` | WKWebView | WebView2 | N/A |
| `renderer: "cef"` | ✅ | ✅ | ✅ |

## Common Pitfalls

### 1. Calling `win.loadURL()` instead of `win.webview.loadURL()`

```ts
// ❌ WRONG — BrowserWindow has no loadURL method
win.loadURL("https://example.com");

// ✅ CORRECT — use the attached BrowserView
win.webview.loadURL("https://example.com");
```

### 2. Forgetting exitOnLastWindowClosed for tray apps

```ts
// ❌ App quits immediately because no windows are open
const tray = new Tray({ title: "My App" });

// ✅ Set in electrobun.config.ts:
// runtime: { exitOnLastWindowClosed: false }
```

### 3. Sending data to view before dom-ready

```ts
// ❌ View may not be ready
const win = new BrowserWindow({ url: "views://main/index.html", ... });
win.webview.rpc?.send?.updateUI({ data: "hello" });

// ✅ Wait for dom-ready
win.webview.on("dom-ready", () => {
  win.webview.rpc?.send?.updateUI({ data: "hello" });
});
```

### 4. Using roles in Tray menus

```ts
// ❌ Tray MenuItemConfig does not support roles
tray.setMenu([{ role: "quit" }]);

// ✅ Use action-based items
tray.setMenu([{ type: "normal", label: "Quit", action: "quit" }]);
tray.on("tray-clicked", (e) => {
  if (e.data?.action === "quit") Utils.quit();
});
```

### 5. Using file:// paths instead of views:// protocol

```ts
// ❌ WRONG
new BrowserWindow({ url: "file:///path/to/index.html", ... });

// ✅ CORRECT — views:// maps to built output
new BrowserWindow({ url: "views://mainview/index.html", ... });
```

### 6. Missing type: "normal" in Tray menu items

```ts
// ❌ Ambiguous — type is required for Tray MenuItemConfig
tray.setMenu([{ label: "Click", action: "click" }]);

// ✅ Explicit type
tray.setMenu([{ type: "normal", label: "Click", action: "click" }]);
```

### 7. ApplicationMenu on Linux

```ts
// ❌ Does nothing on Linux
ApplicationMenu.setApplicationMenu([...]);

// ✅ Check platform or implement menu in HTML for Linux
if (process.platform !== "linux") {
  ApplicationMenu.setApplicationMenu([...]);
}
```

### 8. Multi-window cleanup

```ts
// ❌ Leaked reference — child window stays in map after close
const children = new Map<number, BrowserWindow>();
const child = new BrowserWindow({ ... });
children.set(child.id, child);

// ✅ Clean up on close
child.on("close", () => {
  children.delete(child.id);
});
```
