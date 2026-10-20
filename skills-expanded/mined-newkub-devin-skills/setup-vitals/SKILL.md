---
name: follow-lib-web-vitals-setup-vitals
description: Setup web-vitals — install, on* callbacks, reporting to endpoint
argument-hint: "[endpoint]"
related:
  - follow-lib-web-vitals
  - run-install
  - run-verify
  - run-dev
  - resolve-errors
---

## Goal

Set up `web-vitals` in a project — install it, wire the `on*` callbacks, and send metrics to an analytics endpoint

## Scope

Use when setting up Core Web Vitals reporting for the first time — covers install, `onLCP`/`onINP`/`onCLS`/`onFCP`/`onTTFB`, beacon transport, and production sampling

## Execute

### 1. Install And Check State

> Goal: install `web-vitals` and check the entry point

1. Install `bun add web-vitals` (use the package manager the project uses)
2. Identify the app's entry point (`main.ts`, `index.tsx`, app layout) where reporting will be wired
3. If it already exists → verify the version and config only (idempotent)

### 2. Wire Metric Callbacks

> Goal: report metrics with the `on*` functions

```ts
import { onCLS, onINP, onLCP, onFCP, onTTFB } from 'web-vitals'

function sendToAnalytics(metric) {
  const body = JSON.stringify(metric)
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/analytics', body)
  } else {
    fetch('/analytics', { body, method: 'POST', keepalive: true })
  }
}

onCLS(sendToAnalytics)
onINP(sendToAnalytics)
onLCP(sendToAnalytics)
onFCP(sendToAnalytics)
onTTFB(sendToAnalytics)
```

1. Use the `on*` callbacks — not `get*` (deprecated)
2. Use `navigator.sendBeacon` or `fetch` with `keepalive: true` — metrics can still be sent while the page is unloading
3. Always import `import type { Metric }` or the types you need with `import type` (v6 types are explicit type exports)
4. v6 supports soft navigations — SPA route changes can be reported as separate metrics

### 3. Configure Reporting Strategy

> Goal: send metrics efficiently

1. Report only in production — guard it with an env check
2. Use a sample rate (e.g. 10% of sessions) if traffic is high — not every session
3. Batch metrics or send them one by one, per the endpoint design
4. Use the `web-vitals/attribution` build when you need to debug regressions — the attribution data gives the element/cause of the metric
5. The endpoint must accept `application/json` or the text from sendBeacon — check the backend supports it

### 4. Verify

> Goal: confirm metrics actually reach the endpoint

1. Run `/run-dev` — open the DevTools Network tab and check the beacon/fetch requests to `/analytics`
2. Check the payload has `name`, `value`, `id`, `rating` complete
3. Do `/run-verify` for lint/typecheck
4. If it breaks → do `/resolve-errors` max 3 rounds, then stop and report

## Rules

- INP replaced FID since v3; `onFID` was removed since v5 — never use it
- Never block the main thread to report metrics — use beacon/keepalive only
- Never report in dev when unnecessary — guard with env
- Always import `web-vitals` types with `import type` (v6)
- Use `/follow-lib-web-vitals` for the full reference

## Expected Outcome

- `web-vitals` is installed and reports LCP/INP/CLS/FCP/TTFB to the real endpoint
- Reporting uses beacon/keepalive and doesn't block the main thread
- Production-only + the configured sampling
- Lint/typecheck pass
