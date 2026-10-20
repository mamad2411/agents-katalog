---
name: follow-lib-web-vitals-optimize vitals
description: Improve Core Web Vitals — LCP, INP, CLS optimization patterns
argument-hint: "[metric]"
related:
  - follow-lib-web-vitals
  - report-before-after
  - run-profiler
---

## Goal

Improve the Core Web Vitals scores — LCP, INP, CLS with proven patterns, measured before and after

## Scope

Use when the metrics reported via `web-vitals` miss the thresholds (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) — covers diagnosis with attribution and per-metric optimization patterns

## Execute

### 1. Diagnose With Attribution

> Goal: identify the root cause of the failing metric with real data

1. Use the `web-vitals/attribution` build to see which element/sub-part broke the metric (e.g. the LCP element, the INP interaction target, the CLS shift sources)
2. Do `/deep-optimize` — separate the problems: slow server (TTFB), render-blocking resources, long tasks, layout shifts
3. Capture baseline numbers before fixing — do `/run-profiler` or check the field data being reported

### 2. Optimize LCP

> Goal: make the largest element render faster

1. TTFB: reduce server response time — CDN, caching, SSR/streaming
2. Resource load: preload the LCP image (`<link rel="preload">` or `fetchpriority="high"`), compress/resize images, use modern formats (AVIF/WebP)
3. Render-blocking: defer async scripts, inline critical CSS, reduce render-blocking resources
4. Avoid lazy-loading the LCP image — always load it eagerly

### 3. Optimize INP

> Goal: reduce interaction latency

1. Break up long tasks — use `scheduler.yield()` or chunk work so the main thread stays free
2. Reduce work in event handlers — defer non-critical work out of the interaction
3. Use `useTransition`/`useDeferredValue` (React) or the equivalent for expensive updates
4. Reduce DOM size and unnecessary event listeners — use passive listeners for scroll/touch

### 4. Optimize CLS

> Goal: reduce unexpected layout shifts

1. Always set `width`/`height` or `aspect-ratio` on images/videos/iframes — reserve space before load
2. Avoid injecting content above existing content — ads, banners, and late-loading UI must reserve space
3. Use `font-display: swap` carefully + preload fonts for web fonts — reduce FOIT/FOUT shifts
4. Use CSS `transform` animations instead of layout-affecting properties (top/left/width/height)

### 5. Verify And Compare

> Goal: measure the metrics after fixing against the baseline

1. Capture field data after deploy, or use lab tools (Lighthouse) to compare against the baseline via `/report-before-after`
2. Every fix in its own commit — to isolate the impact per metric
3. If a metric doesn't improve or regresses → revert that point, then report

## Rules

- Always diagnose with attribution data first — never guess
- Fix one point at a time ordered by impact (high → low) — don't change many at once if you can't separate the results
- Preserve behavior — optimization must not change the UX/output
- Field data (real users) matters more than lab scores — measure both, but field decides
- Use `/follow-lib-web-vitals` for setup

## Expected Outcome

- The root cause of metric regressions is identified via attribution
- LCP/INP/CLS improve against the baseline with real numbers
- No UX regression
