---
name: addfox-testing
description: >-
  Test Addfox browser extensions. Rstest (Rsbuild testing) for unit and component tests with jsdom/happy-dom;
  mock chrome.* / browser.* APIs; Playwright E2E with chromium.launchPersistentContext, --load-extension pointing
  at .addfox/extension, extension fixtures, popup chrome-extension:// URLs, CI scripts (addfox build && playwright test).
metadata:
  tags: addfox, testing, rstest, playwright, e2e, unit-test, jsdom, mock-chrome, browser-extension, webextension
---

## When to use

Use this skill when the user or codebase needs **automated tests** for an Addfox extension: `rstest`, `*.test.ts` / `*.spec.ts`, `playwright.config.ts`, `e2e/` folder, mocking `chrome.storage` / `runtime.sendMessage`, or loading the unpacked build from `.addfox/extension` in a real browser.

Trigger examples:

- "给扩展加单元测试 / E2E / Playwright"
- "mock chrome API", "rstest.config", "测试 background 消息"
- "CI 里跑扩展测试", "coverage", "extension fixture"
- Choosing **unit vs E2E** for popup, content script, or content UI

Use **addfox-best-practices** for product architecture; use **addfox-debugging** if tests fail due to build or load errors.

## How to use

Follow sections below for Rstest setup, chrome mocks, and Playwright extension loading. Supplementary notes: [reference.md](reference.md).

---

# Addfox Testing

Use **Rstest** for unit tests and **Playwright** for E2E extension loading.

---

## 1. Test Types Overview

| Test Type | Tool | Use Case | Speed |
|-----------|------|----------|-------|
| Unit | Rstest | Logic, utilities, storage, messaging | Fast (<1s) |
| Component | Rstest + jsdom | React/Vue/Svelte components | Medium (~1s) |
| E2E | Playwright | Full extension load, user flows | Slow (~10s) |

### Decision Matrix

| Feature to Test | Recommended Type | Notes |
|-----------------|------------------|-------|
| Background message handlers | Unit | Mock `chrome.runtime` |
| Storage operations | Unit | Mock `chrome.storage` |
| Content script selectors | Unit | Use jsdom |
| React component rendering | Component | Use testing-library |
| Popup interactions | E2E | Full browser context |
| Cross-extension messaging | E2E | Real extension instances |
| Content UI appearance | E2E | Visual verification |
| Permission flows | E2E | Real browser prompts |

---

## 2. Unit Testing with Rstest

### 2.1 Installation

Rstest is pre-configured in Addfox. Install additional dependencies:

```bash
# Rstest is included with Addfox
pnpm add -D @testing-library/react @testing-library/jest-dom jsdom

# For Vue
pnpm add -D @vue/test-utils

# For utilities
pnpm add -D happy-dom  # Alternative to jsdom, faster
```

### 2.2 Configuration

Add to project root (if not present):

```ts
// rstest.config.ts
import { defineConfig } from 'rstest';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom', // or 'happy-dom', 'node'
    setupFiles: ['./test/setup.ts'],
    include: ['**/*.test.ts', '**/*.spec.ts'],
    exclude: ['**/node_modules/**', '**/e2e/**']
  }
});
```

### 2.3 Mocking Extension APIs

Create mock for `chrome.*` APIs:

```ts
// test/mocks/chrome.ts
export const mockChrome = {
  runtime: {
    sendMessage: vi.fn(),
    onMessage: {
      addListener: vi.fn(),
      removeListener: vi.fn()
    },
    getManifest: vi.fn(() => ({
      manifest_version: 3,
      version: '1.0.0'
    }))
  },
  storage: {
    local: {
      get: vi.fn(),
      set: vi.fn()
    },
    sync: {
      get: vi.fn(),
      set: vi.fn()
    }
  },
  tabs: {
    query: vi.fn(),
    sendMessage: vi.fn(),
    create: vi.fn()
  },
  scripting: {
    executeScript: vi.fn()
  }
};

// test/setup.ts
import { mockChrome } from './mocks/chrome';

global.chrome = mockChrome as any;
```

### 2.4 Unit Test Examples

**Background logic:**
```ts
// src/utils/storage.test.ts
import { describe, it, expect, vi, beforeEach } from 'rstest';
import { saveSettings, getSettings } from './storage';

describe('storage', () => {
  beforeEach(() => {
    vi.resetAllMocks();
    chrome.storage.sync.get = vi.fn().mockResolvedValue({});
    chrome.storage.sync.set = vi.fn().mockResolvedValue(undefined);
  });

  it('saves settings to sync storage', async () => {
    const settings = { theme: 'dark', autoSave: true };
    await saveSettings(settings);
    
    expect(chrome.storage.sync.set).toHaveBeenCalledWith(settings);
  });

  it('retrieves settings with defaults', async () => {
    chrome.storage.sync.get = vi.fn().mockResolvedValue({ theme: 'light' });
    
    const result = await getSettings();
    
    expect(chrome.storage.sync.get).toHaveBeenCalled();
    expect(result.theme).toBe('light');
  });
});
```

**Message handlers:**
```ts
// src/background/messages.test.ts
import { describe, it, expect, vi } from 'rstest';
import { handleMessage } from './messages';

describe('message handlers', () => {
  it('handles GET_SETTINGS from popup', async () => {
    const message = { from: 'popup', action: 'GET_SETTINGS' };
    const sender = { tab: { id: 123 } };
    
    const response = await handleMessage(message, sender);
    
    expect(response).toHaveProperty('settings');
  });

  it('rejects unknown actions', async () => {
    const message = { from: 'content', action: 'UNKNOWN' };
    
    await expect(handleMessage(message, {}))
      .rejects.toThrow('Unknown action');
  });
});
```

**Content script utilities:**
```ts
// src/content/utils.test.ts
import { describe, it, expect } from 'rstest';
import { extractVideoInfo } from './utils';

// Mock document for content script tests
const mockDocument = `
  <video src="https://example.com/video.mp4" data-title="Test Video"></video>
`;

describe('extractVideoInfo', () => {
  it('extracts video URL from page', () => {
    document.body.innerHTML = mockDocument;
    
    const info = extractVideoInfo();
    
    expect(info.url).toBe('https://example.com/video.mp4');
    expect(info.title).toBe('Test Video');
  });

  it('returns null when no video found', () => {
    document.body.innerHTML = '<div>No video here</div>';
    
    const info = extractVideoInfo();
    
    expect(info).toBeNull();
  });
});
```

### 2.5 Component Testing

**React component:**
```tsx
// src/components/Button.test.tsx
import { describe, it, expect, vi } from 'rstest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    
    fireEvent.click(screen.getByText('Click'));
    
    expect(handleClick).toHaveBeenCalled();
  });
});
```

---

## 3. E2E Testing with Playwright

### 3.1 Installation

```bash
pnpm add -D @playwright/test
npx playwright install chromium firefox
```

### 3.2 E2E Configuration

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false, // Extensions should run sequentially
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1, // Single worker for extension tests
  reporter: 'list',
  use: {
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    // Firefox requires signed extensions for E2E
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] }
    // }
  ]
});
```

### 3.3 Extension Fixture

```ts
// e2e/fixtures.ts
import { test as base, chromium, type BrowserContext } from '@playwright/test';
import path from 'path';

export const test = base.extend<{
  context: BrowserContext;
  extensionId: string;
}>({
  context: async ({}, use) => {
    // Build extension first
    const extensionPath = path.join(__dirname, '../.addfox/extension');
    
    const context = await chromium.launchPersistentContext('', {
      headless: false,
      args: [
        `--disable-extensions-except=${extensionPath}`,
        `--load-extension=${extensionPath}`
      ]
    });
    
    await use(context);
    await context.close();
  },
  
  extensionId: async ({ context }, use) => {
    // Get extension ID from background page
    let [background] = context.backgroundPages();
    if (!background) {
      background = await context.waitForEvent('backgroundpage');
    }
    
    const extensionId = background.url().split('/')[2];
    await use(extensionId);
  }
});

export const expect = test.expect;
```

### 3.4 E2E Test Examples

**Extension load:**
```ts
// e2e/extension-load.test.ts
import { test, expect } from './fixtures';

test('extension loads without errors', async ({ context }) => {
  const page = await context.newPage();
  
  // Check console for errors
  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  
  await page.goto('https://example.com');
  await page.waitForTimeout(1000); // Allow extension to initialize
  
  expect(errors).toHaveLength(0);
});
```

**Popup interaction:**
```ts
// e2e/popup.test.ts
import { test, expect } from './fixtures';

test('popup opens and shows content', async ({ context, extensionId }) => {
  const page = await context.newPage();
  await page.goto(`chrome-extension://${extensionId}/popup/index.html`);
  
  // Verify popup rendered
  await expect(page.locator('body')).toContainText('My Extension');
  
  // Test interaction
  await page.click('button[data-testid="settings"]');
  await expect(page.locator('.settings-panel')).toBeVisible();
});
```

**Content script injection:**
```ts
// e2e/content-script.test.ts
import { test, expect } from './fixtures';

test('content script injects on matching page', async ({ context }) => {
  const page = await context.newPage();
  
  // Navigate to page matching content_scripts.matches
  await page.goto('https://example.com');
  
  // Wait for content script to inject
  await page.waitForSelector('[data-extension-root]', { timeout: 5000 });
  
  // Verify content UI exists
  const root = page.locator('[data-extension-root]');
  await expect(root).toBeVisible();
});
```

**Background script:**
```ts
// e2e/background.test.ts
import { test, expect } from './fixtures';

test('background script responds to messages', async ({ context }) => {
  const page = await context.newPage();
  await page.goto('https://example.com');
  
  // Send message from page to background via content script
  const response = await page.evaluate(async () => {
    return await chrome.runtime.sendMessage({
      from: 'test',
      action: 'PING'
    });
  });
  
  expect(response).toEqual({ status: 'pong' });
});
```

### 3.5 E2E Best Practices

| Practice | Why |
|----------|-----|
| Build before E2E | `addfox build` must run before Playwright tests |
| Use `test.extend` | Create reusable fixtures for extension context |
| Single worker | Extension tests conflict with parallel runs |
| Headless off | Some extension APIs require headed browser |
| Cleanup context | Always close browser context after tests |

---

## 4. Test Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "test": "rstest",
    "test:unit": "rstest --run",
    "test:e2e": "addfox build && playwright test",
    "test:e2e:ui": "addfox build && playwright test --ui",
    "test:coverage": "rstest --coverage"
  }
}
```

---

## 5. Testing Checklist

### Unit Tests
- [ ] Mock `chrome.*` APIs in setup file
- [ ] Test background message handlers
- [ ] Test storage operations with mocked storage
- [ ] Test content script utilities in jsdom
- [ ] Test components with testing-library

### E2E Tests
- [ ] Build extension before running Playwright
- [ ] Create fixture for extension context
- [ ] Test extension loads without console errors
- [ ] Test popup/options page rendering
- [ ] Test content script injection on matching pages
- [ ] Test background script message handling

### Configuration
- [ ] `rstest.config.ts` with appropriate environment
- [ ] `playwright.config.ts` with extension args
- [ ] Test mocks for all used `chrome.*` APIs
- [ ] CI workflow for automated testing

---

## Additional resources

- Rstest: [Rsbuild Testing](https://rsbuild.dev/guide/testing)
- Playwright: [Extension Testing Guide](https://playwright.dev/docs/chrome-extensions)
- Testing Library: [DOM Testing](https://testing-library.com/docs/dom-testing-library/intro/)
- Example E2E patterns: [Playwright Extension Examples](https://github.com/microsoft/playwright/tree/main/tests/electron)
