---
name: web-performance
description: Measures and improves web page speed using Core Web Vitals (LCP, INP, CLS) with field and lab data - fixes slow loading, slow interactions and layout shifts, cuts JavaScript, image and font weight, sets caching headers, and adds performance budgets to CI. Use when a site or web app feels slow, Lighthouse or PageSpeed scores are low, Core Web Vitals fail in Search Console or RUM, bundles are too large, or a page is about to launch. Not for backend latency with no frontend symptom.
license: MIT
---

# Web Performance

Measure real users first, fix the metric that is actually failing, and verify with the same measurement. Never optimize by guesswork or by chasing a desktop Lighthouse score on a fast laptop.

## Targets

Core Web Vitals are judged at the **75th percentile** of page loads, separately for mobile and desktop.

| Metric | Measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| LCP (Largest Contentful Paint) | Loading | ≤ 2.5 s | 2.5–4.0 s | > 4.0 s |
| INP (Interaction to Next Paint) | Responsiveness | ≤ 200 ms | 200–500 ms | > 500 ms |
| CLS (Cumulative Layout Shift) | Visual stability | ≤ 0.1 | 0.1–0.25 | > 0.25 |

Diagnostic (not Core Web Vitals): TTFB ≤ 0.8 s and FCP ≤ 1.8 s are considered good.

## Workflow

1. **Get field data.** Use the project's RUM if it has one, then PageSpeed Insights (shows CrUX field data when the site has enough traffic) and the Search Console Core Web Vitals report. If there is no field data, add the `web-vitals` library (below).
2. **Find the worst metric and page template** at p75 on mobile. Work on that first.
3. **Reproduce in the lab** against a production build, never the dev server. Use the Chrome DevTools Performance panel with CPU throttling (4x or more) and network throttling, or Lighthouse (`npx lighthouse https://example.com --view`). A plain Lighthouse page load can't measure INP because nobody interacts; record the slow interaction with the DevTools Performance panel or a Lighthouse timespan, and use Total Blocking Time as a load-time proxy.
4. **Apply the fixes for that metric** (sections below). One change at a time, re-measure after each.
5. **Verify in the field after deploy.** CrUX is a 28-day rolling window, so RUM shows results sooner.
6. **Lock it in** with budgets in CI so it doesn't regress.

### Field measurement with `web-vitals`

```js
import { onCLS, onINP, onLCP } from "web-vitals";

function send(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    id: metric.id,
    page: location.pathname,
  });
  if (!navigator.sendBeacon?.("/analytics/vitals", body)) {
    fetch("/analytics/vitals", { method: "POST", body, keepalive: true });
  }
}

onCLS(send);
onINP(send);
onLCP(send);
```

To learn *why* a metric is slow (which element, which interaction), import from `web-vitals/attribution` and send the attribution fields you need; check the installed version's docs for their names. Aggregate at p75 per page template and device type, not averages.

## Fixing LCP

First find the LCP element (Lighthouse "Largest Contentful Paint element", or the Performance panel). Then break the time into four parts and fix the biggest:

| Part | Typical causes | Fixes |
|---|---|---|
| TTFB | Slow server, no CDN, redirects, uncached HTML | CDN, cache HTML or render at the edge, remove redirect chains, speed up the backend |
| Resource load delay | LCP image found late (CSS background, injected by JS, lazy-loaded) | Put it in the HTML as `<img>`, add `fetchpriority="high"`, preload it if it can't be discovered early |
| Resource load duration | Huge or unoptimized image | Right-size with `srcset`/`sizes`, AVIF or WebP, compress |
| Element render delay | Render-blocking CSS/JS, client-side rendering, web fonts hiding text | Inline critical CSS, `defer` scripts, server-render or pre-render the content, `font-display` |

```html
<img
  src="/img/hero-1200.avif"
  srcset="/img/hero-800.avif 800w, /img/hero-1200.avif 1200w, /img/hero-2000.avif 2000w"
  sizes="100vw"
  width="1200" height="600"
  fetchpriority="high"
  alt="Team reviewing a dashboard">
```

Never put `loading="lazy"` on the LCP image. Lazy-load only below-the-fold images.

## Fixing INP

1. Find the slow interactions: field attribution from `web-vitals/attribution`, or record the interaction in the Performance panel and look at the Interactions track.
2. Split the time into input delay (main thread busy when the user clicked), processing (your handlers) and presentation delay (render and paint after).
3. Fix:
   - **Break up long tasks** (over 50 ms). Do the visible update first and yield before the rest:

     ```js
     function yieldToMain() {
       if (globalThis.scheduler?.yield) return scheduler.yield();
       return new Promise((resolve) => setTimeout(resolve, 0));
     }

     button.addEventListener("click", async () => {
       showSpinner();          // visible feedback first
       await yieldToMain();
       await applyFilters();   // heavier work after the next paint
     });
     ```

   - **Ship less JavaScript**: code split by route, lazy-load heavy components used only after interaction, remove unused dependencies.
   - **Tame third-party scripts** (tag managers, chat widgets, A/B testing): load them with `async`/`defer` or after page load, and remove ones nobody uses.
   - **Avoid layout thrashing**: batch DOM reads before writes; don't read `offsetHeight` in a loop that also writes styles.
   - **Reduce render work**: virtualize long lists, use `content-visibility: auto` for off-screen sections, keep the DOM size reasonable. In React, wrap non-urgent updates in `startTransition`.

## Fixing CLS

- Give every `img`, `video` and `iframe` `width` and `height` attributes, or a CSS `aspect-ratio`.
- Reserve space (`min-height`) for ads, embeds, cookie banners and late-loading components. Prefer overlays for banners instead of pushing content down.
- Don't insert content above existing content unless it is a direct response to a user action (shifts within 500 ms of an input don't count).
- Fonts: preload the one or two critical font files, use `font-display: swap` with metric overrides (`size-adjust`, `ascent-override`) on the fallback, or `font-display: optional`.
- Animate with `transform` and `opacity`, never `top`, `left`, `width` or `height`.

## JavaScript and bundles

| Bundler | Analyzer |
|---|---|
| Vite / Rollup | `rollup-plugin-visualizer` |
| webpack | `webpack-bundle-analyzer` |
| Next.js | `@next/bundle-analyzer` |
| Anything with source maps | `npx source-map-explorer dist/**/*.js` |

Look for: duplicate copies of a library, whole libraries imported for one function, large polyfills for browsers you don't support, locale or icon packs bundled in full, and code for one route shipped on every route. Split with dynamic `import()` and the framework's lazy-loading.

## Caching and delivery

| Asset | `Cache-Control` |
|---|---|
| Fingerprinted files (`app.3f9a1c.js`, `logo.8d2e.svg`) | `public, max-age=31536000, immutable` |
| HTML documents | `no-cache` (revalidate every time), or a short `max-age` with CDN purge on deploy |
| User-specific API responses | `private`, with a `max-age` that fits the data, or `no-store` for sensitive data |

Also: serve over HTTP/2 or HTTP/3 with Brotli or gzip, `preconnect` to the one or two third-party origins needed early, and keep pages eligible for the back/forward cache (avoid `unload` handlers).

## Budgets in CI

Lighthouse CI (`npx @lhci/cli autorun`) with a `lighthouserc.json`:

```json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run start",
      "url": ["http://localhost:3000/"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["warn", { "maxNumericValue": 200 }]
      }
    }
  }
}
```

Add a bundle-size budget too (for example `size-limit`, or the bundler's size warnings) so JavaScript growth fails the PR that causes it.

## Anti-patterns

- **Measuring the dev server** or a fast desktop and calling it done.
- **Optimizing the score instead of the metric**: a 100 in the lab means little if p75 field LCP fails.
- **Lazy-loading everything**, including the hero image.
- **Preloading many resources**: they compete with the LCP resource. Preload only what is critical and discovered late.
- **Averages instead of p75**, or mixing mobile and desktop data.
- **Ignoring third-party scripts**, often the largest share of main-thread time.
- **One-off fixes with no budget**: performance regresses within a few releases.

## Done when

- The failing metric is "good" at p75 in field data for the affected template (or lab shows the fix and field verification is scheduled).
- Each change was measured before and after on a production build with throttling.
- A CI budget covers the metric or bundle size that was fixed.

## References

- [references/checklist.md](references/checklist.md) — read when auditing a whole page or site, or before a launch, for the full checklist by area (server, HTML, images, fonts, JavaScript, CSS, third parties, caching, monitoring).
