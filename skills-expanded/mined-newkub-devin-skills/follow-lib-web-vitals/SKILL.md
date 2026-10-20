---
name: follow-lib-web-vitals
description: Use web-vitals to measure Core Web Vitals — LCP, INP, CLS, FCP, TTFB reporting
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - run-dev
  - run-profiler
---

## Goal

Use web-vitals to measure Core Web Vitals — LCP, INP, CLS, FCP, TTFB reporting

## Scope

Use when the task involves measuring Core Web Vitals with `web-vitals` — setup reporting, metric callbacks, attribution, debugging

- Use this skill for field data (real-user metrics) — for lab tools (Lighthouse) and profiling use `/run-profiler` or `/deep-optimize` instead
- Thresholds: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 are considered good

- Latest: `web-vitals@6.2.2` (verified 2026-09-16)
- References: [apis](references/apis.md) 
## Execute

### 1. Setup And Usage

> Goal: use it correctly per the official docs

1. Use the `onLCP`, `onINP`, `onCLS`, `onFCP`, `onTTFB` callbacks — not the get* functions (deprecated)
1. Send metrics to an analytics endpoint — batch or the beacon API
1. Report only in production + a sample rate — not every session
1. Set the attribution build (`web-vitals/attribution`) when debugging regressions
1. v6: always import types with `import type` (types are explicit type exports), e.g. `import type { Metric } from 'web-vitals'`
1. v6: supports soft navigations — SPA route changes can be reported as separate metrics
1. v6 attribution: `onINP` defaults to `includeProcessedEventEntries: false` — set it to `true` yourself if you want processed event entries

### 2. Report Metrics

> Goal: send metrics to an endpoint correctly

1. The metric object has `{ name, value, rating, delta, entries, id }` — `rating` is `good` / `needs-improvement` / `poor`
2. Use `navigator.sendBeacon` or `fetch` + `keepalive: true` — most metrics fire when the page is unloading
3. The endpoint must accept `text/plain` or parse the body itself — sendBeacon doesn't always let you set the content-type
4. Use `reportAllChanges: true` only for debugging — by default it reports only the final value when the page is hidden
5. `onLongTasks` is a supplement when debugging INP/long-task issues

### 3. Verify

> Goal: confirm correct usage

1. Do `/run-verify` for lint, typecheck
2. Do `/run-test` if there are relevant tests
3. Check the latest official docs before using an API you're unsure about (web vitals lib)

### Workflows

- Install + `on*` callbacks + reporting to an endpoint → `workflows/setup-vitals/SKILL.md`
- Improve LCP/INP/CLS patterns → `workflows/optimize-vitals/SKILL.md`

## Rules

- INP replaced FID since v3; `onFID` was removed since v5 — never use it
- Use `navigator.sendBeacon` or `fetch keepalive` for reporting
- Don't block the main thread to report metrics

- Use /run-verify if needed
- Use /run-test if needed
- Use /run-dev if needed
- Use /run-profiler if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (web vitals lib)
- No known security/performance pitfalls (web vitals lib)
- Lint, typecheck, tests pass
