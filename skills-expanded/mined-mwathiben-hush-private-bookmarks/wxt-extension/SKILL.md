---
name: wxt-extension
description: WXT browser extension framework conventions, entrypoint routing, manifest generation, browser API abstraction, and cross-browser targeting. Triggers on wxt.config.ts, entrypoints/, defineBackground, defineContentScript, browser.*, content script UI, manifest permissions, or any browser extension development task.
---

# WXT Extension Development

WXT v0.20.x framework conventions for this project. All code examples assume React + TypeScript.

Reference: https://wxt.dev

---

## 1. Convention-Based Entrypoint Routing

WXT auto-discovers entrypoints from the `entrypoints/` directory. File names determine manifest entries.

### Entrypoint Type → Filename Mapping

| Type | Single File | Directory | Output |
|------|-------------|-----------|--------|
| Background | `background.ts` | `background/index.ts` | `background.js` |
| Popup | `popup.html` | `popup/index.html` | `popup.html` |
| Options | `options.html` | `options/index.html` | `options.html` |
| Side Panel | `sidepanel.html` | `sidepanel/index.html` | `sidepanel.html` |
| Content Script | `content.ts` | `content/index.ts` | `content-scripts/content.js` |
| Named Content | `{name}.content.ts` | `{name}.content/index.ts` | `content-scripts/{name}.js` |
| Newtab | `newtab.html` | `newtab/index.html` | `newtab.html` |
| Bookmarks | `bookmarks.html` | `bookmarks/index.html` | `bookmarks.html` |
| History | `history.html` | `history/index.html` | `history.html` |
| Devtools | `devtools.html` | `devtools/index.html` | `devtools.html` |
| Sandbox | `sandbox.html` | `sandbox/index.html` | `sandbox.html` |
| Named Sandbox | `{name}.sandbox.html` | `{name}.sandbox/index.html` | `{name}.html` |
| Named Side Panel | `{name}.sidepanel.html` | `{name}.sidepanel/index.html` | `{name}.html` |
| Unlisted Page | `{name}.html` | `{name}/index.html` | `{name}.html` |
| Unlisted Script | `{name}.ts` | `{name}/index.ts` | `{name}.js` |
| Unlisted CSS | `{name}.css` | `{name}/index.css` | `{name}.css` |

### Directory Pattern for Multi-File Entrypoints

```
entrypoints/
  popup/
    index.html      ← THIS is the entrypoint (not main.tsx)
    main.tsx
    App.tsx
    style.css
  background/
    index.ts         ← THIS is the entrypoint
    alarms.ts
    messaging.ts
```

### CRITICAL RULES

1. **Max 1 level of nesting.** `entrypoints/popup/index.html` works. `entrypoints/features/popup/index.html` does NOT.

2. **Every file directly in `entrypoints/` becomes an entrypoint.** Never place helper files, utilities, or shared code directly in `entrypoints/`. They will be treated as unlisted scripts/pages.

   ```
   # WRONG — utils.ts becomes an entrypoint
   entrypoints/
     background.ts
     utils.ts          ← WXT treats this as unlisted script!

   # CORRECT — helper inside directory
   entrypoints/
     background/
       index.ts
       utils.ts         ← just a helper, not an entrypoint
   ```

3. **Named entrypoints use dot notation.** `overlay.content.ts` creates a content script named "overlay". `overlay.ts` creates an unlisted script.

### Project Entrypoint Layout (Hush Private Bookmarks)

```
entrypoints/
  popup/              ← browser action popup (React SPA, directory pattern)
    index.html
    main.tsx
    App.tsx
  manager/            ← full-page bookmark manager (unlisted page, directory pattern)
    index.html
    main.tsx
    App.tsx
  background/
    index.ts
  content.ts
```

- **`popup/`** is a recognized entrypoint → outputs `popup.html`, registered as `action.default_popup` in manifest.
- **`manager/`** is an **unlisted page** (no reserved name like "bookmarks" or "options") → outputs `/manager.html`. It does NOT appear in the manifest automatically.
- Both popup and manager import shared code from `components/` and `lib/` directories.

Opening the manager page from background or popup:

```typescript
const url = browser.runtime.getURL('/manager.html');
await browser.tabs.create({ url });
```

---

## 2. Manifest.json Generation

WXT generates `manifest.json` at `.output/{browser}-{mv}-{mode}/manifest.json`. There is no source `manifest.json` file.

### Sources (in order of precedence)

1. Entrypoint files (auto-detected from `entrypoints/`)
2. `wxt.config.ts` manifest property
3. WXT modules
4. `build:manifestGenerated` hook

### Adding Permissions in wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-react'],
  manifest: {
    permissions: ['storage', 'bookmarks', 'tabs'],
    host_permissions: ['*://*.example.com/*'],
  },
});
```

### Conditional Manifest (Function Form)

```typescript
export default defineConfig({
  manifest: ({ browser, manifestVersion, mode, command }) => ({
    permissions: ['storage', 'bookmarks'],
    // Add dev-only permissions
    ...(mode === 'development' && {
      host_permissions: ['http://localhost/*'],
    }),
  }),
});
```

### ALWAYS Define in MV3 Format

WXT auto-converts MV3 properties to MV2 equivalents:

| MV3 Property | MV2 Equivalent |
|-------------|----------------|
| `action` | `browser_action` |
| `web_accessible_resources` (object array) | `web_accessible_resources` (flat string array) |
| `host_permissions` | merged into `permissions` |

```typescript
// CORRECT — define in MV3 format, WXT converts for MV2 builds
manifest: {
  action: { default_title: 'My Extension' },
  web_accessible_resources: [
    { matches: ['*://*.example.com/*'], resources: ['icon/*.png'] },
  ],
}
```

### Icon Auto-Discovery

WXT finds icons in `public/` matching these patterns:
- `icon-{size}.png` (e.g., `icon-16.png`, `icon-128.png`)
- `icon/{size}.png` (e.g., `icon/16.png`)
- `icon-{size}x{size}.png`
- `icon@{size}.png`

No manual icon config needed if you follow these patterns.

### Version from package.json

- `version`: cleaned numeric (e.g., `"1.3.0-alpha2"` → `"1.3.0"`)
- `version_name`: exact string from package.json

### HTML Meta Tags → Manifest

Popup, options, and sidepanel HTML files can set manifest properties via `<meta>` tags:

```html
<!-- entrypoints/popup/index.html -->
<title>Hush Bookmarks</title>
<meta name="manifest.type" content="browser_action" />
<meta name="manifest.default_icon" content="{ 16: '/icon/16.png', 32: '/icon/32.png' }" />

<!-- Browser filtering -->
<meta name="manifest.include" content="['chrome', 'firefox']" />
<meta name="manifest.exclude" content="['safari']" />
```

Options page:
```html
<meta name="manifest.open_in_tab" content="true" />
```

### Modifying Manifest via Hook

```typescript
export default defineConfig({
  hooks: {
    'build:manifestGenerated': (wxt, manifest) => {
      if (wxt.config.mode === 'development') {
        manifest.name += ' (DEV)';
      }
    },
  },
});
```

---

## 3. Browser API Abstraction

### The `browser` Global

WXT provides a unified `browser` global that works across all browsers:

```typescript
// Implementation (simplified)
export const browser = globalThis.browser?.runtime?.id
  ? globalThis.browser  // Firefox native
  : globalThis.chrome;  // Chromium browsers
```

### Usage

```typescript
// Auto-imported — no explicit import needed
browser.storage.local.get('key');
browser.runtime.sendMessage({ type: 'ping' });
browser.bookmarks.getTree();

// Explicit import when needed (e.g., in lib/ files)
import { browser } from 'wxt/browser';
```

### TypeScript Types

```typescript
import { type Browser } from 'wxt/browser';

function handleMessage(
  message: unknown,
  sender: Browser.runtime.MessageSender,
): void {
  // ...
}
```

### Promise-Based API

WXT enables promise-style APIs for both MV2 and MV3 across all browsers. No callbacks needed:

```typescript
// Works in Chrome, Firefox, Edge, Brave — MV2 and MV3
const tabs = await browser.tabs.query({ active: true });
const data = await browser.storage.local.get('key');
```

### Feature Detection (MANDATORY)

TypeScript types assume all APIs exist. They don't. Always feature-detect:

```typescript
// CORRECT — optional chaining for APIs that may not exist
browser.runtime.onSuspend?.addListener(() => {
  // MV3 service worker suspend
});

// CORRECT — fallback for MV2/MV3 API name differences
(browser.action ?? browser.browserAction).onClicked.addListener(() => {
  // Works in both MV2 and MV3
});

// WRONG — will crash if API doesn't exist
browser.sidePanel.open({ windowId: 1 }); // sidePanel not in Firefox
```

### NEVER Use `chrome.*` Directly

```typescript
// WRONG
chrome.storage.local.get('key');
chrome.runtime.sendMessage({ type: 'ping' });

// CORRECT
browser.storage.local.get('key');
browser.runtime.sendMessage({ type: 'ping' });
```

---

## 4. Entrypoint Structure

### CRITICAL: Build-Time vs Runtime Code

WXT imports entrypoint files into Node.js during the build to extract configuration. **All runtime code must be inside `main()`.**

```typescript
// WRONG — browser APIs at module level crash the build
browser.action.onClicked.addListener(() => {}); // ← Node.js error!

export default defineBackground(() => {
  // ...
});
```

```typescript
// CORRECT — all runtime code inside main
export default defineBackground(() => {
  browser.action.onClicked.addListener(() => {
    // runs in browser, not Node.js
  });
});
```

This applies to: `defineBackground`, `defineContentScript`, `defineUnlistedScript`.

HTML entrypoints (popup, options, etc.) are NOT affected — their JS runs normally.

### defineBackground()

```typescript
export default defineBackground({
  // MV2: persistent background page. MV3: ignored (always non-persistent service worker)
  persistent: false,
  // MV3 only: 'module' enables ES module syntax in service worker
  type: 'module',
  // Browser filtering
  include: undefined,  // string[] — only build for these browsers
  exclude: undefined,  // string[] — skip these browsers

  main() {
    // CANNOT be async
    // All runtime code goes here
    browser.runtime.onInstalled.addListener((details) => {
      if (details.reason === 'install') {
        // first install
      }
    });
  },
});

// Shorthand (no options needed):
export default defineBackground(() => {
  // main function body
});
```

**MV3 service worker constraints:**
- No DOM access (no `document`, no `window.localStorage`)
- No persistent state (service worker terminates when idle)
- Use `browser.storage` instead of in-memory state
- Use `browser.alarms` instead of `setInterval`

### defineContentScript()

```typescript
export default defineContentScript({
  // REQUIRED
  matches: ['*://*.example.com/*'],

  // Match filtering
  excludeMatches: [],
  includeGlobs: [],
  excludeGlobs: [],

  // Injection behavior
  allFrames: false,
  runAt: 'document_idle',  // 'document_start' | 'document_end' | 'document_idle'
  matchAboutBlank: false,
  matchOriginAsFallback: false,

  // Execution world
  world: 'ISOLATED',  // 'ISOLATED' | 'MAIN'

  // CSS injection
  cssInjectionMode: 'manifest',  // 'manifest' | 'manual' | 'ui'

  // Registration method
  registration: 'manifest',  // 'manifest' | 'runtime'

  // Browser filtering
  include: undefined,
  exclude: undefined,

  main(ctx: ContentScriptContext) {
    // CAN be async
    // ctx provides lifecycle-aware helpers
  },
});
```

### ContentScriptContext Lifecycle

The `ctx` parameter provides lifecycle-safe wrappers that auto-cleanup when the extension context invalidates (update, uninstall, disable):

```typescript
export default defineContentScript({
  matches: ['*://*.example.com/*'],
  main(ctx) {
    // Use ctx wrappers instead of raw browser APIs
    ctx.addEventListener(window, 'click', handler);    // auto-removed on invalidation
    ctx.setTimeout(doWork, 1000);                      // auto-cancelled
    ctx.setInterval(poll, 5000);                       // auto-cancelled
    ctx.requestAnimationFrame(animate);                // auto-cancelled

    // Check validity before async operations
    if (ctx.isValid) {
      // safe to proceed
    }
    if (ctx.isInvalid) {
      // context destroyed, stop work
    }
  },
});
```

### Content Script UI Methods

| Method | Isolated Styles | Isolated Events | HMR | Page Context Access |
|--------|----------------|-----------------|-----|---------------------|
| Integrated | No | No | No | Yes |
| Shadow Root | Yes | Yes (opt-in) | No | Yes |
| IFrame | Yes | Yes | Yes | No |

**Shadow Root UI (recommended for most cases):**

```typescript
import './style.css';

export default defineContentScript({
  matches: ['*://*.example.com/*'],
  cssInjectionMode: 'ui',

  async main(ctx) {
    const ui = await createShadowRootUi(ctx, {
      name: 'hush-bookmark-ui',
      position: 'inline',
      anchor: 'body',
      onMount(container) {
        const root = createRoot(container);
        root.render(<App />);
        return root;
      },
      onRemove(root) {
        root?.unmount();
      },
    });
    ui.mount();
  },
});
```

**IFrame UI (for full HMR during dev):**

1. Create `entrypoints/overlay.html` (an unlisted page)
2. Add to `web_accessible_resources` in manifest
3. Mount:

```typescript
export default defineContentScript({
  matches: ['*://*.example.com/*'],
  main(ctx) {
    const ui = createIframeUi(ctx, {
      page: '/overlay.html',
      position: 'inline',
      anchor: 'body',
      onMount(wrapper, iframe) {
        iframe.width = '400';
        iframe.height = '300';
      },
    });
    ui.mount();
  },
});
```

### SPA Navigation Handling

SPAs don't trigger full page reloads. Content scripts need explicit navigation detection:

```typescript
export default defineContentScript({
  matches: ['*://*.example.com/*'],
  main(ctx) {
    ctx.addEventListener(window, 'wxt:locationchange', ({ newUrl }) => {
      // Re-run logic on SPA navigation
      if (shouldActivate(newUrl)) {
        activate(ctx);
      }
    });
  },
});
```

### defineUnlistedScript()

Scripts not tied to any manifest entry. You load them manually.

```typescript
export default defineUnlistedScript(() => {
  // runs when explicitly loaded
});

// Load from another entrypoint:
const url = browser.runtime.getURL('/my-script.js');
```

**You must add unlisted scripts to `web_accessible_resources` if injecting into web pages.**

### HTML Entrypoints (Popup, Options, etc.)

Standard HTML + React SPA. No special `main()` restriction — these run in browser context normally.

```html
<!-- entrypoints/popup/index.html -->
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hush Private Bookmarks</title>
  <meta name="manifest.type" content="browser_action" />
</head>
<body>
  <div id="root"></div>
  <script type="module" src="./main.tsx"></script>
</body>
</html>
```

---

## 5. MV3 Compliance

### Default Manifest Versions by Browser

| Browser | Default MV | Override |
|---------|-----------|---------|
| Chrome | MV3 | `--mv2` |
| Edge | MV3 | `--mv2` |
| Brave | MV3 | `--mv2` |
| Firefox | MV2 | `--mv3` |
| Safari | MV2 | `--mv3` |

### Runtime Detection

```typescript
if (import.meta.env.MANIFEST_VERSION === 3) {
  // MV3-specific code
}
if (import.meta.env.MANIFEST_VERSION === 2) {
  // MV2 fallback
}
```

### MV3 Service Worker Constraints

Background scripts in MV3 are service workers:
- **No DOM.** No `document`, `window.localStorage`, `XMLHttpRequest`.
- **Non-persistent.** Terminates when idle. No in-memory state survives.
- **Use `browser.storage`** for persistence, **`browser.alarms`** for timers.
- **`main()` cannot be async** in defineBackground.

### Always Write MV3-First

Define all manifest properties in MV3 format. WXT handles MV2 conversion:

```typescript
// CORRECT — MV3 format, auto-converts to MV2
manifest: {
  action: { default_title: 'Hush' },
  web_accessible_resources: [
    { matches: ['<all_urls>'], resources: ['icon/*.png'] },
  ],
}

// WRONG — MV2 format, won't auto-convert to MV3
manifest: {
  browser_action: { default_title: 'Hush' },
  web_accessible_resources: ['icon/*.png'],
}
```

---

## 6. Cross-Browser Targeting

### Build Commands

```bash
wxt                  # dev: chrome (default)
wxt -b firefox       # dev: firefox
wxt -b edge          # dev: edge (opens Chrome by default, configure binary)
wxt build            # prod: chrome
wxt build -b firefox # prod: firefox
wxt zip              # package: chrome
wxt zip -b firefox   # package: firefox
```

### Output Directory Convention

`.output/{browser}-mv{version}-{mode}/`

Examples:
- `.output/chrome-mv3-dev/`
- `.output/firefox-mv2-production/`

### Runtime Browser Detection

```typescript
// String check
if (import.meta.env.BROWSER === 'firefox') {
  // Firefox-only code
}

// Boolean shortcuts
if (import.meta.env.FIREFOX) { /* ... */ }
if (import.meta.env.CHROME) { /* ... */ }
if (import.meta.env.EDGE) { /* ... */ }
```

### Per-Entrypoint Browser Filtering

Script entrypoints:
```typescript
export default defineContentScript({
  include: ['chrome', 'edge'],  // only in these builds
  exclude: ['firefox'],         // skip these builds
  matches: ['*://*.example.com/*'],
  main(ctx) { /* ... */ },
});
```

HTML entrypoints:
```html
<meta name="manifest.include" content="['chrome', 'edge']" />
```

Config-level filtering:
```typescript
export default defineConfig({
  filterEntrypoints: (entrypoint) => {
    // programmatic control
    return true;
  },
});
```

### Browser Binary Configuration

```typescript
// web-ext.config.ts (project root, gitignored)
import { defineWebExtConfig } from 'wxt';

export default defineWebExtConfig({
  binaries: {
    chrome: '/path/to/chrome-beta',
    firefox: 'firefoxdeveloperedition',
    edge: '/path/to/msedge',
  },
});
```

---

## 7. Storage API

WXT provides `wxt/storage` — a typed wrapper around `browser.storage`.

**Requires `storage` permission in manifest.**

### Storage Area Prefixes

| Prefix | Area | Scope |
|--------|------|-------|
| `local:` | `browser.storage.local` | Per-device, persists |
| `sync:` | `browser.storage.sync` | Synced across devices |
| `session:` | `browser.storage.session` | Per-session, cleared on close |
| `managed:` | `browser.storage.managed` | Admin-configured, read-only |

### Defining Typed Storage Items

```typescript
import { storage } from 'wxt/storage';

const encryptedBookmarks = storage.defineItem<string>('local:encryptedBookmarks', {
  defaultValue: '',
});

// Usage
const data = await encryptedBookmarks.getValue();
await encryptedBookmarks.setValue(encrypted);

// Watch for changes
const unwatch = encryptedBookmarks.watch((newValue) => {
  // react to changes from any context (popup, background, content script)
});
```

### Versioned Storage with Migrations

```typescript
const settings = storage.defineItem<Settings>('local:settings', {
  defaultValue: { theme: 'system', autoLock: true },
  version: 2,
  migrations: {
    2: (oldValue: OldSettings): Settings => ({
      ...oldValue,
      autoLock: true, // new field in v2
    }),
  },
});
```

---

## 8. Environment Variables

### Built-in Variables

| Variable | Type | Values |
|----------|------|--------|
| `import.meta.env.BROWSER` | `string` | `'chrome'`, `'firefox'`, etc. |
| `import.meta.env.MANIFEST_VERSION` | `number` | `2` or `3` |
| `import.meta.env.CHROME` | `boolean` | browser shortcut |
| `import.meta.env.FIREFOX` | `boolean` | browser shortcut |
| `import.meta.env.EDGE` | `boolean` | browser shortcut |
| `import.meta.env.MODE` | `string` | `'development'` or `'production'` |
| `import.meta.env.DEV` | `boolean` | true in dev |
| `import.meta.env.PROD` | `boolean` | true in prod |

### Custom Variables

Prefix with `WXT_` or `VITE_` in `.env` files:

```
WXT_API_KEY=abc123
```

Dotenv file resolution order: `.env`, `.env.local`, `.env.{mode}`, `.env.{browser}`, `.env.{mode}.{browser}`

### Using in Manifest Config

Must use function form to defer evaluation:

```typescript
export default defineConfig({
  manifest: () => ({
    oauth2: {
      client_id: import.meta.env.WXT_CLIENT_ID,
    },
  }),
});
```

---

## 9. Auto-Imports

WXT auto-imports exports from these directories (no explicit import needed):

- `components/`
- `composables/`
- `hooks/`
- `utils/`

Also auto-imports WXT utilities: `defineBackground`, `defineContentScript`, `createShadowRootUi`, `browser`, etc.

Run `wxt prepare` to generate TypeScript declarations. Add to package.json:

```json
{ "scripts": { "postinstall": "wxt prepare" } }
```

Explicit import when needed (e.g., in test files):

```typescript
import { defineBackground, browser } from '#imports';
```

---

## 10. Common Mistakes — DO NOT

### 1. Runtime code outside `main()` (THE #1 MISTAKE)

```typescript
// FATAL — crashes build. WXT runs this in Node.js.
const tabs = await browser.tabs.query({});

export default defineBackground(() => { /* ... */ });
```

### 2. Placing helper files directly in `entrypoints/`

```
entrypoints/
  background.ts
  helpers.ts     ← WXT makes this an unlisted script!
```

Move helpers into a subdirectory or into `lib/`/`utils/`.

### 3. Nesting entrypoints deeper than 1 level

```
entrypoints/
  features/
    overlay/
      content/
        index.ts   ← NOT discovered. Max 1 level deep.
```

### 4. Forgetting `web_accessible_resources`

Content scripts that reference extension assets (images, scripts, HTML) need them declared:

```typescript
manifest: {
  web_accessible_resources: [
    { matches: ['<all_urls>'], resources: ['icon/*.png', 'overlay.html'] },
  ],
}
```

And use `browser.runtime.getURL()` to get the full URL:

```typescript
const iconUrl = browser.runtime.getURL('/icon/128.png');
```

### 5. Using `chrome.*` instead of `browser`

Always use WXT's `browser` global. See §3.

### 6. Assuming all browser APIs exist

Not every API is available in every browser or manifest version. Always feature-detect:

```typescript
// WRONG
browser.sidePanel.open({ windowId });

// CORRECT
browser.sidePanel?.open({ windowId });
```

### 7. Forgetting `storage` permission

`browser.storage` calls fail silently or throw without the permission:

```typescript
manifest: {
  permissions: ['storage'],  // REQUIRED for wxt/storage
}
```

### 8. Ignoring SPA navigation in content scripts

Content scripts only run on initial page load. SPAs change URL without reloading:

```typescript
ctx.addEventListener(window, 'wxt:locationchange', ({ newUrl }) => {
  // handle navigation
});
```

### 9. Async `main()` in defineBackground

```typescript
// WRONG — main cannot be async in defineBackground
export default defineBackground({
  async main() { /* ... */ },  // ← breaks
});

// CORRECT — use async inside, not on main itself
export default defineBackground({
  main() {
    (async () => {
      await someSetup();
    })();
  },
});
```

### 10. Using `window.localStorage` in background service worker

MV3 background is a service worker — no `window`, no `localStorage`. Use `browser.storage.local` or `browser.storage.session`.
