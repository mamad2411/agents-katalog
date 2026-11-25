---
name: wxt-chrome-extension
description: WXT Chrome extension development: Manifest V3, content scripts, service workers, Chrome APIs, popup/options pages, cross-browser compatibility, Chrome Web Store publishing, testing, and debugging.
origin: AI Dev Kit
---
# WXT Chrome Extension

Use this skill when building, modifying, or debugging Chrome extensions using the WXT framework, or when working with Manifest V3 extension architecture.

## When to Use

- Scaffolding a new WXT extension project or adding entrypoints
- Implementing content scripts, background service workers, popup, or options pages
- Configuring Manifest V3 permissions, host_permissions, or CSP
- Setting up Chrome API integrations (tabs, storage, identity, contextMenus, scripting)
- Preparing for Chrome Web Store submission
- Debugging extension issues via chrome://extensions DevTools

## Core Concepts

### WXT Project Structure
```
my-extension/
├── entrypoints/
│   ├── background.ts          # Service worker (MV3)
│   ├── content.ts             # Content script (auto-injected)
│   ├── content/index.tsx      # Content script with UI overlay
│   ├── popup/index.html       # Popup page (React)
│   ├── popup/index.tsx
│   ├── options/index.html     # Options page
│   └── options/index.tsx
├── assets/                    # Icons, logos
├── wxt.config.ts              # WXT configuration
├── package.json
└── tsconfig.json
```

### wxt.config.ts Essentials
```ts
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
    permissions: [
      'storage',
      'tabs',
      'activeTab',
      'contextMenus',
      'alarms',
      'notifications',
    ],
    host_permissions: [
      'https://*.example.com/*',
    ],
    action: {
      default_popup: 'popup.html',
      default_icon: {
        16: 'icon-16.png',
        32: 'icon-32.png',
        48: 'icon-48.png',
        128: 'icon-128.png',
      },
    },
    options_ui: {
      page: 'options.html',
      open_in_tab: true,
    },
  },
});
```

### Manifest V3 Key Changes from V2
- **Background scripts → Service workers**: No persistent background pages; stateless event-driven workers
- **webRequest → Declarative Net Request**: Blocking webRequest replaced; use `declarativeNetRequest` for request modification
- **Remote code banned**: All code must be bundled; no loading scripts from CDNs
- **eval() restricted**: Content Security Policy blocks `unsafe-eval`; use `chrome.runtime.getURL()` for bundled resources
- **executeScript → Scripting API**: Use `chrome.scripting.executeScript()` with proper world specification

### Content Scripts
```ts
// entrypoints/content.ts
export default defineContentScript({
  matches: ['https://*.example.com/*'],
  runAt: 'document_idle',
  world: 'ISOLATED', // ISOLATED (extension context) or MAIN (page context)
  main() {
    // DOM manipulation
    const observer = new MutationObserver((mutations) => {
      // React to DOM changes
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Message passing to background
    chrome.runtime.sendMessage({ type: 'PAGE_LOADED', url: window.location.href });
  },
});
```

### Background Service Worker
```ts
// entrypoints/background.ts
export default defineBackground(() => {
  // Service worker lifecycle: starts/stops based on events
  chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
      chrome.tabs.create({ url: 'options.html' });
    }
  });

  // Alarms for periodic work
  chrome.alarms.create('cleanup', { periodInMinutes: 60 });
  chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'cleanup') {
      // Periodic cleanup
    }
  });

  // Message handling
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'GET_SETTINGS') {
      chrome.storage.local.get('settings', sendResponse);
      return true; // Keep message channel open for async response
    }
  });
});
```

### Communication Patterns
```
Content Script ←→ Background Worker ←→ Popup/Options

// Content → Background
chrome.runtime.sendMessage({ type: 'DATA', payload: data });

// Background → Content (specific tab)
chrome.tabs.sendMessage(tabId, { type: 'UPDATE', data });

// Popup → Background
const response = await chrome.runtime.sendMessage({ type: 'QUERY' });

// Long-lived connections (ports)
const port = chrome.runtime.connect({ name: 'stream' });
port.postMessage({ type: 'INIT' });
port.onMessage.addListener(handleMessage);
```

### Chrome APIs Quick Reference
| API | Permission | Use Case |
|-----|-----------|----------|
| `chrome.storage` | `storage` | Persist settings, cache data |
| `chrome.tabs` | `tabs` | Query, create, update, remove tabs |
| `chrome.identity` | `identity` | OAuth2, Google Sign-In |
| `chrome.contextMenus` | `contextMenus` | Right-click menu items |
| `chrome.scripting` | `scripting` | Programmatic content script injection |
| `chrome.notifications` | `notifications` | System notifications |
| `chrome.alarms` | `alarms` | Scheduled periodic tasks |

### Chrome Web Store Publishing Checklist
- [ ] Icons: 16, 32, 48, 128 PNG in `assets/`
- [ ] Screenshots: 1280x800, minimum 1, maximum 5
- [ ] Description: Clear value proposition, feature list
- [ ] Privacy policy: Required if accessing user data, hosted URL
- [ ] Version incremented in `wxt.config.ts` manifest
- [ ] Build: `wxt build --mode production` then `wxt zip`
- [ ] Test in clean Chrome profile before submission

## Anti-Patterns

- **Storing state in service worker**: Service workers are terminated when idle; use `chrome.storage` for persistence
- **Requesting excessive permissions**: Request minimum necessary; use optional permissions for rarely-used features
- **Using eval or inline scripts in popup**: CSP blocks this; bundle all code
- **Ignoring world isolation**: Content scripts in ISOLATED world can't access page JS; use `world: 'MAIN'` explicitly when needed
- **Hardcoding host_permissions**: Use patterns (`https://*.example.com/*`) not exact URLs
- **Not handling service worker lifecycle**: Events may arrive after worker restart; design for stateless handlers

## Best Practices

- Use WXT's auto-imports for Chrome APIs — no manual imports needed
- Prefer `chrome.storage.local` for large data, `chrome.storage.sync` for settings that should sync across devices
- Test content script injection at `document_idle` for most cases; use `document_start` for style injection
- Use alarms instead of `setTimeout`/`setInterval` in service workers (timers don't survive worker suspension)
- Version your extension semantically; Chrome Web Store rejects duplicate version numbers
- Keep popup lightweight; defer heavy computation to background worker
- Use `chrome.action.setBadgeText()` for status indicators

## Related Skills

- `frontend-patterns` — React patterns for popup/options pages
- `e2e-testing` — Playwright testing with Chrome extension loading
- `security-review` — Permission auditing, CSP compliance
- `coding-standards` — TypeScript configuration for WXT projects
