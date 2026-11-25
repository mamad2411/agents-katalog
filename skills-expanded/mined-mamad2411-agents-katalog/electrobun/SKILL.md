---
name: electrobun
description: "Desktop app framework using Bun + native webview/CEF. Routes to sub-skills for app shell (windows, views, menus, system APIs), RPC (typed bidirectional communication), and release (build, packaging, updates). Use when building Electrobun desktop apps."
---

# Electrobun

Desktop app framework using Bun runtime + native webview/CEF + Zig native bindings. Complete solution for building, updating, and shipping cross-platform desktop applications in TypeScript.

**CRITICAL: Electrobun is NOT Electron. Never use Electron APIs (ipcMain, ipcRenderer, app.on('ready'), webContents, etc.).**

## Sub-Skill Routing

| Need | Load Skill | Trigger Phrases |
|------|-----------|----------------|
| Windows, views, menus, tray, system APIs | `electrobun-app-shell` | BrowserWindow, BrowserView, Tray, ApplicationMenu, ContextMenu, clipboard, notifications, GlobalShortcut, Screen, Session, file dialogs, GpuWindow |
| RPC, typed communication, schemas | `electrobun-rpc` | createRPC, defineElectrobunRPC, RPCSchema, request, message, Electroview, transport, handlers |
| Build, packaging, updates, signing | `electrobun-release` | build, ship, Updater, code signing, notarization, release channels, electrobun.config.ts, targets, ASAR, bsdiff |

**Load the specific sub-skill** for detailed patterns and examples. This router skill covers the mental model, project structure, and non-negotiable rules.

## Mental Model

Electrobun is a **three-layer sandwich**:

```
┌─────────────────────────────────────────────────────┐
│                 Your Electrobun App                   │
│                                                       │
│  ┌──────────────────┐      ┌───────────────────────┐ │
│  │  Bun Process      │      │  Webview / Browser    │ │
│  │  (Main Process)   │      │  (Renderer)           │ │
│  │                   │      │                       │ │
│  │  import from      │ RPC  │  import from          │ │
│  │  "electrobun/bun" │◄────►│  "electrobun/view"    │ │
│  │                   │      │                       │ │
│  │  • BrowserWindow  │      │  • Electroview        │ │
│  │  • BrowserView    │      │  • RPC handlers       │ │
│  │  • Tray, Menus    │      │  • DOM / UI           │ │
│  │  • Utils, Updater │      │  • <electrobun-webview>│ │
│  │  • GlobalShortcut │      │  • <electrobun-wgpu>  │ │
│  └────────┬──────────┘      └──────────┬────────────┘ │
│           │                            │              │
│  ┌────────┴────────────────────────────┴────────────┐ │
│  │         Native Layer (C++ / ObjC / Zig)           │ │
│  │  Window management, system webview hosting,       │ │
│  │  file dialogs, clipboard, notifications,          │ │
│  │  global shortcuts, tray icons, GPU surfaces       │ │
│  └───────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

1. **Bun Process (Main Process)** — TypeScript backend logic. Manages windows, tray, menus, system APIs, app lifecycle. Import from `"electrobun/bun"`.
2. **Native Layer** — Zig FFI bindings → macOS/Windows/Linux native APIs. You don't interact with this directly.
3. **Webview/Browser (Renderer)** — UI runs in system native webview (WebKit on macOS, WebView2 on Windows, WebKitGTK on Linux) or optional bundled CEF. Import from `"electrobun/view"`.

Communication between layers is via **typed RPC** — define a schema as TypeScript types, both sides get fully typed request/response and fire-and-forget message APIs.

## Project Structure

```
my-app/
├── electrobun.config.ts     ← config: app metadata, views, build, runtime settings
├── package.json
├── tsconfig.json
├── src/
│   ├── bun/
│   │   └── index.ts         ← main process entry (import from "electrobun/bun")
│   ├── views/
│   │   └── mainview/
│   │       ├── index.html   ← webview HTML content
│   │       ├── index.css    ← webview styles
│   │       └── index.ts     ← browser code (import from "electrobun/view")
│   └── shared/
│       └── types.ts         ← shared RPC type definitions (no runtime imports)
├── icon.iconset/            ← app icons (macOS)
├── build/                   ← build output (generated)
└── artifacts/               ← distribution artifacts (generated)
```

## Import Patterns

```typescript
// Main process (runs in Bun) — use "electrobun/bun"
import Electrobun from "electrobun/bun";
import { BrowserWindow, BrowserView, Tray, Utils, PATHS } from "electrobun/bun";

// Browser/renderer context — use "electrobun/view"
import { Electroview } from "electrobun/view";

// Shared types (for RPC schemas) — plain TypeScript, no runtime import
import type { MyRPCSchema } from "../shared/types";
```

## views:// URL Scheme

Electrobun uses a custom `views://` protocol to load bundled assets:

```typescript
// Load a view in a window
const win = new BrowserWindow({
    title: "My App",
    url: "views://mainview/index.html",
});
```

`views://mainview/index.html` resolves to `<app>/Resources/app/views/mainview/index.html` at runtime. Files are mapped via `build.copy` in `electrobun.config.ts`.

## Minimal Config Example

```typescript
import type { ElectrobunConfig } from "electrobun";

export default {
    app: {
        name: "My App",
        identifier: "com.example.myapp",
        version: "1.0.0",
    },
    build: {
        bun: { entrypoint: "src/bun/index.ts" },
        views: {
            mainview: { entrypoint: "src/views/mainview/index.ts" },
        },
        copy: {
            "src/views/mainview/index.html": "views/mainview/index.html",
            "src/views/mainview/index.css": "views/mainview/index.css",
        },
    },
} satisfies ElectrobunConfig;
```

## Non-Negotiable Rules

1. **This is NOT Electron** — never use `ipcMain`, `ipcRenderer`, `app.on('ready')`, `webContents`, or any Electron API
2. **Import `"electrobun/bun"` in main process, `"electrobun/view"` in browser** — never mix them
3. **Use `views://` URLs to load bundled assets** — not `file://` or relative paths
4. **Views must be configured in `electrobun.config.ts`** — both in `build.views` (TS entrypoints) and `build.copy` (static files)
5. **Always define RPC schemas as TypeScript types** — this gives you type-safe bidirectional communication
6. **`BrowserWindow` creates a `BrowserView` automatically** — don't create views manually for simple single-view windows
7. **The native layer is Zig FFI** — not Node.js native modules or N-API

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Importing `"electrobun"` | Use `"electrobun/bun"` or `"electrobun/view"` |
| Using Electron-style `ipcMain`/`ipcRenderer` | Use Electrobun's typed RPC: `createRPC` / `defineElectrobunRPC` |
| Forgetting to configure views in config | Add entries to both `build.views` and `build.copy` in `electrobun.config.ts` |
| Manually creating BrowserView for simple windows | `BrowserWindow` auto-creates one — just pass `url` option |
| Using `file://` URLs for bundled assets | Use `views://` protocol |
| Putting runtime code in `shared/` | `shared/` is for type-only imports — no `"electrobun/bun"` or `"electrobun/view"` imports |

## Platform Support

| Platform | Webview Engine | Notes |
|----------|---------------|-------|
| **macOS 14+** (ARM64, x64) | WebKit (WKWebView) | Full support — code signing + notarization |
| **Windows 11+** (x64) | Edge WebView2 | Full support via WebView2 |
| **Ubuntu 22.04+** (x64, ARM64) | WebKitGTK | CEF strongly recommended |

All platforms optionally support **bundled CEF** for consistent cross-platform rendering. Configure via `build.<platform>.bundleCEF` and `build.<platform>.defaultRenderer` in `electrobun.config.ts`.

## Quick Start

```bash
# Create a new project
bunx electrobun init

# Development with hot reload
electrobun dev --watch

# Build for distribution
electrobun build
```

## Key API Surface (from "electrobun/bun")

| Category | Exports |
|----------|---------|
| **Window & View** | `BrowserWindow`, `BrowserView`, `GpuWindow`, `WGPUView` |
| **System UI** | `Tray`, `ApplicationMenu`, `ContextMenu` |
| **RPC** | `createRPC`, `defineElectrobunRPC`, `RPCSchema` |
| **System APIs** | `Utils`, `GlobalShortcut`, `Screen`, `Session`, `PATHS` |
| **Lifecycle** | `Updater`, `BuildConfig` |
| **WebGPU** | `WGPU`, `WGPUBridge`, `three`, `babylon` |
