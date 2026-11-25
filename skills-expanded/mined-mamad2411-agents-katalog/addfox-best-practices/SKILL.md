---
name: addfox-best-practices
description: >-
  Addfox + Rsbuild for Manifest V3 browser extensions. addfox.config.ts, manifest (chromium/firefox split),
  file-based app/ entries (background service worker, content, popup, options, sidepanel, devtools, offscreen),
  permissions and host_permissions, webextension-polyfill, UI frameworks (React Vue Preact Svelte Solid),
  Tailwind v4 UnoCSS Sass Less, runtime messaging with a `from` field, content page UI via
  defineShadowContentUI / defineIframeContentUI / defineContentUI from @addfox/utils, addfox dev/build CLI.
metadata:
  tags: addfox, browser-extension, webextension, manifest-v3, mv3, chrome-extension, firefox, rsbuild, addfox.config, content-script, service-worker, popup, sidepanel, messaging, shadow-dom, tailwind, crx
---

## When to use

Use this skill **whenever** the project depends on Addfox (`addfox` in package.json, `addfox.config.ts`, `defineConfig` from `addfox`) **or** the user asks about building or configuring extensions with Addfox, Rsbuild plugin setup, `.addfox/extension` output, or MV3 extension architecture.

Also load it when the user mentions any of the following (including synonyms):

- **Config & manifest**: `addfox.config`, manifest fields, `host_permissions`, `web_accessible_resources`, Chrome vs Firefox manifest split, `appDir`, `outDir`, `zip`, `envPrefix`, `hotReload`, `report` / Rsdoctor
- **Entries**: `app/background`, `app/content`, `app/popup`, `app/options`, `app/sidepanel`, custom `entry`, HTML template `data-addfox-entry`
- **Cross-browser**: `webextension-polyfill`, `browser.*` API, `addfox dev -b` / `addfox build -b`
- **UI on pages**: floating panel, inject UI into page, Shadow DOM, iframe UI, `@addfox/utils` content UI helpers
- **Styles**: Tailwind v4 `@tailwindcss/postcss`, UnoCSS, scoped CSS in content scripts
- **Feature-heavy extensions** (video, AI, downloads, etc.): use this skill **together with** `extension-functions-best-practices` for domain patterns

**Do not** use this skill for pure migration from WXT/Plasmo (use **migrate-to-addfox**), for test setup (use **addfox-testing**), or for build/runtime failures (use **addfox-debugging** first if the user pasted errors).

## How to use

Read this file for end-to-end patterns. For focused rules, open:

- [rules/manifest-fields.md](rules/manifest-fields.md) — manifest keys and Addfox-specific behavior
- [rules/permissions.md](rules/permissions.md) — permission choices and least-privilege patterns
- [rules/messaging.md](rules/messaging.md) — message shapes, async responses, tab vs runtime messaging
- [rules/content-ui.md](rules/content-ui.md) — `defineShadowContentUI`, iframe UI, mount timing
- [reference.md](reference.md) — CLI, config table, cross-platform notes

Related skills: [addfox-debugging](../addfox-debugging/SKILL.md), [addfox-testing](../addfox-testing/SKILL.md), [migrate-to-addfox](../migrate-to-addfox/SKILL.md), [extension-functions-best-practices](../extension-functions-best-practices/SKILL.md).

---

# Addfox Best Practices

Covers entry discovery, config, manifest, permissions, cross-platform APIs, UI frameworks, styles, messaging, and content UI.

---

## 1. Entry

### File-based Entry (Recommended)

Do not set `entry` in config when possible. Use default `appDir: "app"` and place scripts under reserved directories:

```
app/
├── background/          → Service worker
│   └── index.ts
├── content/             → Content script
│   └── index.ts
├── popup/               → Popup page
│   └── index.tsx
├── options/             → Options page
│   └── index.tsx
├── sidepanel/           → Side panel (Chrome)
│   └── index.tsx
├── devtools/            → DevTools page
│   └── index.tsx
├── offscreen/           → Offscreen document (MV3)
│   └── index.tsx
├── newtab/              → New Tab page
│   └── index.tsx
└── history/             → History page
    └── index.tsx
```

The framework discovers reserved names by directory; do not write source file paths for built-in entries in the manifest — the framework fills output paths automatically.

### Reserved Entry Names

| Entry | Output Path | HTML Generated | Notes |
|-------|-------------|----------------|-------|
| `background` | `background/index.js` | ❌ | Service worker (MV3) or background page (MV2) |
| `content` | `content/index.js` | ❌ | Content script(s) |
| `popup` | `popup/index.html` | ✅ | Toolbar popup |
| `options` | `options/index.html` | ✅ | Extension options page |
| `sidepanel` | `sidepanel/index.html` | ✅ | Chrome side panel |
| `devtools` | `devtools/index.html` | ✅ | DevTools extension |
| `offscreen` | `offscreen/index.html` | ✅ | Offscreen document for DOM/audio in MV3 |
| `sandbox` | `sandbox/index.html` | ✅ | Sandbox page |
| `newtab` | `newtab/index.html` | ✅ | New Tab override |
| `bookmarks` | `bookmarks/index.html` | ✅ | Bookmarks override |
| `history` | `history/index.html` | ✅ | History override |

### Custom Entries

Use the config **`entry`** field for non–built-in entries:

```ts
// addfox.config.ts
export default defineConfig({
  entry: {
    capture: 'capture/index.ts',
    worker: 'workers/custom.ts'
  },
  manifest: {
    // Reference by output path
    web_accessible_resources: [{
      resources: ['capture/index.html'],
      matches: ['<all_urls>']
    }]
  }
});
```

### HTML Templates

For popup/options/sidepanel/devtools/offscreen, either:
- **Omit HTML** — framework generates it automatically
- **Provide template** with entry marker:

```html
<!-- app/popup/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Popup</title>
</head>
<body>
  <div id="root"></div>
  <!-- This marker tells Addfox where to inject -->
  <script data-addfox-entry src="./index.tsx"></script>
</body>
</html>
```

Details: [reference.md](reference.md#entry).

---

## 2. addfox.config and manifest

### Config File

`addfox.config.ts` (or `.js`/`.mjs`) at project root:

```ts
import { defineConfig } from 'addfox';
import { pluginReact } from '@rsbuild/plugin-react';

const manifest = {
  manifest_version: 3,
  name: 'My Extension',
  version: '1.0.0',
  description: 'Extension description',
  permissions: ['storage', 'activeTab'],
  host_permissions: ['<all_urls>'],
  action: {
    default_popup: 'popup/index.html'
  },
  options_ui: {
    open_in_tab: true
  },
  content_scripts: [{
    matches: ['<all_urls>']
  }]
};

export default defineConfig({
  // App directory (default: "app")
  appDir: 'app',
  
  // Output directory name under .addfox (default: "extension")
  outDir: 'extension',
  
  // Manifest configuration - supports chromium/firefox split
  manifest: {
    chromium: manifest,
    firefox: { ...manifest }
  },
  
  // Rsbuild plugins (from @rsbuild/plugin-* or @addfox/rsbuild-plugin-*)
  plugins: [pluginReact()],
  
  // Override/extend Rsbuild config (optional)
  rsbuild: {
    // Rsbuild configuration object
    // Or function: (base, helpers) => helpers.merge(base, overrides)
  }
});
```

### Config Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `manifest` | `object \| { chromium, firefox }` | Extension manifest. Can be single object or split by browser. |
| `plugins` | `Array<RsbuildPlugin>` | Rsbuild plugins array. Use `@rsbuild/plugin-react`, `@addfox/rsbuild-plugin-vue`, etc. |
| `rsbuild` | `object \| function` | Override/extend Rsbuild config. Object: deep-merged. Function: `(base, helpers) => config`. |
| `entry` | `object` | Custom entries. Key = entry name, value = path relative to appDir. |
| `appDir` | `string` | App directory; default `"app"`. |
| `outDir` | `string` | Output directory under `.addfox`; default `"extension"`. |
| `browserPath` | `object` | Browser executable paths for dev mode. `{ chrome, firefox, edge, ... }` |
| `zip` | `boolean` | Whether to create zip output; default `true`. |
| `envPrefix` | `string[]` | Env var prefixes to expose; default `['']` exposes all. Use `['PUBLIC_']` for safety. |
| `cache` | `boolean` | Cache chromium user data dir; default `true`. |
| `hotReload` | `object \| boolean` | Hot reload options: `{ port?: number, autoRefreshContentPage?: boolean }` |
| `debug` | `boolean` | Enable error monitor in dev; default `false`. |
| `report` | `boolean \| object` | Enable Rsdoctor report; default `false`. |

### Manifest Configuration

The `manifest` field accepts:

1. **Single object** — Used for all browsers:
   ```ts
   manifest: {
     manifest_version: 3,
     name: 'My Extension',
     version: '1.0.0'
   }
   ```

2. **Browser split** — Different manifests for Chrome and Firefox:
   ```ts
   const baseManifest = {
     manifest_version: 3,
     name: 'My Extension',
     version: '1.0.0'
   };
   
   manifest: {
     chromium: {
       ...baseManifest,
       minimum_chrome_version: '88'
     },
     firefox: {
       ...baseManifest,
       browser_specific_settings: {
         gecko: { id: 'myextension@example.com' }
       }
     }
   }
   ```

### Dependencies

Install `addfox` as dev dependency:

```bash
# pnpm (recommended)
pnpm add -D addfox

# npm
npm install -D addfox

# yarn
yarn add -D addfox
```

**强烈推荐**: Add `webextension-polyfill` for cross-browser Promise-based API:

```bash
pnpm add webextension-polyfill
pnpm add -D @types/webextension-polyfill
```

Manifest field reference: [rules/manifest-fields.md](rules/manifest-fields.md).
Permission guidance: [rules/permissions.md](rules/permissions.md).

---

## 3. Permissions

### Least Privilege Principle

Request only permissions needed for declared features:

```ts
const manifest = {
  permissions: [
    'storage',           // Settings/caching
    'activeTab',         // Current tab on user gesture
    'scripting',         // Inject scripts/CSS
    'alarms',            // Scheduled tasks
    'notifications',     // Desktop notifications
    'contextMenus',      // Right-click menu
    'offscreen'          // MV3 offscreen documents
  ],
  host_permissions: [
    '*://*.example.com/*'  // Specific sites only
  ],
  optional_permissions: [
    'tabs',              // Request at runtime if needed
    '<all_urls>'         // Broad access (optional)
  ]
};
```

### Permission Patterns by Feature

| Feature | Minimal Permissions | Optional |
|---------|---------------------|----------|
| Basic popup | `storage` | `activeTab` |
| Content script | `activeTab` or specific `host_permissions` | `scripting` |
| Video download | `downloads`, `webRequest`/`declarativeNetRequest` | `tabs` |
| AI sidebar | `sidePanel`, `storage`, `activeTab` | `scripting` |
| Screenshot | `activeTab` | `downloads`, `clipboardWrite` |
| Password manager | `storage`, `scripting`, `activeTab` | `identity` |
| Web3 wallet | `storage`, `scripting`, `activeTab` | `alarms` |

**Note**: For detailed implementation of specific features (video, AI, etc.), see the **extension-functions-best-practices** skill.

Document sensitive permissions (e.g. `<all_urls>`, `tabs`) in store listing and privacy policy.

See [rules/permissions.md](rules/permissions.md) for scenarios and recommendations.

---

## 4. Cross-platform (Chrome / Firefox)

### 4.1 webextension-polyfill（强烈推荐）

**强烈推荐**在 Addfox 项目中使用 [`webextension-polyfill`](https://github.com/mozilla/webextension-polyfill) 来实现跨浏览器兼容。

#### 为什么使用 polyfill

- **统一的 Promise API**: Chrome 的 `chrome.*` API 使用回调，而 Firefox 的 `browser.*` 支持 Promise；polyfill 让 Chrome 也支持 Promise
- **一致的命名空间**: 统一使用 `browser.*` 命名空间，代码在不同浏览器中表现一致
- **更好的类型支持**: 配合 `@types/webextension-polyfill` 获得完整的 TypeScript 类型

#### 安装

```bash
# npm
npm install webextension-polyfill
npm install -D @types/webextension-polyfill

# pnpm
pnpm add webextension-polyfill
pnpm add -D @types/webextension-polyfill

# yarn
yarn add webextension-polyfill
yarn add -D @types/webextension-polyfill
```

#### 使用示例

**app/background/index.ts**
```typescript
import browser from 'webextension-polyfill';

// 使用 Promise API（在 Chrome 和 Firefox 中都可用）
browser.runtime.onInstalled.addListener(async (details) => {
  if (details.reason === 'install') {
    console.log('Extension installed!');
    await browser.storage.local.set({ installedAt: Date.now() });
  }
});

// 消息处理
browser.runtime.onMessage.addListener(async (message, sender) => {
  if (message.from === 'popup') {
    return { received: true, timestamp: Date.now() };
  }
});

// 使用 browser.action (Chrome) / browser.browserAction (Firefox 自动映射)
browser.action.onClicked.addListener(async (tab) => {
  await browser.scripting.executeScript({
    target: { tabId: tab.id! },
    func: () => alert('Hello from Addfox!'),
  });
});
```

**app/popup/index.tsx**
```typescript
import browser from 'webextension-polyfill';

async function init() {
  // 获取当前活动标签页
  const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
  
  // 发送消息到 content script
  const response = await browser.tabs.sendMessage(tab.id!, { 
    type: 'GET_PAGE_INFO',
    from: 'popup'
  });
  
  document.getElementById('title')!.textContent = response.title;
}

init();
```

**app/content/index.ts**
```typescript
import browser from 'webextension-polyfill';

// 监听来自 background/popup 的消息
browser.runtime.onMessage.addListener((message, sender) => {
  if (message.type === 'GET_PAGE_INFO' && message.from === 'popup') {
    return Promise.resolve({
      title: document.title,
      url: location.href,
      h1: document.querySelector('h1')?.textContent
    });
  }
});

// 使用 storage API
async function saveData(key: string, value: any) {
  await browser.storage.local.set({ [key]: value });
  const result = await browser.storage.local.get(key);
  console.log('Saved:', result);
}
```

**app/options/index.tsx**
```typescript
import browser from 'webextension-polyfill';

const form = document.getElementById('options-form') as HTMLFormElement;

// 加载保存的设置
async function loadSettings() {
  const { apiKey, theme } = await browser.storage.sync.get(['apiKey', 'theme']);
  (form.elements.namedItem('apiKey') as HTMLInputElement).value = apiKey || '';
  (form.elements.namedItem('theme') as HTMLSelectElement).value = theme || 'light';
}

// 保存设置
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  await browser.storage.sync.set({
    apiKey: formData.get('apiKey'),
    theme: formData.get('theme')
  });
  // 显示保存成功提示
  await browser.notifications.create({
    type: 'basic',
    iconUrl: browser.runtime.getURL('icon.png'),
    title: '设置已保存',
    message: '您的首选项已更新'
  });
});

loadSettings();
```

#### 配置 tsconfig.json

确保 TypeScript 能正确识别 `webextension-polyfill` 的类型：

```json
{
  "compilerOptions": {
    "types": ["webextension-polyfill"]
  }
}
```

### 4.2 Manifest 差异处理

Use `manifest: { chromium: {...}, firefox: {...} }` when fields differ:

```ts
const baseManifest = {
  manifest_version: 3,
  name: 'My Extension',
  version: '1.0.0'
};

export default defineConfig({
  manifest: {
    chromium: {
      ...baseManifest,
      minimum_chrome_version: '88'
    },
    firefox: {
      ...baseManifest,
      browser_specific_settings: {
        gecko: {
          id: 'myextension@example.com',
          strict_min_version: '109.0'
        }
      }
    }
  }
});
```

Build for specific target:
```bash
addfox dev -b chrome     # or chromium, firefox, edge, brave
addfox build -b firefox  # Firefox-specific build
```

See [reference.md](reference.md#cross-platform).

---

## 5. UI frameworks

### Supported Frameworks

| Framework | Plugin Package | Install Command |
|-----------|----------------|-----------------|
| React | `@rsbuild/plugin-react` | `pnpm add -D @rsbuild/plugin-react` |
| Vue 3 | `@addfox/rsbuild-plugin-vue` | `pnpm add -D @addfox/rsbuild-plugin-vue` |
| Preact | `@rsbuild/plugin-preact` | `pnpm add -D @rsbuild/plugin-preact` |
| Svelte | `@rsbuild/plugin-svelte` | `pnpm add -D @rsbuild/plugin-svelte` |
| Solid | `@rsbuild/plugin-solid` | `pnpm add -D @rsbuild/plugin-solid` |
| Vanilla | None | No plugin needed |

### Setup Example (React)

```ts
// addfox.config.ts
import { defineConfig } from 'addfox';
import { pluginReact } from '@rsbuild/plugin-react';

export default defineConfig({
  plugins: [pluginReact()],
  manifest: { ... }
});
```

```json
// package.json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@rsbuild/plugin-react": "^1.2.0"
  }
}
```

### Setup Example (Vue)

```ts
// addfox.config.ts
import { defineConfig } from 'addfox';
import vue from '@addfox/rsbuild-plugin-vue';

export default defineConfig({
  plugins: [vue()],
  manifest: { ... }
});
```

Entry files remain JS/TS/JSX/TSX/Vue (e.g. `app/popup/index.tsx`).

---

## 6. Styles

### Tailwind CSS v4

Addfox uses Tailwind CSS v4 with PostCSS:

```bash
pnpm add -D tailwindcss @tailwindcss/postcss postcss
```

```js
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};
```

Import Tailwind in your CSS:

```css
/* app/popup/index.css */
@import 'tailwindcss';
```

```tsx
// app/popup/index.tsx
import './index.css';
```

### Tailwind CSS v3 (Legacy)

For Tailwind v3, use traditional PostCSS configuration:

```bash
pnpm add -D tailwindcss postcss autoprefixer
```

```js
// postcss.config.mjs
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

```js
// tailwind.config.js
export default {
  content: ['./app/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### UnoCSS

```bash
pnpm add -D unocss @unocss/postcss
```

```js
// postcss.config.mjs
export default {
  plugins: {
    '@unocss/postcss': {},
  },
};
```

### Sass/Less

Rsbuild has built-in support. Just install and use:

```bash
pnpm add -D sass
```

```scss
/* app/popup/index.scss */
$primary: #3b82f6;
.button { background: $primary; }
```

### CSS Scoping

Prefer scoped styles or BEM/utility classes to avoid leaking into page:

```css
/* Use prefix for content scripts */
.my-extension-popup { ... }
.my-extension-content { ... }
```

Content scripts should inject minimal, prefixed CSS when not using Shadow DOM or iframe isolation.

---

## 7. Messaging

### Include Message Origin

Always include a `from` (or equivalent) field in message payloads:

```ts
// popup sending
browser.runtime.sendMessage({
  from: 'popup',
  action: 'getSettings',
  payload: {}
});

// background receiving
browser.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.from === 'popup' && msg.action === 'getSettings') {
    // handle
  }
});
```

Senders can be: `"background"`, `"content"`, `"popup"`, `"options"`, or custom IDs.

### Message Types by Context

| From | To | API | Example |
|------|-----|-----|---------|
| Popup | Background | `browser.runtime.sendMessage` | Get settings |
| Popup | Content | `browser.tabs.sendMessage` | Page interaction |
| Content | Background | `browser.runtime.sendMessage` | Report event |
| Background | Content | `browser.tabs.sendMessage` | Inject script |
| Background | Popup | Not directly possible | Use storage or message passing via content |

### Content ↔ Page Script

Use `window.postMessage` + custom events only for content ↔ page script when needed, and validate origin:

```ts
// Content script
window.postMessage({
  from: 'extension-content',
  type: 'REQUEST_DATA'
}, '*');

// Listen from page
window.addEventListener('message', (e) => {
  if (e.origin !== location.origin) return;
  if (e.data.from === 'page-script') {
    // handle
  }
});
```

See [rules/messaging.md](rules/messaging.md) for detailed patterns.

---

## 8. Content UI (injecting DOM in pages)

When the user needs to **create content UI** or **inject DOM into web pages** from a content script, use Addfox's built-in helpers from **`@addfox/utils`** instead of manually creating shadow roots or iframes.

### Three Isolation Levels

| Method | Wrapper | Isolation | Use When |
|--------|---------|-----------|----------|
| `defineShadowContentUI` | Shadow DOM | Style only | Style isolation, single mount root |
| `defineIframeContentUI` | iframe | Full (JS+CSS) | Full isolation from page |
| `defineContentUI` | Plain element | None | No isolation needed |

### Usage

```ts
import { defineShadowContentUI, defineIframeContentUI, defineContentUI } from '@addfox/utils';

// Shadow DOM - most common
const mountShadow = defineShadowContentUI({
  name: 'my-content-ui',        // Must contain hyphen
  target: 'body',
  attr: { 
    id: 'my-root', 
    style: 'position:fixed;bottom:16px;right:16px;z-index:2147483647;' 
  },
  injectMode: 'append'
});

// React example
const root = mountShadow();
createRoot(root).render(<MyComponent />);

// iframe - full isolation
const mountIframe = defineIframeContentUI({
  target: 'body',
  attr: { class: 'my-iframe-ui' }
});

// Plain element - no isolation
const mountPlain = defineContentUI({
  tag: 'div',
  target: 'body',
  attr: { id: 'content-ui-root' }
});
```

### When to Call Mount

Ensure the target exists:

```ts
function mountUI() {
  const root = mountShadow();
  createRoot(root).render(<App />);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mountUI);
} else {
  mountUI();
}
```

### Manifest and CSS

When using `defineShadowContentUI` or `defineIframeContentUI`, the framework may not auto-fill `content_scripts.css` in the manifest (CSS is injected at runtime). Import your styles in the content entry:

```ts
// app/content/index.ts
import './styles.css';  // Bundled and injected automatically
import { defineShadowContentUI } from '@addfox/utils';
```

See [rules/content-ui.md](rules/content-ui.md) for API details and examples.

---

## 9. Common Feature Implementations

When implementing specific extension features, combine Addfox best practices with the **extension-functions-best-practices** skill:

| Feature Category | Addfox Setup | See Also |
|-----------------|-------------|----------|
| **Video Enhancement** | `content` entry with Shadow UI | extension-functions-best-practices (Video) |
| **Video Download** | `background` + `webRequest` | extension-functions-best-practices (Video) |
| **AI Sidebar** | `sidepanel` entry | extension-functions-best-practices (AI) |
| **Page Translation** | `content` entry | extension-functions-best-practices (Translation) |
| **Screenshot** | `activeTab` permission | extension-functions-best-practices (Image) |
| **Password Manager** | `storage` + `scripting` | extension-functions-best-practices (Password Manager) |
| **Web3 Wallet** | `content` + `offscreen` | extension-functions-best-practices (Web3) |

**Example**: Building an AI sidebar extension:
1. Use Addfox for `sidepanel` entry setup
2. Use extension-functions-best-practices for AI SDK integration (Vercel AI SDK, LangChain)

---

## 10. Rsbuild Configuration (Advanced)

Use the `rsbuild` field to override or extend Rsbuild configuration:

### Object Form (Deep Merge)

```ts
export default defineConfig({
  rsbuild: {
    source: {
      alias: {
        '@': './app',
      },
    },
    output: {
      copy: [
        { from: './public', to: '.' }
      ]
    }
  }
});
```

### Function Form (Full Control)

```ts
export default defineConfig({
  rsbuild: (base, helpers) => {
    return helpers.merge(base, {
      source: {
        define: {
          'process.env.API_URL': JSON.stringify('https://api.example.com')
        }
      }
    });
  }
});
```

### Common Rsbuild Options

| Option | Description |
|--------|-------------|
| `source.alias` | Path aliases |
| `source.define` | Global constants |
| `output.copy` | Static asset copying |
| `output.assetPrefix` | Asset URL prefix |
| `server.port` | Dev server port |
| `dev.hmr` | HMR configuration |

---

## Checklist (when generating or modifying extension)

- [ ] Entry: file-based under `app/` with reserved names, or explicit `entry` in config.
- [ ] Config: use `rsbuild` (not `rsbuildConfig`) for Rsbuild overrides.
- [ ] Manifest: use `{ chromium: {...}, firefox: {...} }` for browser split.
- [ ] Plugins: use `@rsbuild/plugin-*` or `@addfox/rsbuild-plugin-*` packages.
- [ ] Permissions: minimal set; sensitive ones documented.
- [ ] Cross-browser: **use `webextension-polyfill` with `browser.*` API**.
- [ ] Messaging: payload includes `from` for routing/security.
- [ ] Content UI: use `defineShadowContentUI` / `defineIframeContentUI` / `defineContentUI` from `@addfox/utils`.
- [ ] Styles: Tailwind v4 uses `@tailwindcss/postcss` in `postcss.config.mjs`.
- [ ] Feature implementation: reference extension-functions-best-practices for video/AI/etc.

---

## Additional resources

- Detailed config, CLI, and manifest: [reference.md](reference.md).
- Manifest field usage: [rules/manifest-fields.md](rules/manifest-fields.md).
- Permissions by scenario: [rules/permissions.md](rules/permissions.md).
- Messaging patterns: [rules/messaging.md](rules/messaging.md).
- Content UI: [rules/content-ui.md](rules/content-ui.md).
- Debugging: [addfox-debugging skill](../addfox-debugging/SKILL.md).
- Testing: [addfox-testing skill](../addfox-testing/SKILL.md).
- Feature implementations: [extension-functions-best-practices skill](../extension-functions-best-practices/SKILL.md).
