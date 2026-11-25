---
name: optimize-core-web-vitals
description: Diagnoses and fixes Core Web Vitals (LCP, INP, CLS) and Lighthouse failures via image/font/JS strategy in the browser; used when pages are slow, janky, or failing a Lighthouse/PageSpeed audit.
when_to_use: When the user reports slow page load, layout shift, sluggish interactions, poor Lighthouse/PageSpeed scores, or asks to improve LCP/INP/CLS or Core Web Vitals — frontend/browser-side specifically. Not for backend/server query latency (that is performance-profiling).
---

## When to Use

Use when a page is slow to render, shifts layout, or feels laggy on interaction — and the fix lives in the browser (HTML/CSS/JS/assets), not the server query path.

| Symptom | Metric | This skill |
|---|---|---|
| Hero/main content paints late | LCP | yes |
| Content jumps after load | CLS | yes |
| Click/typing feels frozen | INP | yes |
| Lighthouse/PageSpeed score red | all | yes |
| API/DB response is the bottleneck | TTFB-backend | no → backend profiling |

Targets (pass = 75th percentile): **LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1**. TTFB ≤ 800ms is a precondition for LCP — if TTFB alone blows the budget, stop and route to backend.

## Steps

**1. Baseline before touching anything.** Run a trace + audit on the real URL so you have a before/after diff.
- `chrome-devtools.performance_start_trace` (with `reload: true`, `autoStop: true`) → load → `performance_stop_trace`.
- Or `chrome-devtools.lighthouse_audit` (categories `["performance"]`, mobile preset — mobile is what fails first).
- Run `performance_analyze_insight` on the flagged insights (e.g. `LCPBreakdown`, `RenderBlocking`, `CLSCulprits`, `DocumentLatency`). Record the LCP element, INP target, CLS shifters, and TTFB. **Do not guess which image/script is the problem — read it from the trace.**

**2. Identify the LCP element and attack its critical path.** LCP = TTFB + resource load delay + load time + render delay. Fix the dominant segment:
- LCP is an image → add `fetchpriority="high"` to that one `<img>`, and `<link rel="preload" as="image" fetchpriority="high" imagesrcset=...>` in `<head>`. Remove `loading="lazy"` from it (lazy on the LCP image is a top regression).
- Serve modern formats: AVIF then WebP fallback via `<picture>`; provide `srcset`/`sizes` so mobile downloads a small file, not the desktop original.
- LCP is text → preload the font (step 4) and remove render-blocking CSS/JS in front of it.

**3. Kill render-blocking resources.** From the `RenderBlocking` insight:
- Inline critical above-the-fold CSS; load the rest with `media` swap or async. Defer non-critical CSS.
- Add `defer` (or `type="module"`) to scripts; never `async` a script that the first paint depends on ordering-wise.
- Remove third-party/analytics tags from the critical path — load them after `load` or via `requestIdleCallback`.
- Self-host or `preconnect` to required cross-origin asset domains.

**4. Eliminate CLS — reserve space for everything that arrives late.**
- Every `<img>`/`<video>`/`<iframe>` gets explicit `width`+`height` (or CSS `aspect-ratio`) so the box is reserved before the asset loads.
- Fonts: `font-display: swap` + `<link rel="preload" as="font" type="font/woff2" crossorigin>` for the primary font; set `size-adjust`/`ascent-override` (or a matched fallback metric) to minimize the swap reflow.
- Ads/embeds/dynamic banners: reserve a min-height container. Never inject DOM above existing content without space already held.
- Avoid animating layout properties (top/left/height); use `transform`/`opacity`.

**5. Fix INP — the slowest interaction, not just the first.** From the trace's interaction/long-task data:
- Break long tasks (>50ms) with `scheduler.yield()` or chunked work; move heavy compute to a Web Worker.
- `debounce`/`throttle` input handlers; isolate expensive work out of the event handler's synchronous path.
- Reduce hydration cost: ship less JS to the client, use islands/partial hydration or server components so interactive regions hydrate independently instead of one giant blocking bundle.
- Avoid forced synchronous layout (reading `offsetWidth`/`getBoundingClientRect` then writing styles in a loop — batch reads then writes).

**6. Cut the JS budget.** Check `list_network_requests` for the heaviest scripts:
- Code-split by route; dynamic-`import()` below-the-fold and on-interaction components (modals, carousels, charts).
- Tree-shake; drop unused polyfills and duplicate library copies (check for two versions of the same dep in the bundle).
- `loading="lazy"` + `IntersectionObserver` for below-fold images/iframes (but NOT the LCP element — see step 2).

**7. Re-run the audit and diff.** Repeat step 1 on the same URL/preset. Compare LCP/INP/CLS numbers before vs after. Iterate until all three pass the target or the remaining gap is backend TTFB.

## Common Errors

- **Lazy-loading the LCP image.** `loading="lazy"` on the hero delays the very thing LCP measures. Lazy is for below-fold only.
- **Trusting lab CLS = 0.** Lab loads fast and may not trigger font swap or late ads. Reproduce by throttling network/CPU in the trace, or check field data — most CLS comes from late-arriving fonts/ads/images, not the initial paint.
- **`fetchpriority="high"` on everything.** Priority is relative; flag one LCP resource. Marking many demotes the signal to noise.
- **`preload` without using it.** A preloaded font/image not referenced within a few seconds throws a console warning and wastes bandwidth. Preload only the LCP image and the first-paint font.
- **Preloading a font without `crossorigin`.** Fonts are CORS-fetched; a `preload` missing `crossorigin` double-downloads the file.
- **Optimizing the first interaction only.** INP is the worst interaction across the session. Test scrolling, opening menus, typing — not just the initial click.
- **Desktop-only testing.** CWV failures are mobile-first (slow CPU, slow network). Always audit with the mobile preset and CPU/network throttling.
- **Counting bytes saved, not metric moved.** "Saved 200KB" means nothing if it wasn't on the critical path. Verify the metric number changed, not the asset size.

## Verify

1. Re-run `lighthouse_audit` (mobile) **and** a `performance_start_trace`/`stop_trace` on the same URL as the baseline.
2. Confirm: **LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1** — quote the actual before→after numbers, not "improved".
3. `list_console_messages` shows no new preload/warning errors and no unused-preload warnings.
4. `list_network_requests` confirms LCP image is high priority + modern format, fonts are preloaded, and no surprise render-blocking script returned.
5. If a target still fails and the remaining cost is TTFB/server, say so explicitly and route to backend — do not claim a browser-side fix that isn't there.
