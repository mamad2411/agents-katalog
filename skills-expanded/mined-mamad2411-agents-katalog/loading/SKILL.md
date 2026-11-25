---
name: loading
description: Measure and fix loading performance: TTFB, FCP, render-blocking resources, script/font strategy, resource hints, bfcache, SSR hydration, cache headers, and network-aware loading. Use when asked about TTFB, FCP, render-blocking, slow loading, font performance, script optimization, preload/prefetch/preconnect, service workers, save-data, or slow 2g/3g connections.
license: MIT
metadata:
  author: ult-performance
  version: "1.0.0"
  mcp-server: chrome-devtools
  category: web-performance
---

# Loading performance

Read [execute-snippets.md](../../references/execute-snippets.md) and [schema.md](../../references/schema.md) before evaluating scripts.

## Scripts

**Document timing**
- `scripts/TTFB.js`
- `scripts/TTFB-Sub-Parts.js`
- `scripts/TTFB-Resources.js`
- `scripts/FCP.js`
- `scripts/Event-Processing-Time.js`

**Blocking and CSS**
- `scripts/Find-render-blocking-resources.js`
- `scripts/Critical-CSS-Detection.js`
- `scripts/Inline-CSS-Info-and-Size.js`
- `scripts/CSS-Media-Queries-Analysis.js`
- `scripts/Content-Visibility.js`

**Scripts**
- `scripts/Script-Loading.js`
- `scripts/Validate-Preload-Async-Defer-Scripts.js`
- `scripts/First-And-Third-Party-Script-Info.js`
- `scripts/First-And-Third-Party-Script-Timings.js`
- `scripts/JS-Execution-Time-Breakdown.js`
- `scripts/Inline-Script-Info-and-Size.js`
- `scripts/SSR-Hydration-Data-Analysis.js`

**Hints, fonts, images in the critical path**
- `scripts/Resource-Hints.js`
- `scripts/Resource-Hints-Validation.js`
- `scripts/Prefetch-Resource-Validation.js`
- `scripts/Priority-Hints-Audit.js`
- `scripts/Fonts-Preloaded-Loaded-and-used-above-the-fold.js`
- `scripts/Find-Above-The-Fold-Lazy-Loaded-Images.js`
- `scripts/Find-Images-With-Lazy-and-Fetchpriority.js`
- `scripts/Find-non-Lazy-Loaded-Images-outside-of-the-viewport.js`

**Cache / navigation**
- `scripts/Cache-Strategy-Analysis.js`
- `scripts/Service-Worker-Analysis.js`
- `scripts/Back-Forward-Cache.js`
- `scripts/Client-Side-Redirect-Detection.js`

**Network**
- `scripts/Network-Bandwidth-Connection-Quality.js`

## Workflows

### Complete loading audit

1. `TTFB.js` → `FCP.js` → `Find-render-blocking-resources.js`
2. `Critical-CSS-Detection.js` → `Script-Loading.js` → `Resource-Hints-Validation.js`

### Slow TTFB

1. `TTFB.js` → `TTFB-Sub-Parts.js` (DNS / connect / SSL / server)
2. `Service-Worker-Analysis.js` if a worker is present
3. `TTFB-Resources.js` for slow third-party/API origins

### Fonts

1. `Fonts-Preloaded-Loaded-and-used-above-the-fold.js`
2. `Resource-Hints-Validation.js`
3. `Find-render-blocking-resources.js`

### Scripts

1. `Script-Loading.js`
2. `First-And-Third-Party-Script-Info.js` + timings
3. `JS-Execution-Time-Breakdown.js`
4. `Validate-Preload-Async-Defer-Scripts.js`

### Slow connection / save-data

1. `Network-Bandwidth-Connection-Quality.js`
2. Follow [network.md](references/network.md)

## Decision tree

- TTFB > 600ms → `TTFB-Sub-Parts.js`
- FCP > 1.8s → render-blocking + critical CSS + Script-Loading
- Blocking stylesheets → Critical-CSS-Detection
- Blocking scripts → Script-Loading + Validate-Preload-Async-Defer-Scripts
- Unused preloads → remove; missing LCP/font preloads → Priority-Hints-Audit / Fonts snippet
- SW overhead > 100ms → Navigation Preload
- Fonts preloaded but unused ATF → drop preload; used but not preloaded → add
- Third-party scripts > 5 → timings + JS execution breakdown
- Hydration data > 100KB → reduce serialized state
- LCP image without `fetchpriority="high"` → add it; do not also lazy-load it
- Prefetch > 10 hints or > 2MB → cut
- Render-blocking CSS > 14KB → inline critical CSS
- Client-side redirects → move to the server
- `effectiveType` 2g/slow-2g or `saveData` → [network.md](references/network.md)

When LCP is the complaint, load `core-web-vitals` after the loading diagnosis. Image-only issues → `media`. Main-thread blocking during load → `interaction`.

## Fix pointers

Code-level loading, caching, Early Hints, Speculation Rules: `performance` skill.

Snippet descriptions: [snippets.md](references/snippets.md)
