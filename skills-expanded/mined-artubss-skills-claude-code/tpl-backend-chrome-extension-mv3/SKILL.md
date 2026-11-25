---
name: tpl-backend-chrome-extension-mv3
description: Template do pack (backend/12-chrome-extension-mv3.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/12-chrome-extension-mv3.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Chrome Extension Manifest V3

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/12-chrome-extension-mv3.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Platform:** Chrome Extension Manifest V3
- **Language:** TypeScript 5.x (strict)
- **UI Framework:** React 19 (popup + options pages)
- **Build tool:** Vite + CRXJS v2
- **Styling:** Tailwind CSS v3
- **State:** Zustand (popup) + chrome.storage.sync
- **Testing:** Vitest + happy-dom (unit), Playwright (E2E)

---

## PROJECT STRUCTURE
```
src/
├── background/
│   └── service-worker.ts     # Background service worker
├── content/
│   ├── index.ts              # Content script entry
│   └── injected.ts           # Injected script (isolated world)
├── popup/
│   ├── index.html
│   ├── App.tsx
│   └── components/
├── options/
│   ├── index.html
│   └── App.tsx
├── shared/
│   ├── messages.ts           # Message type definitions
│   ├── storage.ts            # chrome.storage wrappers
│   └── utils.ts
public/
└── icons/
manifest.json
vite.config.ts
tsconfig.json
```

---

## ARCHITECTURE RULES
1. **Service worker is stateless** — it can be terminated at any time; never rely on in-memory state; use `chrome.storage`.
2. **Content scripts are isolated** — they run in the page context but cannot access page JS variables directly; use `window.postMessage` or injected scripts.
3. **Message passing is typed** — define a discriminated union `AppMessage`; use `chrome.runtime.sendMessage` only with typed messages.
4. **Permissions are minimal** — request only what is needed; do not use `<all_urls>` if a specific match pattern suffices.
5. **No eval / dynamic code execution** — MV3 CSP blocks it; build everything at compile time.
6. **storage.sync for user preferences** — `storage.local` for large or sensitive data.
7. **CRXJS handles HMR** — never manually reload in development.

---

## MANIFEST V3 CONFIGURATION

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "Production-ready Chrome Extension",
  "permissions": [
    "storage",
    "activeTab",
    "scripting"
  ],
  "host_permissions": [
    "https://api.example.com/*"
  ],
  "background": {
    "service_worker": "src/background/service-worker.ts",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["https://*.example.com/*"],
      "js": ["src/content/index.ts"],
      "run_at": "document_idle"
    }
  ],
  "action": {
    "default_popup": "src/popup/index.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "options_ui": {
    "page": "src/options/index.html",
    "open_in_tab": true
  }
}
```

---

## TYPED MESSAGE PASSING

```typescript
// src/shared/messages.ts
export type AppMessage =
  | { type: 'GET_PAGE_DATA' }
  | { type: 'PAGE_DATA'; payload: { title: string; url: string } }
  | { type: 'SET_BADGE'; count: number }
  | { type: 'OPEN_OPTIONS' }

// src/background/service-worker.ts
import type { AppMessage } from '../shared/messages'

// Service worker: listen for messages from popup or content
chrome.runtime.onMessage.addListener(
  (message: AppMessage, sender, sendResponse) => {
    if (message.type === 'GET_PAGE_DATA') {
      // Query active tab
      chrome.tabs.query({ active: true, currentWindow: true }, async ([tab]) => {
        if (!tab.id) return
        const results = await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: () => ({ title: document.title, url: location.href }),
        })
        sendResponse({ type: 'PAGE_DATA', payload: results[0].result })
      })
      return true // keeps channel open for async response
    }

    if (message.type === 'SET_BADGE') {
      chrome.action.setBadgeText({ text: String(message.count) })
      chrome.action.setBadgeBackgroundColor({ color: '#6366f1' })
    }
  }
)

// src/popup/App.tsx — sending messages
const getPageData = async () => {
  const response = await chrome.runtime.sendMessage<AppMessage, AppMessage>({
    type: 'GET_PAGE_DATA',
  })
  if (response.type === 'PAGE_DATA') setData(response.payload)
}
```

---

## STORAGE API WRAPPER

```typescript
// src/shared/storage.ts
export interface ExtConfig {
  theme:       'light' | 'dark'
  apiKey:      string
  autoCapture: boolean
}

const DEFAULTS: ExtConfig = {
  theme: 'light', apiKey: '', autoCapture: false,
}

export const storage = {
  async get(): Promise<ExtConfig> {
    const raw = await chrome.storage.sync.get(DEFAULTS)
    return raw as ExtConfig
  },
  async set(patch: Partial<ExtConfig>): Promise<void> {
    await chrome.storage.sync.set(patch)
  },
  onChange(cb: (changes: Partial<ExtConfig>) => void): void {
    chrome.storage.sync.onChanged.addListener((changes) => {
      const patch: Partial<ExtConfig> = {}
      for (const [key, { newValue }] of Object.entries(changes)) {
        (patch as Record<string, unknown>)[key] = newValue
      }
      cb(patch)
    })
  },
}
```

---

## CONTENT SCRIPT ISOLATION

```typescript
// src/content/index.ts — runs in ISOLATED world; can read DOM
import type { AppMessage } from '../shared/messages'

// Observe DOM changes and notify background
const observer = new MutationObserver(() => {
  const count = document.querySelectorAll('[data-item]').length
  chrome.runtime.sendMessage<AppMessage>({ type: 'SET_BADGE', count })
})
observer.observe(document.body, { childList: true, subtree: true })

// src/content/injected.ts — access page JS from MAIN world
// Injected via chrome.scripting.executeScript with world: "MAIN"
// NOTE: Cannot use chrome.* APIs here
window.addEventListener('message', (event) => {
  if (event.source !== window || event.data?.source !== 'my-ext') return
  // Bridge page data → isolated context via postMessage
  window.postMessage({ source: 'my-ext-page', data: window.__appState }, '*')
})
```

---

## ROUTING TABLE (Message Type → Handler)

| Message Type | From | To | Action |
|-------------|------|----|--------|
| `GET_PAGE_DATA` | Popup | Service Worker | Execute script in active tab |
| `PAGE_DATA` | Service Worker | Popup | Return title + URL |
| `SET_BADGE` | Content Script | Service Worker | Update badge count |
| `OPEN_OPTIONS` | Popup | Service Worker | `chrome.runtime.openOptionsPage()` |
| `storage.get` | Any | chrome.storage.sync | Read config |
| `storage.set` | Options page | chrome.storage.sync | Write config |
| content→bg | Content | Service Worker | DOM event notification |
| tab.onUpdated | — | Service Worker | React on navigation |

---

## QUALITY GATES
- [ ] `tsc --noEmit` — zero errors
- [ ] No `eval`, `new Function()`, or `innerHTML = userInput`
- [ ] Permissions declared in `manifest.json` — nothing requested at runtime that isn't declared
- [ ] `vitest run` passes all unit tests
- [ ] `npm run build` produces clean `dist/` (no TS source, no sourcemaps in prod)
- [ ] Extension loads in Chrome without errors in `chrome://extensions/`
- [ ] Service worker message handlers all `return true` if async
- [ ] Content script does not access `chrome.storage` directly in `MAIN` world scripts

---

## FORBIDDEN
- ❌ `eval()` or `document.write()` — blocked by MV3 CSP
- ❌ Remote scripts loaded at runtime — all code must be bundled
- ❌ `chrome.tabs.executeScript` (MV2 API) — use `chrome.scripting.executeScript`
- ❌ Storing tokens in `localStorage` — use `chrome.storage.local`
- ❌ `background.js` as classic script with DOM access — SW has no DOM
- ❌ `<all_urls>` host permission without clear justification
- ❌ Hardcoded API keys in extension source — fetch from storage
- ❌ Long-running tasks in service worker without keepalive strategy
