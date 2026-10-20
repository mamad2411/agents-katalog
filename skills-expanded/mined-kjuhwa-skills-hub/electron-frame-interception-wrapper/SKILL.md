---
name: electron-frame-interception-wrapper
description: Pre-load wrapper that intercepts require('electron') via Module.prototype.require and returns a Proxy patching BrowserWindow and Menu. Enables injecting frame mode, menu-bar behavior, and CSS without modifying minified app code.
category: electron-packaging
version: 1.0.0
tags: [electron, proxy, browserwindow, menu, preload, patching, linux]
source_type: extracted-from-git
source_url: https://github.com/aaddrick/claude-desktop-debian.git
source_ref: main
source_commit: 2fd9faf9db4eaa409b88310bdce397f8bdb0e916
source_project: claude-desktop-debian
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

# Electron Frame Interception Wrapper

## When to use

Use this pattern when:
- You are repackaging a third-party Electron app and cannot modify its minified source code directly.
- You need to change default `BrowserWindow` options (e.g., `frame`, `autoHideMenuBar`, `titleBarStyle`) without editing the app's bundle.
- You want to inject CSS into every window after it loads (e.g., scrollbar styling for a non-native platform).
- You want to intercept `Menu.setApplicationMenu` to apply side effects (e.g., hide the menu bar after every menu update).

This pattern is an alternative to patching minified JS with `sed`. It is more robust across upstream version bumps because it operates at the JavaScript module level rather than on text patterns.

## Pattern

### Entry point injection

1. Read the app's current `main` field from `package.json`.
2. Create `frame-fix-entry.js` that `require`s the wrapper then the original main.
3. Update `package.json`'s `main` field to point at `frame-fix-entry.js`.

### Wrapper structure

The wrapper overrides `Module.prototype.require`. On the first call with `id === 'electron'`:
- Build a `PatchedBrowserWindow` class extending the original.
- Build a patched `setApplicationMenu` function.
- Cache both (lazy singleton).

On every call with `id === 'electron'`, return a `Proxy` over the real module that substitutes `BrowserWindow` and `Menu` from the cache.

```
Module.prototype.require override
  └─ id === 'electron' ?
       ├─ first call: build PatchedBrowserWindow + patchedSetApplicationMenu
       └─ always: return Proxy{ BrowserWindow → Patched, Menu → proxy of Menu }
```

## Minimal example

```javascript
// wrapper.js — injected before the original app main
const Module = require('module');
const path = require('path');
const originalRequire = Module.prototype.require;

// Correct process.resourcesPath if electron and app live in different directories
// (common on NixOS or when electron is installed separately)
const derivedResourcesPath = path.dirname(__dirname);
if (derivedResourcesPath !== process.resourcesPath) {
  process.resourcesPath = derivedResourcesPath;
}

let PatchedBrowserWindow = null;
let patchedSetApplicationMenu = null;

Module.prototype.require = function(id) {
  const result = originalRequire.apply(this, arguments);

  if (id === 'electron') {
    if (!PatchedBrowserWindow) {
      const OriginalBrowserWindow = result.BrowserWindow;
      const OriginalMenu = result.Menu;

      PatchedBrowserWindow = class PatchedWindow extends OriginalBrowserWindow {
        constructor(options) {
          if (process.platform === 'linux') {
            options = options || {};
            const isPopup = options.frame === false
              || (options.titleBarStyle === '' && !options.minWidth);

            if (isPopup) {
              options.frame = false;
              delete options.titleBarStyle;
              delete options.titleBarOverlay;
            } else {
              // Main window: force native frame, hide menu bar by default
              options.frame = true;
              options.autoHideMenuBar = true;
              delete options.titleBarStyle;
              delete options.titleBarOverlay;
            }
          }
          super(options);

          if (process.platform === 'linux') {
            this.setMenuBarVisibility(false);
            // Inject custom CSS on every page load
            this.webContents.on('did-finish-load', () => {
              this.webContents.insertCSS(
                '::-webkit-scrollbar { width: 8px; } ' +
                '::-webkit-scrollbar-thumb { background: rgba(128,128,128,0.3); border-radius: 4px; }'
              ).catch(() => {});
            });
          }
        }
      };

      // Copy static members (getAllWindows, fromId, etc.)
      for (const key of Object.getOwnPropertyNames(OriginalBrowserWindow)) {
        if (key === 'prototype' || key === 'length' || key === 'name') continue;
        try {
          const desc = Object.getOwnPropertyDescriptor(OriginalBrowserWindow, key);
          if (desc) Object.defineProperty(PatchedBrowserWindow, key, desc);
        } catch (_) {}
      }

      // Intercept setApplicationMenu to keep menu bar hidden
      const originalSetMenu = OriginalMenu.setApplicationMenu.bind(OriginalMenu);
      patchedSetApplicationMenu = function(menu) {
        originalSetMenu(menu);
        if (process.platform === 'linux') {
          for (const win of PatchedBrowserWindow.getAllWindows()) {
            if (!win.isDestroyed()) win.setMenuBarVisibility(false);
          }
        }
      };
    }

    return new Proxy(result, {
      get(target, prop, receiver) {
        if (prop === 'BrowserWindow') return PatchedBrowserWindow;
        if (prop === 'Menu') {
          return new Proxy(target.Menu, {
            get(menuTarget, menuProp) {
              if (menuProp === 'setApplicationMenu') return patchedSetApplicationMenu;
              return Reflect.get(menuTarget, menuProp);
            }
          });
        }
        return Reflect.get(target, prop, receiver);
      }
    });
  }

  return result;
};
```

```javascript
// entry.js — this becomes package.json's "main"
require('./wrapper.js');
require('./original-main.js');  // the app's original main entry
```

```javascript
// Snippet to update package.json (run once during build)
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg.originalMain = pkg.main;
pkg.main = 'entry.js';
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
```

## Why this works

### `Module.prototype.require` intercept vs. require cache override

Overriding `Module.prototype.require` intercepts all future `require('electron')` calls from any module, not just the entry point. This is necessary because the app may call `require('electron')` from multiple files (main process, preload scripts, etc.). Overriding the require cache entry directly (`require.cache[require.resolve('electron')]`) only works for future loads, not for modules already in the cache.

### Proxy over non-configurable getters

The Electron module exports `BrowserWindow` through a non-configurable getter on the exports object. You cannot write `result.BrowserWindow = PatchedBrowserWindow` — this throws in strict mode. A `Proxy` with a `get` trap intercepts property access without modifying the underlying object, bypassing this restriction entirely.

### Lazy singleton to handle multiple require calls

The first `require('electron')` call builds and caches the patched classes. Subsequent calls reuse the cache. This avoids re-wrapping on every require (which would create new class objects, breaking `instanceof` checks on window instances).

### Popup detection heuristic

Main windows have `minWidth` set (they are resizable). Popup/quick-entry windows have `titleBarStyle: ''` but no `minWidth`. Checking `options.titleBarStyle === '' && !options.minWidth` distinguishes them without relying on any app-specific string that could change between versions.

## Pitfalls

- **Do not override `Module._resolveFilename`** — overriding `require` is sufficient and less invasive. Touching `_resolveFilename` breaks module path resolution for all modules.
- **Static method copy must skip `prototype`, `length`, `name`** — these are non-configurable on function objects and `Object.defineProperty` will throw if you try to copy them. Always guard with `if (key === 'prototype' || ...) continue`.
- **`process.resourcesPath` is read-only in Electron 28.2.1+** — the correction at the top of the wrapper must happen before any app code reads it. Test this carefully when updating Electron versions.
- **CSS injection timing** — `insertCSS` must be called in `did-finish-load`, not `dom-ready`, because some CSS resets happen after `dom-ready` in Electron's render lifecycle.
- **`autoHideMenuBar` and `setMenuBarVisibility` interact** — setting both can cause flicker. Use `autoHideMenuBar: true` for the "Alt toggles" mode and `setMenuBarVisibility(false)` for the "always hidden" mode. Do not combine them for the same mode.

## Source reference

`scripts/frame-fix-wrapper.js` — full implementation; `build.sh` `patch_app_asar()` for injection into `package.json`
