---
name: lightpanda-browser
description: "Trigger: headless browser, Playwright, Puppeteer, E2E tests, scraping, browser automation, CDP, read a web page, screenshot, captura, PDF render. Pick Lightpanda (default) or Chromium (pixels only) and wire Playwright to it."
metadata:
  author: "alvaroofernaandez"
  version: "1.0"
---

## Activation Contract

Load before launching any headless browser: Playwright or Puppeteer scripts, E2E
tests, scraping, reading/extracting a page, form automation, or any screenshot,
visual check or HTML-to-PDF render.

## Hard Rules

- **Lightpanda is the default headless browser.** It is not Chromium-based,
  written in Zig, far lighter on RAM/CPU and built for agents.
- **Lightpanda has no graphical rendering engine.** It ignores CSS layout:
  `page.screenshot()` and `lightpanda fetch --dump png|pdf` return a
  *text-only* render (verified: a centered 26em page comes out full-width,
  CJK glyphs missing). Never present that output as a screenshot.
- **Chromium only when pixels matter**: real screenshots, visual regression,
  `aval design gate` render gates (contrast, overflow, target size, responsive,
  reduced motion), `design-taste-frontend` look-and-fix loop, HTML-to-PDF
  (`pdf-report` and any branded PDF/manual skill), and
  anything reading `getBoundingClientRect`/computed layout.
- If a flow fails on Lightpanda because of a missing Web API (it is beta),
  rerun that one flow on Chromium and say so; do not switch the whole suite.
- Always set `LIGHTPANDA_DISABLE_TELEMETRY=true` (telemetry is on by default).

## Decision Gates

| Task | Browser |
|---|---|
| E2E functional flow (navigate, click, fill, assert text/URL/DOM) | Lightpanda |
| Scraping, page → markdown/HTML/JSON-LD | Lightpanda (`fetch --dump`) |
| Agent reads/browses a page (no script needed) | Lightpanda `fetch --dump markdown` or `lightpanda mcp` — no Node at all |
| Screenshot, visual diff, layout/contrast gate | Chromium |
| PDF generation | Chromium |
| Lightpanda lacks an API the page needs | Chromium for that flow only |

## Execution Steps

1. Install if missing: `brew install lightpanda-io/browser/lightpanda` (Docker: `lightpanda/browser:nightly`, CDP on 9222).
2. Start the CDP server:
   `LIGHTPANDA_DISABLE_TELEMETRY=true lightpanda serve --host 127.0.0.1 --port 9222`
3. Connect Playwright over CDP (use `playwright-core`; no bundled browser needed):

   ```js
   import { chromium } from 'playwright-core';
   const browser = await chromium.connectOverCDP('ws://127.0.0.1:9222');
   const page = await (await browser.newContext()).newPage();
   ```

   Puppeteer: `puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:9222' })`.
4. Playwright Test (verified with 1.63.0 in three repos): add a `webServer`
   entry `{ command: 'lightpanda serve --host 127.0.0.1 --port 9222', url:
   'http://127.0.0.1:9222/json/version', reuseExistingServer: true, env: {
   LIGHTPANDA_DISABLE_TELEMETRY: 'true' } }`, a `lightpanda` project with
   `use: { cdpEndpoint: 'ws://127.0.0.1:9222' }`, and a `chromium` project
   limited (`testMatch`) to pixel specs. Override `browser` in a shared fixture
   and make EVERY spec import `test`/`expect` from it — a spec importing from
   `@playwright/test` silently keeps launching Chromium:

   ```ts
   export const test = base.extend<{}, { cdpEndpoint: string | undefined }>({
     cdpEndpoint: [undefined, { scope: 'worker', option: true }],
     browser: [async ({ cdpEndpoint, playwright, browserName, launchOptions }, use) => {
       const b = cdpEndpoint
         ? await playwright.chromium.connectOverCDP(cdpEndpoint)
         : await playwright[browserName].launch(launchOptions);
       await use(b);
       await b.close();
     }, { scope: 'worker' }],
   });
   ```

   Read the ports from env (e.g. `E2E_LIGHTPANDA_PORT`) — worktrees and dev
   servers collide on fixed ports. CI (Linux): download
   `https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux`.
5. One-shot reads without a script:
   `lightpanda fetch --dump markdown --wait-until networkidle <url>`
   (`html`, `markdown`, `structured_data`; `--wait-selector` to wait for content).
6. Agent flows: prefer `lightpanda mcp` (stdio MCP server; `--port` for HTTP,
   `--cdp-port` to also expose CDP) or `fetch` over writing a Playwright script.
7. Stop only what you started, by the PID you captured. NEVER `pkill`/`killall`
   by pattern (`lightpanda serve`, `next dev`, `node`): other sessions run dev
   servers and Lightpanda instances on this machine.

## Install Footprint

- New projects: `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 pnpm add -D playwright-core`
  (13 MB library, no browser). `@playwright/test` only when the runner is needed;
  keep the same env var so no Chromium lands per project.
- Keep one Chromium headless shell per pinned Playwright revision, only for the
  pixel tasks above. Before pruning `~/Library/Caches/ms-playwright`, list which
  `playwright-core/browsers.json` pin each revision — a revision still pinned by a
  project is in use, not a duplicate.

## Benchmark (2026-11-04, local page, fill + click + read, 20 runs)

| Setup | Browser RSS | Median per page |
|---|---|---|
| Playwright + Chromium headless shell | 284 MB | 82 ms |
| Playwright + Lightpanda | 39 MB | 38–44 ms |
| Puppeteer + Lightpanda | 39 MB | 54–57 ms |
| `lightpanda fetch --dump markdown` | 31 MB | 240 ms per call, no Node |

Playwright stays the client: fastest per action and it keeps the test runner.

## Verified on 1.0.2 (2026-11-04)

Works over CDP with Playwright: `goto`, `title`, `content`, `evaluate`, `$eval`,
locators (`locator`, `getByRole`, strict mode), `click` + navigation,
`expect().toHaveText/toHaveCount`.

**Hydration probe first.** Before moving any spec, load one client-rendered
route on Lightpanda and check the app hydrates (a client-only element appears,
or React fibers exist on the DOM). A Next 16 app (gdr) never hydrated: 0
fibers after 15 s, no errors — server-rendered headings pass, everything
interactive times out. If the probe fails, wire the `lightpanda` project but
leave it empty.

Measured on 13 repos (2026-11-04): Lightpanda paid off on pure functional
suites (freak-hub auth specs 26 s vs 1.1 min on Chromium), and moved nothing
in layout-heavy marketing sites or apps gated by Clerk.

Known gaps — keep these specs on Chromium:
- Clerk browser sign-up/sign-in does not complete (mir-platform onboarding
  never renders). Use a pre-authenticated `storageState` or keep the spec on Chromium.
- Hydration can fail silently on some React/Next apps (see probe above).
- No `navigator.serviceWorker`: apps mocking with MSW in the browser cannot run.
- `ReadableStream.tee` missing (logged as a warning).
- Anything using `setViewportSize`, `boundingBox`, `getComputedStyle`,
  `toHaveCSS`, `emulateMedia`, hover/`mouse.wheel` geometry, canvas/WebGL
  (maps, charts) or axe contrast.
Split by file: one layout assertion keeps the whole spec file on Chromium.

## Output Contract

State which browser ran each check. A screenshot or visual claim must come from
Chromium; label any Lightpanda image as text-only.
