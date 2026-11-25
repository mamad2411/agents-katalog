---
name: core-web-vitals
description: "Core Web Vitals (LCP, INP, CLS) optimization using field and lab data. Use when asked to improve page experience, fix LCP, reduce CLS or optimize INP."
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
---

# Core Web Vitals

Optimize LCP, INP and CLS by using field data to find user impact and browser traces to find causes.

| Metric | Measures | Good | Needs work | Poor |
|---|---|---|---|---|
| LCP | Loading | <= 2.5s | 2.5s to 4s | > 4s |
| INP | Interactivity | <= 200ms | 200ms to 500ms | > 500ms |
| CLS | Visual stability | <= 0.1 | 0.1 to 0.25 | > 0.25 |

Google judges the 75th percentile: 75% of page visits must be Good.

## Measure before optimizing

1. Read page-level CrUX p75; fall back to origin-level data and label it as such.
2. Record a browser performance trace under stated conditions (Chrome DevTools MCP: `performance_start_trace`, which can include CrUX beside lab metrics).
3. Analyze only the insights tied to the failing metric, then inspect the implicated code and resources.
4. Re-run an equivalent lab measurement after the fix. Report lab results as lab results; CrUX and first-party RUM need new user visits before field numbers move.

With source code only, name likely causes and mark the metric `Not verified`, since failing status needs runtime evidence.

| Source | Use |
|---|---|
| Performance trace | One load or interaction, focused insights |
| CrUX / Search Console | Aggregated real-user p75, for prioritizing |
| Lighthouse CLI / PageSpeed Insights | Controlled lab fallback |
| First-party RUM (`web-vitals` library) | Production segmented by route, device, release, attribution |
| Raw `PerformanceObserver` | Debugging one session |

Chrome DevTools MCP's `lighthouse_audit` deliberately excludes performance, so use a trace for it. A single lab value and a field p75 are different samples, so compare them only as such. For production collection, use the `web-vitals` library because raw browser APIs do not implement every metric's lifecycle and reporting rules.

## LCP

The LCP element is usually a hero image or video, large text block, background image or `<svg>`. Time splits into TTFB, resource load delay and duration, and render delay; attack the largest part in the trace.
- TTFB above 800ms: CDN, caching, edge rendering.
- Make the LCP resource discoverable in the initial HTML: an `<img>` with `fetchpriority="high"`, not a CSS background. Preload only when the trace shows late discovery.
- Server-render the LCP content; skip JS-fetched hero text.
- Inline critical CSS (under 14KB), keep render-blocking JS out of `<head>`, use `font-display: swap`, serve right-sized WebP/AVIF.

Prerendering the next page via Speculation Rules is a separate navigation optimization: [references/speculation-rules.md](references/speculation-rules.md). Detailed LCP work (discovery, loading, render delay): [references/LCP.md](references/LCP.md).

## INP

INP covers clicks, taps and key presses across the visit. Diagnose input delay, processing time and presentation delay separately: main-thread contention before the handler, expensive handler work, or slow rendering after it. When field INP is poor or a trace shows a slow interaction, read [references/INP.md](references/INP.md) (trace interpretation, yielding patterns, third-party causes, observer, attribution).

## CLS

CLS sums unexpected layout shifts across the visit. Find the shifted node and its trigger from field attribution or a trace; the visible victim is often not the cause. When field CLS is poor or a trace reports shifts, read [references/CLS.md](references/CLS.md) (reserved space, dynamic content, fonts, animation, observer, checklist).

## Framework fixes

Next.js `priority` on the hero `next/image`, `dynamic()` for heavy components, `useTransition` for expensive React updates, explicit dimensions or `aspect-ratio` on media. Snippets for Next.js, React, Vue/Nuxt, the common LCP causes and an LCP element observer: [references/framework-fixes.md](references/framework-fixes.md).

Docs: [LCP](https://web.dev/articles/lcp), [INP](https://web.dev/articles/inp), [CLS](https://web.dev/articles/cls).
