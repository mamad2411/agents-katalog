---
name: qa-browser-check
description: Fast browser health check for web pages. Catches 404s, console errors, and missing assets. Returns JSON with check results per URL.
---

# qa-browser-check - Quick Browser Health Check

Fast sanity check for web pages - catches 404s, console errors, and missing assets.

## Input Schema

```json
{
  "project_dir": "/path/to/project",
  "ticket_id": "TICKET-XXX",
  "urls": ["http://localhost:8080/index.html"],
  "check_console": true,
  "check_network": true,
  "timeout_ms": 5000
}
```

## Behavior

### 1. Server Detection (Same as run-tests)

Check if dev server is running before attempting to load pages:

```bash
lsof -i :8080 | grep LISTEN || (cd $project_dir && python3 -m http.server 8080 &)
```

### 2. Page Checks

For each URL, verify:

| Check | Pass Criteria |
|-------|---------------|
| Page loads | HTTP 200 response |
| No 404s | All resources load (images, CSS, JS) |
| No console errors | `window.console.error` not called |
| No CORS errors | No cross-origin blocks |
| DOM renders | Expected elements exist |

### 3. Quick Implementation

Use Playwright in check mode (not test mode):

```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch();
const page = await browser.newPage();

// Collect console errors
const consoleErrors = [];
page.on('console', msg => {
  if (msg.type() === 'error') consoleErrors.push(msg.text());
});

// Collect failed requests
const failedRequests = [];
page.on('requestfailed', req => {
  failedRequests.push({ url: req.url(), error: req.failure().errorText });
});

// Load page
await page.goto(url, { waitUntil: 'networkidle' });

// Check for expected elements
const hasBody = await page.$('body') !== null;
```

## Output Format

```json
{
  "skill": "qa-browser-check",
  "status": "success|failure",
  "checks": [
    {
      "url": "http://localhost:8080/index.html",
      "loaded": true,
      "status_code": 200,
      "console_errors": [],
      "failed_requests": [],
      "dom_valid": true
    }
  ],
  "summary": {
    "total_urls": 1,
    "passed": 1,
    "failed": 0
  },
  "errors": [],
  "warnings": [],
  "next_action": "proceed|fix"
}
```

## Error Categories

| Category | Severity | Example |
|----------|----------|---------|
| PAGE_404 | HIGH | Main page returns 404 |
| ASSET_404 | MEDIUM | CSS/JS file not found |
| CONSOLE_ERROR | MEDIUM | JavaScript runtime error |
| CORS_ERROR | LOW | Cross-origin block (may be expected) |
| TIMEOUT | HIGH | Page didn't load in time |
