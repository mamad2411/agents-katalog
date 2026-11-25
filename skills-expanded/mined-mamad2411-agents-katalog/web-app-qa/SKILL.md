---
name: web-app-qa
description: "Verify a web application works end-to-end in a real browser before reporting a fix complete — catch CORS errors, JS crashes, and blank pages that HTTP status codes miss."
version: 1.3.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [qa, testing, verification, frontend, browser, playwright]
    triggers: [qa, testing, verification, browser-test, playwright, smoke-test, visual-check, ui-test, end-to-end]
    related_skills: [systematic-debugging, firefox-remote-control]
---

# Web App QA

## the operator's Rule

**Do NOT say a fix is working until you have logged in through the browser UI, navigated all relevant pages, and verified the app functions correctly.** HTTP 200 from curl is NOT sufficient. API responses returning JSON is NOT sufficient. Only a real browser engine (Playwright Firefox headless, or the operator's Firefox) counts as verified.

## When to Use

- AFTER applying any web app fix, before telling the user it's complete
- When HTTP status codes all say 200 but the user reports "it's not working"
- When debugging a demo-mode app that authenticates client-side (localStorage, Supabase, etc.)
- When environment variables at the system level might override app configuration
- For verifying multi-role apps (admin, contractor, client) — each role path must be tested

## Toolkit

### Playwright (Headless — Chromium or Firefox)

Primary QA tool on Windows. Prefer Chromium (more reliable headless on Windows). Detect what's available:

```bash
cd <project>
npm install --save-dev --legacy-peer-deps playwright

# Check what's already installed, then install what you need
npx playwright install --list 2>/dev/null
npx playwright install chromium  # most reliable on Windows
# or npx playwright install firefox
```

**Global install path (the operator's machine):** If Playwright is installed globally, the module lives at:
```
C:\Users\<user>\AppData\Roaming\npm\node_modules\@playwright\test\node_modules\playwright
```
Use `NODE_PATH` to require from a script:
```bash
NODE_PATH="${USER_HOME}/AppData/Roaming/npm/node_modules/@playwright/test/node_modules" node qa-check.js
```

**Bundled Firefox binary location (if installed):**
```
C:\Users\<user>\AppData\Local\ms-playwright\firefox-*\firefox\firefox.exe
```

**System Firefox as fallback:** If Playwright's bundled Firefox fails (common on Windows with SWGL headless errors), use the system Firefox:
```javascript
const browser = await firefox.launch({
  headless: true,
  executablePath: 'C:/Program Files/Mozilla Firefox/firefox.exe',
  args: ['--no-sandbox']
});
```
Note: System Firefox in headless mode may crash with `RenderCompositorSWGL failed mapping default framebuffer` on this GPU. In that case, use Playwright's bundled Chromium instead (no SWGL issues), or install `geckodriver` for Selenium-based testing.

**Selenium alternative:** If Playwright can't launch Firefox headless, use Selenium:
```bash
npm install -g geckodriver  # installs geckodriver
```
Then use Selenium 4 with Firefox (see Python script pattern in the QA section).

**Extension choice:** Both `.cjs` (CommonJS) and `.mjs` (ESM) work. Use whichever matches your project:

```javascript
// Option A — .cjs file (CommonJS)
// Save as qa-check.cjs
const { chromium } = require('playwright');

// Option B — .mjs file (ESM, modern import syntax)
// Save as qa-check.mjs
import { firefox } from 'playwright';
// Works with any browser: chromium, firefox, webkit
```

If your project has `"type": "module"` in package.json, `.cjs` is needed for `require()`. Otherwise both work.

### QA Script Template — Smoke Test (no auth)

Use this pattern for quick verification of a demo/public app without login. Checks every route for JS errors, network failures, and failed fetch requests.

```javascript
// Save as qa-smoke.mjs
import { firefox } from 'playwright';

const BASE = 'http://localhost:PORT';
const ROUTES = ['/', '/login', '/dashboard/admin', '/dashboard/admin/settings',
                '/dashboard/client', '/dashboard/contractor', '/contact', '/careers'];

async function run() {
  const browser = await firefox.launch({ headless: true });
  let pass = 0, fail = 0;

  for (const route of ROUTES) {
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await context.newPage();

    const consoleErrors = [], networkErrors = [], fetchErrors = [];
    page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
    page.on('pageerror', err => networkErrors.push(err.message));
    page.on('requestfailed', req => networkErrors.push(`${req.url()} — ${req.failure()?.errorText}`));

    try {
      await page.goto(`${BASE}${route}`, { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForTimeout(2000); // let async fetches settle

      // Check fetch responses via Performance API
      const badFetches = await page.evaluate(() =>
        performance.getEntriesByType('resource')
          .filter(e => e.initiatorType === 'fetch' && e.responseStatus >= 400)
          .map(e => `${e.name} (${e.responseStatus})`)
      );

      const h1 = await page.$eval('h1', el => el.textContent.trim()).catch(() => '(no h1)');
      const label = consoleErrors.length + networkErrors.length + badFetches.length === 0 ? '✅' : '❌';
      console.log(`${label} ${route} — ${h1}`);
      consoleErrors.forEach(e => console.log(`   console: ${e.slice(0, 200)}`));
      networkErrors.forEach(e => console.log(`   network: ${e.slice(0, 200)}`));
      badFetches.forEach(e => console.log(`   fetch ${e}`));

      if (consoleErrors.length + networkErrors.length + badFetches.length > 0) fail++; else pass++;
    } catch (err) {
      console.log(`❌ ${route} — ${err.message}`);
      fail++;
    }
    await context.close();
  }

  await browser.close();
  console.log(`\nRESULTS: ${pass} passed, ${fail} failed`);
}
run().catch(err => { console.error(err); process.exit(1); });
```

### QA Script Template — Multi-Role Login Verification

Use this pattern when the app requires login with different user roles. It clears localStorage between roles to avoid auth state leaking.

```javascript
// Save as qa-roles.mjs
import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  const errors = [];
  page.on('pageerror', err => errors.push({ type: 'js', msg: err.message }));
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push({ type: 'console', msg: msg.text() });
  });

  await page.goto('http://localhost:PORT/', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(1000);

  const roles = [
    { email: 'admin@demo.com', path: '/dashboard/admin' },
    { email: 'client@demo.com', path: '/dashboard/client' },
    { email: 'contractor@demo.com', path: '/dashboard/contractor' },
  ];

  for (const role of roles) {
    // Clear localStorage to reset auth state between roles
    await page.evaluate(() => localStorage.clear());
    await page.goto('http://localhost:PORT/login', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(500);
    await page.fill('input[type="email"]', role.email);
    await page.fill('input[type="password"]', 'demo123');
    await page.click('button[type="submit"]');
    await page.waitForTimeout(3000);

    const url = page.url();
    console.log(`${role.email}: ${url.includes(role.path) ? '✅' : '❌'} ${url}`);
  }

  console.log('Errors:', JSON.stringify(errors));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
```

### What to Check for Each Page

| Check | How | Pass/Fail Signal |
|-------|-----|-----------------|
| **JS errors** | `page.on('pageerror')` collector | Any entry = fail |
| **Console errors** | `page.on('console')` with `msg.type() === 'error'` | CORS errors, 404 fetch errors = fail |
| **URL after redirect** | `page.url()` | Should be `/dashboard/{role}`, not `/login` |
| **Page content** | `page.textContent('body')` | Should be > 100 chars with actual content |
| **No crash** | `page.on('crash')` | Process exit if fired |

## Common Failure Modes

### 0. Auth Returns 500 / "Internal Server Error" — Stale Compiled Code

**Symptom:** `curl -X POST /api/auth` returns 500, but testing the underlying API directly (PostgREST, database) works fine. Logging into the browser shows a blank login redirect or a 500 toast.

**Root cause (three variants):**

A. **Truncated JWT/API keys** — After bulk file rewrites by subagents, base64-encoded service-role keys in `.env.local`, API route files, and `kong.yml` may be truncated to display length (~13-20 chars). The auth route sends a garbage key → Kong rejects it → PostgREST never gets the query → 500.

B. **System env var overrides** — `NEXT_PUBLIC_SUPABASE_URL` set at the system level (Windows env vars) overrides `.env.local`. Next.js inlines the system value into compiled code. See `references/cors-env-var-override.md` and `systematic-debugging`'s `references/nextjs-env-var-inlining.md`.

C. **Orphaned dev server child processes** — On Windows, killing the parent Next.js process (via Ctrl+C, `kill`, or terminal closure) may leave webpack worker children alive on the same port. They continue serving old compiled code with stale env vars. `fuser` can't kill them from MSYS. Fix:
   ```bash
   # Find the PID
   netstat -ano | grep ':PORT' | grep LISTEN
   # Kill it — MSYS needs double-slash to avoid path conversion
   taskkill //F //PID <number>
   ```

**Diagnosis:** Read the compiled route output:
```bash
cat .next/server/app/api/auth/route.js | grep "SRV =\|SUPABASE_URL"
```
Look for truncated strings or wrong inlined URLs.

**Fix:** Regenerate truncated keys with the correct signing secret, unset system env vars, delete `.next`, kill all orphaned processes, then restart clean via `bash start-dev.sh`.

### 1. CORS Error on Login (Firefox shows "Cross-Origin Request Blocked")

**Symptom:** Login form submits but you stay on the login page. No visible error in the UI. Console shows CORS violation.

**Root cause:** System-level environment variables set a `NEXT_PUBLIC_SUPABASE_URL` pointing to a remote Supabase instance. The app tries real Supabase auth instead of demo mode, and the browser blocks the cross-origin POST from localhost.

**Fix (Windows/MSYS2):**
```bash
# Unset env vars before starting the dev server
unset NEXT_PUBLIC_SUPABASE_URL
unset NEXT_PUBLIC_SUPABASE_ANON_KEY
unset SUPABASE_SERVICE_ROLE_KEY
npx next dev -p 3333
```

Create a `start-dev.sh` script in the project root for convenience:
```bash
#!/bin/bash
unset NEXT_PUBLIC_SUPABASE_URL
unset NEXT_PUBLIC_SUPABASE_ANON_KEY
unset SUPABASE_SERVICE_ROLE_KEY
cd "$(dirname "$0")"
NODE_OPTIONS="--max-old-space-size=2048" exec npx next dev -p 3333
```

And add an npm script to `package.json`:
```json
"dev:demo": "bash start-dev.sh"
```

**Why `.env.local` won't fix it:** Next.js checks `process.env` first when looking up environment variables. System env vars from Windows are already in `process.env` when Next.js starts. `.env.local` values are only applied if the key does NOT already exist in `process.env`. You must UNSET them before the Node.js process starts.

### 2. API Returns 200 But Dashboard Is Blank

**Symptom:** `curl http://localhost:3333/api/projects` returns 200 with data. User says the dashboard is blank.

**Root cause:** Client-side JavaScript crashes during hydration because API response data doesn't have fields the UI expects. The crash is invisible to curl — only a real browser engine catches it.

**Fix strategy:**
1. Test with Playwright Firefox — collect `page.on('pageerror')` and page content
2. Find the specific field (e.g., `scheduledDates`, `tasks`, `materials`) that's `undefined`
3. Add `|| []` fallback in the API mapping function:
   ```javascript
   scheduledDates: p.scheduled_dates || p.scheduledDates || [],
   materials: p.materials || [],
   tasks: p.tasks || [],
   ```
4. Re-test: the page should render with empty sections instead of crashing

### 3. `Promise.all` Masks Single-Endpoint Failure

**Symptom:** All data is missing from the dashboard even though most API endpoints work fine individually. Only one endpoint fails.

**Root cause:** `Promise.all([fetch(A), fetch(B), fetch(C)])` rejects entirely if ANY one promise rejects. A single failing endpoint (e.g., `/api/users` using a different data source) blanks the whole page.

**Diagnostic:** Hit each endpoint individually with `curl`. Find the one that fails or times out. Check if it uses a different data store (Supabase vs local JSON).

**Fix:** Either make the failing endpoint use the same data source, or convert to `Promise.allSettled()`.

### 4. Dev Server Returns 200 But Browser Gets 404 For JS/CSS Chunks

**Symptom:** `curl` shows HTTP 200 on the page. Playwright opens the page and console fills with 404 errors for `_next/static/chunks/` URLs. Login form renders but clicking submit does nothing.

**Root cause:** The dev server compiles JavaScript and CSS chunks **lazily** — only when first requested. After a clean start (no `.next` cache), the HTML is served immediately but webpack hasn't finished compiling the chunks yet. The browser requests them, gets 404s, and the page has no JavaScript.

**Fix:** Wait for chunks to be available before running QA (see Pitfalls → Chunk Compilation Race). The reliable pattern is to curl a specific chunk URL until it returns 200, then proceed with Playwright.

### 5. Next.js CSS Not Loading in Production Build (Broken by `loading.tsx`)

**Symptom:** `next build` succeeds, `next start` serves pages at HTTP 200, but CSS is either missing entirely (layout returns 500) or the page renders as unstyled HTML. JS chunks may also fail (400/404). Toggling between `next dev` and `next start` makes the problem appear/disappear.

**Root cause:** Any route file using `loading.tsx` makes that route segment **dynamic** in Next.js. When a layout has dynamic children, Next.js may fail to resolve the CSS chunk path during production builds, emitting a `layout.css` that references hashes that don't exist or returning 5xx for the CSS request. The dev server (HMR) handles this differently and may work fine, masking the issue.

**Diagnosis:**
```bash
# Check if loading.tsx files exist
find app -name 'loading.tsx' 2>/dev/null
# Check CSS in production — should return 200 with substantial content
curl -s -o /dev/null -w "%{http_code} %{size_download}" http://localhost:PORT/_next/static/css/*.css
# Listen for 5xx on CSS assets
curl -v http://localhost:PORT/_next/static/css/app/layout.css 2>&1 | head -20
```

**Fix — three options (try in order):**

A. **Remove `loading.tsx` files** — If the loading UI isn't critical, delete the `loading.tsx` files that make routes dynamic. Routes become static again and CSS resolves correctly. This is the safest fix.

B. **Clean rebuild** — Sometimes the `.next` cache has stale artifacts. Run `next build` (which overwrites `.next` without needing a delete). If that doesn't work, `rm -rf .next` then rebuild.

C. **Add metadata export to layout** — In the root layout, ensure there's a `metadata` or `generateMetadata` export. This can force Next.js to include the layout in the static CSS compilation.

**Verification:** After the fix, curl the CSS file directly (should return 200, 70KB+). Open the page in real Firefox/Playwright and verify `performance.getEntriesByType('resource')` has no 400+ entries for `.css` files.

### 6. Build Corruption After Dirty `next build`

**Symptom:** Both `next start` (production) and `next dev` return 500 with `Cannot find module './NNN.js'`. The `.next/server/pages/` directory contains `_document.js`, `_app.js`, etc. even though this is an App Router project.

**Root cause:** Running `next build --no-lint` after a failed build or cache corruption leaves Page Router artifacts in `.next`. These reference chunk IDs that don't exist in the new build output. The error propagates to BOTH server modes because `next dev` also reads from `.next/server/`.

**Fix:** The ONLY reliable fix is `rm -rf .next` followed by a clean restart. In-place rebuilds compound the corruption.

## Firefox MCP DevTools QA Workflow

See `references/firefox-mcp-qa-workflow.md` for the complete workflow using the operator's Firefox browser via the MCP DevTools tools — navigate, fill forms, take screenshots, and send them as evidence. **Use this when the operator is online and expects visual proof of a working UI.**

**For Angular SPAs** (and when the `mcp_chrome_devtools_mcp_*` tools are available instead of Firefox), see `references/chrome-mcp-angular-patterns.md`. That reference covers the critical hash-route auth pitfall that does not apply to traditional multi-page apps.

**Two modes:**
- **Immediate QA**: Dev server is running; navigate Firefox to each page, screenshot, check console/network, send results.
- **Multi-role verification**: Clear localStorage between roles, log in as admin → client → contractor, screenshot each dashboard.

The Playwright approach (above) works for automated/CI scenarios. The **Firefox MCP approach is for interactive QA** where the operator wants to see actual page screenshots before accepting "it's working."

**Key workflow steps** (full details in the reference):
1. Launch dev server with clean env vars
2. Navigate Firefox to login page
3. Fill credentials and submit
4. Verify redirect URL to correct dashboard path
5. Take screenshot of rendered dashboard
6. Check console errors and network failures
7. Repeat for each role (clearing localStorage between)
8. Send screenshots with MEDIA: paths as evidence

## Pitfalls

- **Curl HTTP 200 means nothing for client-side rendering.** The server may return HTML shell that looks fine, but the JavaScript fails during hydration. Always use a real browser engine for final verification.
- **Firefox and Chrome differ on CORS.** Firefox blocks cross-origin POST to standard Supabase endpoints from localhost, while Chrome may silently fail or be more lenient. Always test with the user's browser.
- **System env vars on Windows persist across terminals.** If set globally, they leak into every child process. `unset` in bash only affects the current shell session. Use a startup script to guarantee clean env.
- **localStorage persists between logins in Playwright.** Clear localStorage between role tests: `page.evaluate(() => localStorage.clear())`.
- **Playwright's `page.fill()` times out if the page redirects before the fill executes.** After login as one role, navigating directly to `/login` as another role may trigger an auth redirect loop before the form loads. Always clear localStorage first.
- **UIDs in Firefox MCP DevTools change between snapshots.** Always take a fresh snapshot before clicking or filling elements — old UIDs from a previous snapshot will fail.

### Angular SPA Auth: Hash-Route Navigation Destroys Session

**Symptom:** You log in successfully, reach the dashboard, then navigate to a different route (e.g., inbox, compose) via `mcp_chrome_devtools_mcp_navigate_page` and get dumped back at the login page.

**Root cause:** Angular SPAs store auth tokens in JavaScript in-memory state. Loading a URL with a hash fragment (`/#/products/emessage/inbox`) via full-page navigation reloads the entire Angular application, destroying the in-memory auth context. The app has no way to restore the session and redirects to login.

**Fix:** Navigate within the SPA by clicking in-page links using `mcp_chrome_devtools_mcp_click`, not by loading URLs directly. Find the link element UID in the snapshot and click it — Angular's router handles the navigation without a full page reload.

See `references/chrome-mcp-angular-patterns.md` for the full workflow.

### Mobile Client Cache Masquerades as Server Downtime

**WHEN the user reports "I can't connect from my phone" but all server-side checks pass (DNS resolves globally, TLS cert is valid, API returns 200, Caddy logs show no errors, full-page curl succeeds):**

1. **The most common cause is stale browser cache on the phone.** Mobile browsers aggressively cache HTML, JS, and API responses — especially Safari and Chrome on iOS. If the user visited during a period of server downtime (Spacebar restart, broken branding, Caddy misconfiguration), the phone cached the broken page state. Even after the server is fully restored, the phone continues to serve the cached failure.

2. **Diagnose by checking for NO mobile requests in server logs.** If access logs show zero requests from mobile user agents (iPhone, Android, Mobile Safari) but you know the user tried, the phone isn't reaching the server — it's serving from cache or DNS is stale.

3. **Fix requires the user to clear their browser cache:**
   - **iOS Safari:** Settings → Safari → Clear History and Website Data
   - **Chrome:** Settings → Privacy → Clear Browsing Data → Cached Images and Files → All Time
   - **Alternative:** Open in private/incognito tab (bypasses cache entirely)

4. **Prevention:** When diagnosing a "can't connect" report, include "try private/incognito mode" as Step 0 — before checking DNS, TLS, or server logs. It's the fastest diagnostic and eliminates the most common false negative.

**Cues that trigger this pitfall:**
- User reports "still not working" after you've verified DNS, TLS, and server health
- Server access logs show NO requests from the user's expected IP or device
- The site works from your own device on a different network
- The user previously saw a broken page during earlier debugging sessions

### Chunk Compilation Race (Dev Server After Clean)

After deleting `.next` and starting `npx next dev`, the dev server compiles JS/CSS chunks **lazily** — only when first requested. The HTML shell returns 200 immediately, but referenced chunks (`_next/static/chunks/main-app.js`, `_next/static/css/app/layout.css`) return 404 until webpack finishes compiling them.

**Symptom:** `curl http://localhost:PORT/page` returns 200, but Playwright's `page.waitForURL()` times out or the browser shows a blank page with 404 console errors for `.js` and `.css` chunk URLs.

**Fix — warm up all chunks before QA:**
```bash
# After dev server responds 200 on /login, verify chunks are compiled
for page in "/login" "/dashboard/admin" "/dashboard/client" "/dashboard/contractor"; do
  while [ "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:3333$page")" != "200" ]; do
    sleep 3
  done
done
# Then check a specific chunk
while [ "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:3333/_next/static/chunks/app/login/page.js")" != "200" ]; do
  sleep 3
done
```

Alternatively, do a production build first (`next build --no-lint`) and serve with `next start`. Fallback: wait 30-60s after server start before running QA.

### Production Build Corruption (Mixed Page Router + App Router Artifacts)

Running `next build --no-lint` in a dirty `.next` state (e.g., after a failed build, or after swapping branches) can leave **Page Router artifacts** (`_document.js`, `_app.js`) mixed into the App Router build output. These stale files reference chunk IDs that don't exist in the new build, crashing BOTH `next start` AND `next dev` with:

```
Error: Cannot find module './548.js'
Require stack:
- .next/server/webpack-runtime.js
- .next/server/pages/_document.js
```

**Diagnosis:** Check for Page Router artifacts in the App Router build:
```bash
ls .next/server/pages/  # should be empty or not exist for App Router projects
```

**Fix:** Only `rm -rf .next` + restart works. `next build` in-place will compound the corruption.
```bash
rm -rf .next && npx next dev -p 3333
```

### Hardcoding as Nuclear Option (When Env Vars Won't Die)

When `NEXT_PUBLIC_*` env vars are set at the system level and a startup script that unsets them is impractical or unreliable, the last resort is to **hardcode the value directly in the source file**:

```javascript
// BEFORE (vulnerable to env var poisoning):
const API = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost:44444'

// AFTER (immune):
const API = 'http://localhost:44444'
```

**Apply to:** Auth routes, data-service files, and any file where the env var gets inlined into compiled code. This works because Next.js inlines the literal value at compile time, bypassing runtime env resolution.

**Trade-off:** Hardcoding breaks portability. Only use for local-dev-only files that won't be deployed. Document the assumption with a comment.

## Reference: Firefox Canvas 2D Compatibility

See `references/firefox-canvas-compat.md` for three Firefox Canvas 2D quirks that cause charts to silently fail: `roundRect` polyfill (FF<112), 8-digit hex → rgba converter (FF<106), and ResizeObserver vs rAF execution order (context scale lost on resize). These fix "works in Chrome, blank/nothing in Firefox" for Canvas-based UIs.

## Reference: Firefox MCP DevTools QA Workflow (full)

See `references/firefox-mcp-qa-workflow.md` for the complete workflow with exact tool calls, error detection patterns, and common pitfalls specific to Firefox MCP QA.
