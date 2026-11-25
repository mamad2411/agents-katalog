---
name: browser-automation
description: Use when automating browsers with Playwright/Puppeteer, testing Chrome extensions, using Chrome DevTools Protocol (CDP), handling dynamic content/SPAs, or debugging automation issues
---

# Browser Automation

## When to Use This Skill

- Setting up browser automation (Playwright, Puppeteer, Selenium)
- Testing Chrome extensions (Manifest V3)
- Cloud browser testing (LambdaTest, BrowserStack)
- Using Chrome DevTools Protocol (CDP)
- Handling dynamic/lazy-loaded content
- Debugging automation issues

## Tool Selection

### Playwright (Recommended)

```bash
npm install -D @playwright/test
```

**Pros:**
- Multi-browser support (Chrome, Firefox, Safari, Edge)
- Built-in test runner with great DX
- Auto-wait mechanisms reduce flakiness
- Excellent debugging tools (trace viewer, inspector)
- Strong TypeScript support

**Use when:**
- Cross-browser testing needed
- Writing end-to-end tests
- TypeScript project

---

### Puppeteer

```bash
npm install puppeteer
```

**Pros:**
- Simpler API, easier to learn
- Smaller footprint
- Direct Chrome/Chromium control
- Official Chrome team project

**Use when:**
- Only need Chrome
- Simple automation tasks
- Quick scripts/prototypes

---

### Selenium

```bash
npm install selenium-webdriver
```

**Use when:**
- Legacy projects already using it
- Multi-language team
- Need specific Selenium features

---

### AI-Powered Automation

**Stagehand**
```bash
npm install @anthropic-ai/stagehand
```

AI agent that automates web tasks using Claude + CDP.

**Use when:**
- Complex multi-step web workflows
- Dynamic/changing UIs
- Natural language task descriptions
- Have budget for LLM API calls

**Not suitable for:**
- Chrome extension testing
- Simple, predictable automation
- Cost-sensitive projects

---

**Browser-Use**
```bash
pip install browser-use
```

Python library for LLM-controlled browser automation.

**Use when:**
- Python-based projects
- Need AI to navigate/interact with sites
- Exploratory automation

---

**Skyvern**

Vision-based web automation using computer vision + LLMs.

**Use when:**
- Sites with no accessible DOM selectors
- Need to handle CAPTCHAs/complex visuals
- Budget for vision API calls

---

## Chrome Extension Testing

### Local Testing (Recommended)

**For Manifest V3 Extensions:**

```javascript
// playwright.config.ts
export default defineConfig({
  use: {
    headless: false,
    args: [
      `--disable-extensions-except=${extensionPath}`,
      `--load-extension=${extensionPath}`,
    ],
  },
})
```

**Find extension ID via CDP:**

```typescript
const client = await context.newCDPSession(page)
const { targetInfos } = await client.send('Target.getTargets')

const extensionTarget = targetInfos.find((target: any) =>
  target.type === 'service_worker' &&
  target.url.startsWith('chrome-extension://')
)

const extensionId = extensionTarget.url.match(/chrome-extension:\/\/([^\/]+)/)?.[1]
```

**Navigate to extension pages:**

```typescript
await page.goto(`chrome-extension://${extensionId}/popup.html`)
await page.goto(`chrome-extension://${extensionId}/options.html`)
await page.goto(`chrome-extension://${extensionId}/sidepanel.html`)
```

---

### Cloud Testing Limitations

**What works:**
- Extension uploads to LambdaTest/BrowserStack
- Extensions load in cloud browsers
- Service workers run
- Can test content scripts on regular sites

**What doesn't work:**
- Cannot navigate to `chrome-extension://` URLs
- All attempts blocked with `net::ERR_BLOCKED_BY_CLIENT`

**Why:** Cloud platforms block extension URLs for security in shared environments.

**Verdict:** Use local testing for extension UI testing. Cloud for content script testing only.

---

## Chrome DevTools Protocol (CDP)

### Get All Browser Targets

```typescript
const client = await context.newCDPSession(page)
const { targetInfos } = await client.send('Target.getTargets')

const extensions = targetInfos.filter(t => t.type === 'service_worker')
const pages = targetInfos.filter(t => t.type === 'page')
const workers = targetInfos.filter(t => t.type === 'worker')
```

### Execute Code in Extension Context

```typescript
// Attach to extension service worker
const swTarget = await client.send('Target.attachToTarget', {
  targetId: extensionTarget.targetId,
  flatten: true,
})

// Execute in service worker context
await client.send('Runtime.evaluate', {
  expression: `
    chrome.storage.local.get(['key']).then(console.log)
  `,
  awaitPromise: true,
})
```

### Intercept Network Requests

```typescript
await client.send('Network.enable')
await client.send('Network.setRequestInterception', {
  patterns: [{ urlPattern: '*' }],
})

client.on('Network.requestIntercepted', async (event) => {
  await client.send('Network.continueInterceptedRequest', {
    interceptionId: event.interceptionId,
    headers: { ...event.request.headers, 'X-Custom': 'value' },
  })
})
```

### Get Console Messages

```typescript
await client.send('Runtime.enable')
await client.send('Log.enable')

client.on('Runtime.consoleAPICalled', (event) => {
  console.log('Console:', event.args.map(a => a.value))
})

client.on('Runtime.exceptionThrown', (event) => {
  console.error('Exception:', event.exceptionDetails)
})
```

---

## Handling Dynamic Content

### Wait Strategies

```typescript
// Wait for specific content
await page.waitForSelector('.product-price', { timeout: 10000 })

// Wait for network to be idle
await page.goto(url, { waitUntil: 'networkidle' })

// Wait for custom condition
await page.waitForFunction(() => {
  return document.querySelectorAll('.item').length > 10
})
```

### Time-Based vs Scroll-Based Lazy Loading

**Key insight:** Some sites load content based on **time elapsed**, not scroll position.

**Testing approach:**
```javascript
// Test 1: Wait with no scroll
await page.goto(url)
await page.waitForTimeout(3000)
const sectionsNoScroll = await page.$$('.section').length

// Test 2: Scroll immediately
await page.goto(url)
await page.evaluate(() => window.scrollTo(0, 5000))
await page.waitForTimeout(500)
const sectionsWithScroll = await page.$$('.section').length

// If same result: site uses time-based loading
// No scroll automation needed - just wait
```

**Benefits of detecting time-based loading:**
- Simpler automation code
- No visual disruption
- More reliable extraction

---

### Handling Lazy-Loaded Images

```javascript
// Force lazy images to load
await page.evaluate(() => {
  // Handle data-src → src pattern
  document.querySelectorAll('[data-src]').forEach(el => {
    if (!el.src) el.src = el.dataset.src
  })

  // Handle loading="lazy" attribute
  document.querySelectorAll('[loading="lazy"]').forEach(el => {
    el.loading = 'eager'
  })
})
```

---

## Advanced Lazy Loading Techniques

### Googlebot-Style Tall Viewport

**Key insight:** Googlebot doesn't scroll - it uses a 12,140px viewport and manipulates IntersectionObserver.

```javascript
// Temporarily expand document for IntersectionObserver
async function triggerLazyLoadViaViewport() {
  const originalHeight = document.documentElement.style.height;
  const originalOverflow = document.documentElement.style.overflow;

  // Googlebot uses 12,140px mobile / 9,307px desktop
  document.documentElement.style.height = '20000px';
  document.documentElement.style.overflow = 'visible';

  // Wait for observers to trigger
  await new Promise(r => setTimeout(r, 500));

  // Restore
  document.documentElement.style.height = originalHeight;
  document.documentElement.style.overflow = originalOverflow;
}
```

**Pros:** No visible scrolling, works with standard IntersectionObserver
**Cons:** Won't work with scroll-event listeners or virtualized lists

---

### IntersectionObserver Override

Patch IntersectionObserver before page loads to force everything to "intersect":

```javascript
// Must inject at document_start (before page JS runs)
const script = document.createElement('script');
script.textContent = `
  const OriginalIO = window.IntersectionObserver;
  window.IntersectionObserver = function(callback, options) {
    // Override rootMargin to include everything off-screen
    const modifiedOptions = {
      ...options,
      rootMargin: '10000px 10000px 10000px 10000px'
    };
    return new OriginalIO(callback, modifiedOptions);
  };
  window.IntersectionObserver.prototype = OriginalIO.prototype;
`;
document.documentElement.prepend(script);
```

**Pros:** Elegant, works at the source, no DOM manipulation
**Cons:** Must inject before page JS runs, may break other functionality

---

### Direct Attribute Manipulation

Force lazy elements to load by modifying their attributes:

```javascript
function forceLoadLazyContent() {
  // Handle data-src → src pattern
  document.querySelectorAll('[data-src]').forEach(el => {
    if (!el.src) el.src = el.dataset.src;
  });

  document.querySelectorAll('[data-srcset]').forEach(el => {
    if (!el.srcset) el.srcset = el.dataset.srcset;
  });

  // Handle background images
  document.querySelectorAll('[data-background]').forEach(el => {
    el.style.backgroundImage = `url(${el.dataset.background})`;
  });

  // Trigger lazysizes library if present
  if (window.lazySizes) {
    document.querySelectorAll('.lazyload').forEach(el => {
      window.lazySizes.loader.unveil(el);
    });
  }
}
```

---

### MutationObserver for Progressive Extraction

Watch for DOM changes and extract content as it loads:

```javascript
function setupProgressiveExtraction(onNewContent) {
  let debounceTimer = null;

  const observer = new MutationObserver((mutations) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const addedNodes = mutations
        .flatMap(m => Array.from(m.addedNodes))
        .filter(n => n.nodeType === Node.ELEMENT_NODE);

      if (addedNodes.length > 0) {
        onNewContent(addedNodes);
      }
    }, 300);
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  return () => observer.disconnect();
}
```

---

### Lazy Loading Decision Matrix

| Approach | Scrolling? | Reliability | Complexity |
|----------|------------|-------------|------------|
| Tall Viewport | No | Medium | Low |
| IO Override | No | Medium | Medium |
| Attribute Manipulation | No | Low | Low |
| MutationObserver | User-initiated | High | Low |

**Recommendation:** Start with **IO Override + Tall Viewport** for most cases. Use **MutationObserver** when user scrolling is acceptable.

---

### Vanity URLs vs Internal IDs

**Problem:** Some sites use vanity URLs that differ from internal identifiers.

```
URL: /user/john-smith
Internal ID: john-smith-a2b3c4d5
```

**Solution:** Match by displayed content, not URL:

```javascript
// Strategy 1: Try URL-based ID
const urlId = location.pathname.split('/').pop()
let profile = findById(urlId)

// Strategy 2: Fall back to displayed name
if (!profile) {
  const displayedName = document.querySelector('h1')?.textContent?.trim()
  profile = findByName(displayedName)
}
```

---

## Cloud Browser Integration

### LambdaTest Setup

```typescript
// playwright.lambdatest.config.ts
const capabilities = {
  'LT:Options': {
    'username': process.env.LT_USERNAME,
    'accessKey': process.env.LT_ACCESS_KEY,
    'platformName': 'Windows 10',
    'browserName': 'Chrome',
    'browserVersion': 'latest',
  }
}

export default defineConfig({
  projects: [{
    name: 'lambdatest',
    use: {
      connectOptions: {
        wsEndpoint: `wss://cdp.lambdatest.com/playwright?capabilities=${encodeURIComponent(JSON.stringify(capabilities))}`,
      },
    },
  }],
})
```

---

## Performance Optimization

### Block Unnecessary Resources

```typescript
await page.route('**/*', route => {
  const type = route.request().resourceType()
  if (['image', 'font', 'media'].includes(type)) {
    route.abort()
  } else {
    route.continue()
  }
})
```

### Reuse Browser Context

```typescript
// Good: Reuse browser, create new contexts
const browser = await chromium.launch()
for (const url of urls) {
  const context = await browser.newContext()
  const page = await context.newPage()
  // ...
  await context.close()
}
await browser.close()
```

### Parallel Execution

```typescript
import pLimit from 'p-limit'
const limit = pLimit(5) // Max 5 concurrent

await Promise.all(
  urls.map(url => limit(() => processUrl(url)))
)
```

---

## Debugging

### Visual Debugging

```typescript
// Screenshots
await page.screenshot({ path: 'debug.png' })

// Video recording
const context = await browser.newContext({
  recordVideo: { dir: 'videos/' }
})
```

### Trace Viewer

```typescript
await context.tracing.start({ screenshots: true, snapshots: true })
// ... run test
await context.tracing.stop({ path: 'trace.zip' })

// View: npx playwright show-trace trace.zip
```

### Slow Motion & Pause

```typescript
const browser = await chromium.launch({
  headless: false,
  slowMo: 1000,
})

await page.pause() // Opens Playwright Inspector
```

---

## Quick Reference

### Common Selectors

```typescript
// CSS
await page.locator('.class')
await page.locator('#id')
await page.locator('[data-testid="value"]')

// Text
await page.locator('text="Exact text"')

// Playwright-specific
await page.getByRole('button', { name: 'Submit' })
await page.getByText('Welcome')
await page.getByLabel('Email')
```

### Data Extraction

```typescript
// Single element
const text = await page.textContent('.element')
const attr = await page.getAttribute('.element', 'href')

// Multiple elements
const texts = await page.$$eval('.item', els => els.map(e => e.textContent))

// Complex extraction
const data = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.product')).map(el => ({
    title: el.querySelector('.title')?.textContent,
    price: el.querySelector('.price')?.textContent,
  }))
})
```

---

## Common Issues

### Element Not Found

```typescript
// Wait for element
await page.waitForSelector('.element', { state: 'visible' })

// Check if in iframe
const frame = page.frame({ url: /example\.com/ })
if (frame) {
  await frame.waitForSelector('.element')
}
```

### Browser Connection Lost

```typescript
try {
  await page.goto(url)
} catch (error) {
  if (error.message.includes('Browser closed')) {
    browser = await chromium.launch()
    // retry
  }
}
```

---

## Resources

- [Playwright Docs](https://playwright.dev/)
- [Puppeteer Docs](https://pptr.dev/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [LambdaTest Playwright Guide](https://www.lambdatest.com/support/docs/playwright-testing/)
