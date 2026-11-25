---
name: web-vitals-field
description: Measure Core Web Vitals in the FIELD with attribution — wire the web-vitals attribution build so a poor INP/LCP/CLS points to the exact element + sub-part. Lab tools cannot field-measure INP; this is the only path to citing the headline CWV.
project_kind: browser   # requires a rendered UI layer; see templates/packs/_project-kind.md
kind: skill
pack: performance
allowed-tools: [Read, Grep, Glob, Bash]
---

# web-vitals-field

## Premise

Field Core Web Vitals **with attribution**, or it is not a finding. Lighthouse runs one synthetic load with zero real interactions — it cannot field-measure INP (Interaction to Next Paint), the headline Core Web Vital since March 2024. The truth comes from real users: the `web-vitals` library's attribution build reports each metric AND the element + timing sub-part responsible, so a regression is citeable ("INP 340ms → `button.add-to-cart`, 280ms in processing") instead of a bare number.

A reported INP/LCP without an attributed target + sub-part breakdown is a halt, not a finding.

This skill stands up the measurement; `bundle-perf` / `lighthouse-ci` consume the budgets, `inp-responsiveness` fixes the INP causes it attributes, and `navigation-speed` consumes the per-route (soft-navigation) INP it surfaces.

## Procedure

1. Install the library (it ships an attribution entry point):
   ```bash
   pnpm add web-vitals
   ```
2. Wire the attribution build to your analytics/RUM sink (NOT the plain `web-vitals` entry — attribution lives in `web-vitals/attribution`):
   ```ts
   import { onINP, onLCP, onCLS, onTTFB, onFCP } from 'web-vitals/attribution';

   const send = (m) => navigator.sendBeacon('/rum', JSON.stringify(m));
   onINP(send);  onLCP(send);  onCLS(send);  onTTFB(send);  onFCP(send);
   ```
   Report on `visibilitychange`/`pagehide` (the library batches the final value) — `sendBeacon` survives the unload, and does not block bfcache.
3. Read the attribution off each metric (the fields below) and pivot your dashboard by the attributed target, not just the metric value.
4. Cross-check the p75 the budget is judged against against **CrUX** (real-world Chrome field data) via the CrUX History API or PageSpeed Insights API — that p75 is what "passing CWV" means, not your lab number.

## Attribution fields (what to read)

**INP** — `metric.attribution`:
- `interactionTarget` — CSS selector of the element that was interacted with (the thing to fix).
- `interactionType` — `pointer` / `keyboard`.
- `inputDelay` — time before the handler ran (main thread busy → break long tasks).
- `processingDuration` — time spent in event handlers (the usual culprit → `scheduler.yield()` / debounce).
- `presentationDelay` — time from handler end to next paint (rendering/layout cost).
- `longAnimationFrameEntries` — array of `PerformanceLongAnimationFrameTiming` (LoAF) entries overlapping the interaction; read `.scripts[].invoker` / `.sourceURL` to name the blocking script.

> Field name is `longAnimationFrameEntries` (an array of LoAF entries) — not `longAnimationFrames`.

**LCP** — `metric.attribution`:
- `element` — the LCP element (selector).
- `url` — the LCP resource URL (if image).
- `timeToFirstByte` — server think-time share (→ `streaming-ssr` if dominant).
- `resourceLoadDelay` — gap between TTFB and the resource starting to load (→ preload / priority).
- `resourceLoadDuration` — how long the resource took to load (→ compress / resize / CDN). *(Renamed from the older `resourceLoadTime`; support both field names if you read older data.)*
- `elementRenderDelay` — time from resource loaded to painted (→ render-blocking JS/CSS).

**CLS** — `metric.attribution`:
- `largestShiftTarget` — selector of the element responsible for the largest layout shift (the thing to reserve space for).
- `largestShiftValue`, `loadState` — magnitude + when in the load it happened.

## Output

```
Field CWV (p75, last 28 days, mobile)        source: RUM /rum + CrUX cross-check

  INP   340ms  POOR   (good ≤200)
        → button.add-to-cart  |  inputDelay 20ms · processingDuration 280ms · presentationDelay 40ms
        → LoAF blocking script: /assets/cart-abc.js (invoker: onClick)
        → fix path: inp-responsiveness — yield in the handler / debounce the recompute

  LCP   2.9s   NEEDS-WORK (good ≤2.5)
        → img.hero  |  TTFB 700ms · loadDelay 400ms · loadDuration 600ms · renderDelay 200ms
        → fix path: TTFB dominates → streaming-ssr; loadDelay → preload + fetchpriority (lcp-audit)

  CLS   0.04   GOOD
  TTFB  700ms  NEEDS-WORK (lab budget)  → server-response-time
        # field-good is ≤800ms (https://web.dev/articles/ttfb); 700ms passes THAT and misses only the
        # stricter 600ms Lighthouse server-response-time audit. Label which bar a value failed —
        # calling a field-good value POOR is how a real regression stops being legible.
```

## SPA / soft navigations

- `web-vitals` reports per page-visit. For client-side route changes (SPAs), INP is attributed to the page the user is on *at interaction time*; CrUX/RUM bucket it to that route.
- Soft navigations, as dated facts: Chrome 151 (2026-07-28) shipped the `soft-navigation` and `interaction-contentful-paint` entry types, and `web-vitals` reports per-route vitals with `reportSoftNavs: true` in Chromium 151+ only. CrUX has published no timeframe for including them (web.dev, *How SPA architectures affect Core Web Vitals*, updated 2026-08-11). So per-route field data comes from your own RUM and covers Chromium only; for other browsers, mark route boundaries yourself (`performance.mark` around router events) and segment RUM by route.

## False positives / gotchas

- Lab tools (Lighthouse) produce a *synthetic* `interaction-to-next-paint` only by scripting an interaction — it is a proxy, never the field value. Never cite lab INP as the measurement.
- A single user's value is noise; budgets are judged on the **p75** across real users.
- Attribution needs the `web-vitals/attribution` import — the plain `web-vitals` import returns the value with no `attribution` object.
- `longAnimationFrameEntries` is only populated where the Long Animation Frames API is supported — absence ≠ "no blocking script", just no LoAF data.

## When to run

- Standing instrumentation on any production frontend with real users (this is RUM, not a one-shot).
- When `lighthouse-ci` / `bundle-perf` flag LCP/CLS in the lab and you need the field truth + the responsible element.
- When INP is the suspected problem — the ONLY way to measure it is the field.

## Halt conditions

- Halt if INP/LCP is reported without `attribution` (the responsible target + sub-part) — a bare metric value is not a finding.
- Halt if a "passing/failing CWV" claim cites lab data with no CrUX/RUM p75 behind it.
- Halt if per-route (soft-navigation) vitals from `reportSoftNavs` are presented as cross-browser or as CrUX data: they are Chromium 151+ RUM only.
- Halt if the RUM beacon is wired in a way that blocks bfcache (e.g. flushing on `unload`) — use `pagehide`/`visibilitychange` + `sendBeacon`.
