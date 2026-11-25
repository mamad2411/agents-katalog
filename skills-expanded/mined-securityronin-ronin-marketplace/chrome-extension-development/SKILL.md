---
name: chrome-extension-development
description: Use when building Chrome extensions (Manifest V3). Covers floating panel architecture, sidepanel API, storage patterns, message passing, content scripts, SPA navigation detection, context menus, Vitest testing, Playwright E2E, and common pitfalls.
---

# Chrome Extension Development

Guidelines for building and maintaining Chrome browser extensions.

---

## Build System Architecture

### The Source vs Dist Problem

Chrome extensions require specific files in a loadable directory structure. Common confusion arises from mixing source and generated files.

**Typical bundler behavior (Vite, esbuild, webpack):**
- Compiles TypeScript/JavaScript: `src/*.ts` → `dist/*.js`
- May bundle imported CSS into JS
- Does NOT automatically copy: HTML, standalone CSS, manifest.json, static assets

### Recommended: Vite with publicDir

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  build: {
    outDir: "dist",
    copyPublicDir: true,  // Copies public/ to dist/
    rollupOptions: {
      input: {
        background: resolve(__dirname, "src/background.ts"),
        sidepanel: resolve(__dirname, "src/sidepanel.ts"),
        // Add more entry points as needed
      },
      output: {
        entryFileNames: "[name].js",
      },
    },
  },
  publicDir: "public",  // HTML, CSS, manifest.json, icons
  test: {
    environment: "jsdom",
    exclude: ["**/node_modules/**", "**/e2e/**"],
  },
});
```

**Project structure:**
```
src/
  background.ts       # Service worker
  sidepanel.ts        # Sidepanel UI logic
  content.ts          # Content script (if needed)
  storage.ts          # Storage utilities
public/
  manifest.json       # Extension manifest
  sidepanel.html      # Sidepanel markup
  styles.css          # Styles
  icons/              # Extension icons
dist/                 # Generated (gitignore this)
```

---

## Manifest V3 Configuration

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "0.1.0",
  "description": "Description",
  "permissions": [
    "activeTab",
    "storage",
    "sidePanel",
    "scripting",
    "contextMenus",
    "notifications"
  ],
  "side_panel": {
    "default_path": "sidepanel.html"
  },
  "commands": {
    "action-name": {
      "suggested_key": {
        "default": "Alt+P",
        "mac": "Alt+P"
      },
      "description": "Command description"
    }
  },
  "action": {
    "default_title": "Extension Name",
    "default_icon": {
      "16": "icons/icon16.png",
      "32": "icons/icon32.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "background": {
    "service_worker": "background.js",
    "type": "module"
  },
  "icons": {
    "16": "icons/icon16.png",
    "32": "icons/icon32.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

### Manifest V3 Notes

- Service workers replace background pages (no persistent background)
- `chrome.scripting.executeScript` replaces `chrome.tabs.executeScript`
- Host permissions moved from `permissions` to `host_permissions`
- Remote code execution prohibited; all code must be bundled

---

## Content Scripts

Content scripts run in web page context with limited Chrome API access.

### Manifest Configuration

```json
{
  "content_scripts": [
    {
      "matches": ["*://*.example.com/*"],
      "js": ["content.js"],
      "css": ["styles.css"],
      "run_at": "document_idle"
    }
  ],
  "host_permissions": [
    "*://*.example.com/*"
  ],
  "web_accessible_resources": [
    {
      "resources": ["styles.css", "images/*"],
      "matches": ["*://*.example.com/*"]
    }
  ]
}
```

**`run_at` options:**
- `document_start` - Before DOM is constructed (for early interception)
- `document_end` - DOM ready, before images/subframes
- `document_idle` - After DOM complete (default, safest)

### Content Script Lifecycle

```typescript
// content.ts
import { logger } from './logger';

// Log when script is parsed (debugging lifecycle issues)
logger.debug('Content script starting');

// Check if extension context is still valid (SPA navigation can invalidate)
function isExtensionContextValid(): boolean {
  try {
    return chrome?.runtime?.id !== undefined;
  } catch {
    return false;
  }
}

// Safe initialization
async function init(): Promise<void> {
  if (!isExtensionContextValid()) {
    logger.warn('Extension context invalid, skipping init');
    return;
  }

  // Wait for page to be ready
  if (document.readyState === 'loading') {
    await new Promise(resolve =>
      document.addEventListener('DOMContentLoaded', resolve)
    );
  }

  // Your initialization code
  setupUI();
  observePageChanges();
}

init().catch(logger.error);
```

### Communicating with Background

```typescript
// content.ts - Send to background
async function sendToBackground(message: unknown): Promise<unknown> {
  if (!isExtensionContextValid()) return null;

  return new Promise((resolve) => {
    try {
      chrome.runtime.sendMessage(message, (response) => {
        if (chrome.runtime.lastError) {
          resolve(null);
          return;
        }
        resolve(response);
      });
    } catch {
      resolve(null);
    }
  });
}

// background.ts - Listen for messages
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'getProfile') {
    fetchProfile(message.id).then(sendResponse);
    return true; // Keep channel open for async response
  }
});
```

### Injecting UI Elements

```typescript
function createFloatingPanel(): HTMLElement {
  const panel = document.createElement('div');
  panel.id = 'my-extension-panel';
  panel.style.cssText = `
    position: fixed;
    top: 100px;
    right: 20px;
    z-index: 2147483647;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  `;

  // Isolate styles with shadow DOM
  const shadow = panel.attachShadow({ mode: 'closed' });
  shadow.innerHTML = `
    <style>/* Your isolated styles */</style>
    <div class="content">...</div>
  `;

  document.body.appendChild(panel);
  return panel;
}
```

---

## Floating Panel Architecture

For complex floating UI that persists across page navigation, use a factory pattern with state management.

### Panel Interface

```typescript
export enum PanelState {
  Minimized = 'minimized',
  Expanded = 'expanded',
}

export interface Position {
  x: number;
  y: number;
}

export interface Panel {
  element: HTMLElement;
  getState: () => PanelState;
  toggle: () => void;
  setPosition: (x: number, y: number) => void;
  getPosition: () => Position;
  setContent: (html: string) => void;
  onAction: (callback: () => void) => void;
  destroy: () => void;
}
```

### Panel Factory

```typescript
export function createPanel(container: HTMLElement): Panel {
  let state: PanelState = PanelState.Minimized;
  let position: Position = { x: 20, y: 20 };
  let actionCallback: (() => void) | null = null;

  // Create main element
  const element = document.createElement('div');
  element.className = 'sr-panel sr-panel--minimized sr-panel--draggable';
  element.style.transform = `translate(${position.x}px, ${position.y}px)`;

  // Minimized orb (clickable indicator)
  const orb = document.createElement('div');
  orb.className = 'sr-panel__orb sr-panel__orb--visible';
  element.appendChild(orb);

  // Expanded content container
  const content = document.createElement('div');
  content.className = 'sr-panel__content';
  element.appendChild(content);

  container.appendChild(element);

  function toggle(): void {
    if (state === PanelState.Minimized) {
      state = PanelState.Expanded;
      element.classList.remove('sr-panel--minimized');
      element.classList.add('sr-panel--expanded');
      orb.classList.remove('sr-panel__orb--visible');
      content.classList.add('sr-panel__content--visible');
    } else {
      state = PanelState.Minimized;
      element.classList.remove('sr-panel--expanded');
      element.classList.add('sr-panel--minimized');
      orb.classList.add('sr-panel__orb--visible');
      content.classList.remove('sr-panel__content--visible');
    }
  }

  // Toggle on orb click
  orb.addEventListener('click', toggle);

  return {
    element,
    getState: () => state,
    toggle,
    setPosition: (x, y) => {
      position = { x, y };
      element.style.transform = `translate(${x}px, ${y}px)`;
    },
    getPosition: () => ({ ...position }),
    setContent: (html) => {
      content.innerHTML = html;
      // Re-attach minimize button listener after content update
      const minimizeBtn = content.querySelector('.sr-panel__minimize');
      minimizeBtn?.addEventListener('click', toggle);
    },
    onAction: (callback) => { actionCallback = callback; },
    destroy: () => element.remove(),
  };
}
```

### Drag and Drop with Position Persistence

```typescript
let isDragging = false;
let dragOffset = { x: 0, y: 0 };

function setupDragListeners(panel: Panel): void {
  const element = panel.element;

  element.addEventListener('mousedown', (e: MouseEvent) => {
    // Don't drag if clicking buttons
    const target = e.target as HTMLElement;
    if (target.tagName === 'BUTTON' || target.closest('button')) return;

    isDragging = true;
    const pos = panel.getPosition();
    dragOffset = {
      x: e.clientX - pos.x,
      y: e.clientY - pos.y,
    };
    element.style.cursor = 'grabbing';
  });

  document.addEventListener('mousemove', (e: MouseEvent) => {
    if (!isDragging) return;
    const newX = e.clientX - dragOffset.x;
    const newY = e.clientY - dragOffset.y;
    panel.setPosition(newX, newY);
  });

  document.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      panel.element.style.cursor = 'grab';
      // Persist position
      savePosition(panel.getPosition());
    }
  });
}

function savePosition(position: Position): void {
  if (!isExtensionContextValid()) return;
  chrome.storage.sync.set({ panelPosition: position });
}

async function loadPosition(): Promise<Position | null> {
  if (!isExtensionContextValid()) return null;
  return new Promise((resolve) => {
    chrome.storage.sync.get(['panelPosition'], (result) => {
      resolve(result.panelPosition || null);
    });
  });
}
```

### CSS Injection via chrome.runtime.getURL

```typescript
function injectStyles(): void {
  if (document.getElementById('my-extension-styles')) return;
  if (!isExtensionContextValid()) return;

  const link = document.createElement('link');
  link.id = 'my-extension-styles';
  link.rel = 'stylesheet';
  link.href = chrome.runtime.getURL('panel.css');
  document.head.appendChild(link);
}
```

### Floating Panel CSS

```css
/* CSS Variables for theming */
:root {
  --panel-bg: #1a1a1a;
  --panel-accent: #c9a227;
  --panel-text: #fafafa;
  --panel-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 10px 20px rgba(0,0,0,0.15);
  --panel-transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Panel Container - Fixed Position */
.sr-panel {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 999999;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  transition: var(--panel-transition);
}

.sr-panel--draggable {
  cursor: grab;
}

.sr-panel--draggable:active {
  cursor: grabbing;
}

/* Minimized Orb */
.sr-panel__orb {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--panel-bg);
  border: 2px solid var(--panel-accent);
  box-shadow: var(--panel-shadow);
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--panel-transition);
}

.sr-panel__orb--visible {
  display: flex;
}

.sr-panel__orb:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(201, 162, 39, 0.3), var(--panel-shadow);
}

/* Pulse animation for alerts */
.sr-panel__orb--alert {
  animation: sr-pulse 2s ease-in-out infinite;
}

@keyframes sr-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(201, 162, 39, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(201, 162, 39, 0); }
}

/* Expanded Content */
.sr-panel__content {
  display: none;
  width: 300px;
  background: #f5f2eb;
  border-radius: 8px;
  box-shadow: var(--panel-shadow);
  overflow: hidden;
  border: 1px solid var(--panel-accent);
}

.sr-panel__content--visible {
  display: block;
  animation: sr-expand 0.3s ease-out;
}

@keyframes sr-expand {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
```

### Progress/Loading States

```typescript
interface ExtractionProgress {
  step: string;
  label: string;
  progress: number; // 0-1
  elapsed: number;  // ms
}

function setProgress(progress: ExtractionProgress | null): void {
  const progressBar = element.querySelector('.sr-panel__progress');
  if (!progress) {
    progressBar?.remove();
    return;
  }

  const label = progressBar?.querySelector('.sr-panel__progress-label');
  const time = progressBar?.querySelector('.sr-panel__progress-time');
  const fill = progressBar?.querySelector('.sr-panel__progress-fill') as HTMLElement;

  if (label) label.textContent = progress.label;
  if (time) time.textContent = `${(progress.elapsed / 1000).toFixed(1)}s`;
  if (fill) fill.style.width = `${progress.progress * 100}%`;
}
```

### Content Priming (Show Partial Data Early)

```typescript
// Show basic info immediately while full extraction happens
function primePanel(): void {
  if (!panel) return;

  // Get quick data from visible DOM
  const h1 = document.querySelector('h1');
  const name = h1?.textContent?.trim() || 'Loading...';

  const headlineEl = document.querySelector('.headline-class');
  const headline = headlineEl?.textContent?.trim();

  panel.setContent(`
    <div class="sr-panel__header">
      <span class="sr-panel__name">${name}</span>
    </div>
    <div class="sr-panel__body">
      ${headline ? `<div class="sr-panel__headline">${headline}</div>` : ''}
      <div class="sr-panel__loading">Analyzing profile...</div>
    </div>
  `);
}
```

### SPA URL Change Detection

Many modern sites are SPAs that don't trigger page loads. Detect navigation using multiple strategies:

```typescript
function observeUrlChanges(): void {
  let lastUrl = window.location.href;

  const checkUrlChange = () => {
    const currentUrl = window.location.href;
    if (currentUrl !== lastUrl) {
      const oldUrl = lastUrl;
      lastUrl = currentUrl;
      handleUrlChange(currentUrl, oldUrl);
    }
  };

  // Strategy 1: Intercept history.pushState and history.replaceState
  const originalPushState = history.pushState.bind(history);
  const originalReplaceState = history.replaceState.bind(history);

  history.pushState = function(...args) {
    originalPushState(...args);
    checkUrlChange();
  };

  history.replaceState = function(...args) {
    originalReplaceState(...args);
    checkUrlChange();
  };

  // Strategy 2: Listen to popstate event (back/forward navigation)
  window.addEventListener('popstate', checkUrlChange);

  // Strategy 3: MutationObserver as fallback
  const observer = new MutationObserver(checkUrlChange);
  observer.observe(document.body, { childList: true, subtree: true });
}

function handleUrlChange(newUrl: string, oldUrl: string): void {
  currentProfileId = null;

  if (isTargetPage(newUrl)) {
    // Switch to full mode
    panel?.setMinimalMode(false);
    primePanel();
    setTimeout(() => extractData(), 500);
  } else {
    // Switch to history mode
    panel?.setMinimalMode(true);
    loadHistory();
  }
}
```

### Background Script URL Notification (More Reliable)

```typescript
// background.ts - Notify content script of tab URL changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url) {
    chrome.tabs.sendMessage(tabId, {
      type: 'URL_CHANGED',
      url: changeInfo.url,
    }).catch(() => {}); // Ignore if no listener
  }
});

// content.ts - Listen for URL change messages
let lastHandledUrl = window.location.href;

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'URL_CHANGED' && message.url !== lastHandledUrl) {
    const oldUrl = lastHandledUrl;
    lastHandledUrl = message.url;
    handleUrlChange(message.url, oldUrl);
  }
});
```

### Modal/Popup Patterns

```typescript
function showPopup(content: string): void {
  // Remove existing
  document.querySelector('.my-extension-popup')?.remove();

  const popup = document.createElement('div');
  popup.className = 'my-extension-popup';
  popup.innerHTML = `
    <div class="popup-backdrop"></div>
    <div class="popup-content">
      <button class="popup-close">&times;</button>
      ${content}
    </div>
  `;

  document.body.appendChild(popup);

  // Animate in
  requestAnimationFrame(() => {
    popup.classList.add('popup--visible');
  });

  // Close handlers
  const closePopup = () => {
    popup.classList.remove('popup--visible');
    setTimeout(() => popup.remove(), 300);
  };

  popup.querySelector('.popup-backdrop')?.addEventListener('click', closePopup);
  popup.querySelector('.popup-close')?.addEventListener('click', closePopup);

  // Close on Escape
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      closePopup();
      document.removeEventListener('keydown', handleEscape);
    }
  };
  document.addEventListener('keydown', handleEscape);
}
```

---

## Sidepanel API

Use sidepanel instead of popup for persistent UI that stays open while user navigates.

### Opening Sidepanel with User Gesture

**Critical:** `chrome.sidePanel.open()` requires a user gesture. Open SYNCHRONOUSLY before any async operations:

```typescript
// Cache for synchronous access (async getPartyCode() won't work for user gesture)
let cachedPartyCode: string | null = null;

// Initialize cache on load
if (typeof chrome !== "undefined" && chrome.storage) {
  getPartyCode().then(code => { cachedPartyCode = code; });

  chrome.storage.onChanged.addListener((changes) => {
    if (changes.partyCode) {
      cachedPartyCode = changes.partyCode.newValue ?? null;
    }
  });
}

export async function handleIconClick(tab: chrome.tabs.Tab): Promise<void> {
  // Use CACHED value for synchronous check (preserves user gesture)
  const hasPartyCode = cachedPartyCode !== null;

  if (!hasPartyCode) {
    // Open sidepanel FIRST - must be synchronous with user gesture
    if (tab.windowId) {
      chrome.sidePanel.open({ windowId: tab.windowId }).catch(() => {});
    }

    // NOW do async operations
    await doAsyncWork();
    return;
  }

  // ... rest of logic
}
```

### Disabling Auto-Open Behavior

```typescript
// In your setup function (called from onInstalled)
await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: false });
```

---

## Storage Patterns

### Getter Functions with Defaults and Migration

**Never trust raw storage values.** Always use getter functions:

```typescript
const QUEUE_KEY = "pendingUrlQueue";

export interface QueuedPost {
  url: string;
  poster?: string;
  content?: string;
  platform: string;
}

export async function getQueue(): Promise<QueuedPost[]> {
  const result = await chrome.storage.local.get([QUEUE_KEY]);
  const queue = result[QUEUE_KEY] ?? [];

  // Handle migration from old format
  return queue.map((item: string | QueuedPost) => {
    if (typeof item === 'string') {
      return { url: item, platform: detectPlatform(item) };
    }
    return item;
  });
}

export async function addToQueue(post: QueuedPost): Promise<void> {
  const queue = await getQueue();

  // Prevent duplicates
  if (queue.some(p => p.url === post.url)) {
    return;
  }

  queue.push(post);

  // Enforce max size
  const MAX_SIZE = 9999;
  while (queue.length > MAX_SIZE) {
    queue.shift();
  }

  await chrome.storage.local.set({ [QUEUE_KEY]: queue });
}
```

### Storage Change Listeners

**Problem:** Raw `changes.newValue` can be undefined or in old format.

**Solution:** Always use getter function in listeners:

```typescript
// BAD - can be undefined or wrong format
chrome.storage.onChanged.addListener((changes) => {
  const queue = changes.pendingUrlQueue?.newValue || [];
  updateUI(queue);  // May crash or show wrong data
});

// GOOD - consistent data format
chrome.storage.onChanged.addListener((changes) => {
  if (changes.pendingUrlQueue) {
    debouncedRefresh();  // Will call getQueue() internally
  }
});
```

---

## Debouncing Concurrent Updates

**Problem:** Multiple event sources can fire simultaneously (storage listener + message handler).

**Solution:** Module-level debounce:

```typescript
let refreshTimeout: number | null = null;
let pendingFromClipboard = false;

export async function debouncedQueueRefresh(fromClipboard = false): Promise<void> {
  // Track metadata from any trigger
  if (fromClipboard) {
    pendingFromClipboard = true;
  }

  if (refreshTimeout) {
    clearTimeout(refreshTimeout);
  }

  refreshTimeout = window.setTimeout(async () => {
    const queue = await getQueue();
    updateQueueBanner(queue.length, queue, pendingFromClipboard);
    refreshTimeout = null;
    pendingFromClipboard = false;
  }, 50);  // 50ms debounce
}
```

---

## Message Passing

### Sidepanel Communication with Retry

Sidepanel may not be ready immediately after opening:

```typescript
async function sendToSidepanel(
  message: Record<string, unknown>,
  retries = 3
): Promise<void> {
  for (let i = 0; i < retries; i++) {
    try {
      await chrome.runtime.sendMessage(message);
      return;
    } catch {
      if (i < retries - 1) {
        await new Promise(resolve => setTimeout(resolve, 100 * (i + 1)));
      }
    }
  }
}

// Usage
await sendToSidepanel({ type: "refreshQueue", source: "feed" });
```

### Message Listener in Sidepanel

```typescript
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === "refreshQueue") {
    debouncedQueueRefresh(message.source === "clipboard");
  } else if (message.type === "showGuidance") {
    showGuidanceBubble(message.context);
  }
  // Must return true for async response
  return true;
});
```

---

## Context Menus

```typescript
export async function setupContextMenus(): Promise<void> {
  // Disable auto-open sidepanel - we handle it ourselves
  await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: false });

  await chrome.contextMenus.removeAll();

  chrome.contextMenus.create({
    id: "open-panel",
    title: "Open Extension Panel",
    contexts: ["action"],
  });

  chrome.contextMenus.create({
    id: "add-item",
    title: "Add Current Item",
    contexts: ["action"],
  });
}

// Event listener setup
chrome.contextMenus.onClicked.addListener(handleContextMenuClick);
chrome.runtime.onInstalled.addListener(setupContextMenus);
```

---

## Badge Management

```typescript
export async function updateBadge(count: number): Promise<void> {
  const text = count > 0 ? String(count) : "";
  await chrome.action.setBadgeText({ text });
  await chrome.action.setBadgeBackgroundColor({ color: "#0077b5" });
}

export async function updateNeedsPartyBadge(): Promise<void> {
  const count = await getQueueCount();
  if (count > 0) {
    await chrome.action.setBadgeText({ text: "!" });
    await chrome.action.setBadgeBackgroundColor({ color: "#ff6b35" });
  } else {
    await chrome.action.setBadgeText({ text: "" });
  }
}
```

---

## Notifications

```typescript
let notificationCounter = 0;

export async function showNotification(
  type: "success" | "error" | "info",
  title: string,
  message: string
): Promise<void> {
  const notificationId = `extension-${Date.now()}-${notificationCounter++}`;

  chrome.notifications.create(
    notificationId,
    {
      type: "basic",
      iconUrl: "icons/icon128.png",
      title,
      message,
    },
    () => {
      // Auto-clear after 5 seconds
      setTimeout(() => {
        chrome.notifications.clear(notificationId, () => {});
      }, 5000);
    }
  );
}
```

---

## Keyboard Shortcuts

```typescript
// In background.ts
chrome.commands.onCommand.addListener((command) => {
  if (command === "add-post") {
    handleKeyboardShortcut();
  }
});

export async function handleKeyboardShortcut(): Promise<void> {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const tab = tabs[0];
  if (tab) {
    await handleIconClick(tab);
  }
}
```

---

## Rate Limiting

```typescript
export class RateLimiter {
  private timestamps: number[] = [];
  private maxActions: number;
  private windowMs: number;

  constructor(maxActions: number, windowMs: number) {
    this.maxActions = maxActions;
    this.windowMs = windowMs;
  }

  private cleanOldTimestamps(): void {
    const now = Date.now();
    this.timestamps = this.timestamps.filter(ts => now - ts < this.windowMs);
  }

  canProceed(): boolean {
    this.cleanOldTimestamps();
    return this.timestamps.length < this.maxActions;
  }

  recordAction(): void {
    this.timestamps.push(Date.now());
  }

  getRemainingTime(): number {
    this.cleanOldTimestamps();
    if (this.timestamps.length < this.maxActions) return 0;
    return this.windowMs - (Date.now() - this.timestamps[0]);
  }

  reset(): void {
    this.timestamps = [];
  }
}

// Usage: 3 posts per minute
const postRateLimiter = new RateLimiter(3, 60000);

if (!postRateLimiter.canProceed()) {
  const remainingSec = Math.ceil(postRateLimiter.getRemainingTime() / 1000);
  return { success: false, message: `Please wait ${remainingSec}s` };
}
postRateLimiter.recordAction();
```

---

## Structured Logging

Create a consistent, filterable logging module:

```typescript
// logger.ts
export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

const PREFIX = '[MyExtension]';
let currentLevel: LogLevel = 'debug';

export function setLogLevel(level: LogLevel): void {
  currentLevel = level;
}

function shouldLog(level: LogLevel): boolean {
  return LOG_LEVELS[level] >= LOG_LEVELS[currentLevel];
}

function log(level: LogLevel, ...args: unknown[]): void {
  if (!shouldLog(level)) return;

  const consoleFn = level === 'debug' ? console.debug
    : level === 'info' ? console.log
    : level === 'warn' ? console.warn
    : console.error;

  consoleFn(PREFIX, ...args);
}

export const logger = {
  debug: (...args: unknown[]) => log('debug', ...args),
  info: (...args: unknown[]) => log('info', ...args),
  warn: (...args: unknown[]) => log('warn', ...args),
  error: (...args: unknown[]) => log('error', ...args),

  // Create module-specific logger
  forModule(module: string) {
    const modulePrefix = `[${module}]`;
    return {
      debug: (...args: unknown[]) => log('debug', modulePrefix, ...args),
      info: (...args: unknown[]) => log('info', modulePrefix, ...args),
      warn: (...args: unknown[]) => log('warn', modulePrefix, ...args),
      error: (...args: unknown[]) => log('error', modulePrefix, ...args),
    };
  },
};

// Usage
import { logger } from './logger';
logger.debug('User clicked button', { userId: 123 });

const panelLogger = logger.forModule('Panel');
panelLogger.info('Panel opened');
```

**Benefits:**
- Filterable in Chrome DevTools by prefix
- Easily toggle verbosity in production
- Module-specific prefixes for debugging

---

## Extension Context Validation

Chrome extension context can become invalid during SPA navigation or page reloads:

```typescript
function isExtensionContextValid(): boolean {
  try {
    return chrome?.runtime?.id !== undefined;
  } catch {
    return false;
  }
}

async function safeStorageGet<T>(key: string): Promise<T | null> {
  if (!isExtensionContextValid()) {
    console.debug('Extension context invalidated');
    return null;
  }

  return new Promise((resolve) => {
    try {
      chrome.storage.local.get([key], (result) => {
        if (chrome.runtime.lastError) {
          console.debug('Storage error:', chrome.runtime.lastError);
          resolve(null);
          return;
        }
        resolve(result[key] || null);
      });
    } catch (e) {
      console.debug('Storage exception:', e);
      resolve(null);
    }
  });
}
```

**When context becomes invalid:**
- SPA navigation (history.pushState)
- Extension reload/update
- Page refresh during content script execution
- Service worker termination

---

## Executing Scripts in Tabs

```typescript
// Extract data from page
export async function getPageContent(tabId: number): Promise<string> {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => document.body.innerText,
  });
  return results[0]?.result ?? "";
}

// Execute function with arguments
export async function detectPostFromFeed(tabId: number): Promise<{
  url: string | null;
  extractedPost: ExtractedPost | null;
}> {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: detectPostInPage,  // Function defined elsewhere
  });
  return results[0]?.result ?? { url: null, extractedPost: null };
}
```

---

## Testing with Vitest

### Mock Chrome APIs

```typescript
// test-setup.ts
import { vi } from 'vitest';

const mockChrome = {
  storage: {
    local: {
      get: vi.fn().mockResolvedValue({}),
      set: vi.fn().mockResolvedValue(undefined),
      remove: vi.fn().mockResolvedValue(undefined),
    },
    onChanged: {
      addListener: vi.fn(),
    },
  },
  runtime: {
    sendMessage: vi.fn().mockResolvedValue(undefined),
    onMessage: { addListener: vi.fn() },
    onInstalled: { addListener: vi.fn() },
  },
  action: {
    onClicked: { addListener: vi.fn() },
    setBadgeText: vi.fn().mockResolvedValue(undefined),
    setBadgeBackgroundColor: vi.fn().mockResolvedValue(undefined),
  },
  sidePanel: {
    open: vi.fn().mockResolvedValue(undefined),
    setPanelBehavior: vi.fn().mockResolvedValue(undefined),
  },
  contextMenus: {
    onClicked: { addListener: vi.fn() },
    removeAll: vi.fn().mockResolvedValue(undefined),
    create: vi.fn(),
  },
  tabs: {
    query: vi.fn().mockResolvedValue([]),
    get: vi.fn().mockResolvedValue({}),
  },
  scripting: {
    executeScript: vi.fn().mockResolvedValue([]),
  },
  notifications: {
    create: vi.fn(),
    clear: vi.fn(),
  },
  commands: {
    onCommand: { addListener: vi.fn() },
  },
};

// @ts-expect-error - mock chrome global
globalThis.chrome = mockChrome;

export { mockChrome };
```

### Vitest Configuration

```typescript
// vite.config.ts
export default defineConfig({
  test: {
    environment: "jsdom",
    exclude: ["**/node_modules/**", "**/e2e/**"],
    setupFiles: ["./src/test-setup.ts"],
  },
});
```

### Example Test

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mockChrome } from './test-setup';
import { getQueue, addToQueue } from './storage';

describe('storage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns empty array when no queue exists', async () => {
    mockChrome.storage.local.get.mockResolvedValue({});
    const queue = await getQueue();
    expect(queue).toEqual([]);
  });

  it('migrates old string format to QueuedPost', async () => {
    mockChrome.storage.local.get.mockResolvedValue({
      pendingUrlQueue: ['https://linkedin.com/posts/123']
    });
    const queue = await getQueue();
    expect(queue[0]).toHaveProperty('url');
    expect(queue[0]).toHaveProperty('platform');
  });

  it('prevents duplicate URLs', async () => {
    mockChrome.storage.local.get.mockResolvedValue({
      pendingUrlQueue: [{ url: 'https://example.com', platform: 'test' }]
    });

    await addToQueue({ url: 'https://example.com', platform: 'test' });

    // Should not call set because URL is duplicate
    expect(mockChrome.storage.local.set).not.toHaveBeenCalled();
  });
});
```

### Testing Async UI Functions

When testing functions that depend on storage, make them async and await in tests:

```typescript
// Function must be async
export async function showGuidanceBubble(context: "notAPost"): Promise<void> {
  const queueCount = await getQueueCount();
  if (queueCount > 0) {
    return;  // Don't show guidance if queue has items
  }
  // ... show guidance
}

// Test must await
it('does not show guidance when queue has posts', async () => {
  mockChrome.storage.local.get.mockResolvedValue({
    pendingUrlQueue: [{ url: 'https://example.com', platform: 'test' }]
  });

  await showGuidanceBubble('notAPost');

  expect(bubble?.style.display).not.toBe('block');
});
```

---

## E2E Testing with Playwright

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';
import path from 'path';

const extensionPath = path.resolve(__dirname, 'dist');

export default defineConfig({
  testDir: './tests',
  timeout: 120000,  // 2 min for complex pages
  retries: 0,
  workers: 1,  // Extensions require single worker

  use: {
    headless: false,  // Extensions require headed mode
    viewport: { width: 1280, height: 720 },
    actionTimeout: 10000,
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/,
    },
    {
      name: 'extension-tests',
      testMatch: /.*\.spec\.ts/,
      dependencies: ['setup'],
    },
  ],
});
```

### Test Fixtures with Extension

```typescript
// tests/fixtures.ts
import { test as base, chromium, BrowserContext } from '@playwright/test';
import path from 'path';

const extensionPath = path.resolve(__dirname, '../dist');
const userDataDir = path.resolve(__dirname, '../.auth/user-data');

export const test = base.extend<{
  context: BrowserContext;
  extensionId: string;
}>({
  context: async ({}, use) => {
    const context = await chromium.launchPersistentContext(userDataDir, {
      headless: false,
      args: [
        `--disable-extensions-except=${extensionPath}`,
        `--load-extension=${extensionPath}`,
        '--no-first-run',
        '--disable-blink-features=AutomationControlled',
      ],
      viewport: { width: 1280, height: 720 },
    });

    await use(context);
    await context.close();
  },

  extensionId: async ({ context }, use) => {
    // Get extension ID from service worker
    let extensionId = '';
    const serviceWorkers = context.serviceWorkers();

    if (serviceWorkers.length > 0) {
      const url = serviceWorkers[0].url();
      const match = url.match(/chrome-extension:\/\/([^/]+)/);
      if (match) extensionId = match[1];
    }

    await use(extensionId);
  },
});

export { expect } from '@playwright/test';
```

### Auth Setup (Manual Login)

```typescript
// tests/auth.setup.ts
import { test as setup, chromium } from '@playwright/test';
import path from 'path';
import fs from 'fs';

const authFile = path.resolve(__dirname, '../.auth/session.json');
const userDataDir = path.resolve(__dirname, '../.auth/user-data');
const extensionPath = path.resolve(__dirname, '../dist');

setup('authenticate', async () => {
  // Check if already authenticated (less than 24h old)
  if (fs.existsSync(authFile)) {
    const stats = fs.statSync(authFile);
    const ageHours = (Date.now() - stats.mtimeMs) / (1000 * 60 * 60);
    if (ageHours < 24) {
      console.log('Using existing auth');
      return;
    }
  }

  // Launch with extension for manual login
  const context = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    args: [
      `--disable-extensions-except=${extensionPath}`,
      `--load-extension=${extensionPath}`,
      '--no-first-run',
    ],
  });

  const page = await context.newPage();
  await page.goto('https://example.com/login');

  // Wait for user to complete login (5 min timeout)
  await page.waitForURL('**/dashboard/**', { timeout: 300000 });

  // Save session
  await context.storageState({ path: authFile });
  await context.close();
});
```

### Example E2E Test

```typescript
// tests/profile.spec.ts
import { test, expect } from './fixtures';

test('extracts profile data', async ({ context }) => {
  const page = await context.newPage();

  await page.goto('https://example.com/profile/user123');

  // Wait for extension UI to appear
  await page.waitForSelector('#my-extension-panel', { timeout: 10000 });

  // Verify extraction
  const name = await page.locator('#my-extension-panel .name').textContent();
  expect(name).toBeTruthy();
});
```

**Key Points:**
- Extensions require `headless: false`
- Use `launchPersistentContext` to preserve auth
- Add `--disable-blink-features=AutomationControlled` to avoid detection
- Single worker (`workers: 1`) for extension testing

---

## Common Pitfalls

1. **Losing user gesture** - `sidePanel.open()` must be called synchronously with click, not after await
2. **Trusting raw storage values** - Always use getter functions with defaults and migration
3. **Race conditions** - Multiple event sources (storage + messages) need debouncing
4. **Forgetting to rebuild** - TypeScript changes require `npm run build`
5. **Sidepanel not ready** - Use retry pattern when sending messages after open
6. **Context invalidation** - Check `chrome.runtime.id` before API calls
7. **Service worker termination** - Don't rely on in-memory state; use storage

---

## Preserving UI State

**Problem:** Temporary messages (like "No post detected") can overwrite important UI (like queue display).

**Solution:** Check existing state before showing temporary content:

```typescript
export async function showGuidanceBubble(context: "notAPost"): Promise<void> {
  // Don't overwrite queue display
  const queueCount = await getQueueCount();
  if (queueCount > 0) {
    return;
  }
  // ... show guidance
}
```

---

## Quick Reference

```typescript
// Open sidepanel (SYNC with user gesture)
chrome.sidePanel.open({ windowId: tab.windowId });

// Storage with defaults
const result = await chrome.storage.local.get([KEY]);
return result[KEY] ?? defaultValue;

// Message with retry
for (let i = 0; i < 3; i++) {
  try { await chrome.runtime.sendMessage(msg); return; }
  catch { await sleep(100 * (i + 1)); }
}

// Execute in tab
const results = await chrome.scripting.executeScript({
  target: { tabId },
  func: () => document.body.innerText,
});

// Badge
await chrome.action.setBadgeText({ text: "!" });
await chrome.action.setBadgeBackgroundColor({ color: "#ff6b35" });
```
