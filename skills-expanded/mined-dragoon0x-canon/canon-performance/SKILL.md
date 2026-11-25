---
name: canon-performance
description: Use when designing or auditing front-end performance, Core Web Vitals (LCP, INP, CLS), bundle size, image optimization, font loading, lazy loading, or perceived speed. Trigger when the user mentions performance, slow, fast, bundle, Core Web Vitals, LCP, INP, CLS, lazy load, or perceived speed.
---

# CANON · Performance

Performance is design. A slow interface fails accessibility, fails conversion, and fails users on slow networks. The targets below are the bar.

## Core Web Vitals (the only metrics that matter for ranking and UX)

| Metric | Good | Needs Improvement | Poor | Source |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5–4.0s | > 4.0s | web.dev |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms | web.dev |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 | web.dev |

**Targets are 75th-percentile across mobile devices on slow 4G.** "Works on my MacBook" is irrelevant.

### TTFB (Time to First Byte) — the prerequisite

| Threshold | Status |
|---|---|
| ≤ 800ms | Good |
| > 1.8s | Poor (LCP cannot be good with this TTFB) |

Bad TTFB ceilings everything else. Fix server response and CDN before anything else.

## LCP — Largest Contentful Paint

Most LCP failures come from one of:
1. Large unoptimized hero image
2. Render-blocking CSS / JS
3. Slow server (TTFB)
4. Web fonts that delay text paint

### Hero Image Rules

```html
<img
  src="hero-1200.webp"
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
  sizes="100vw"
  fetchpriority="high"
  decoding="async"
  width="1200"
  height="600"
  alt="..."
/>
```

| Attribute | Why |
|---|---|
| `fetchpriority="high"` | Tells browser this is the LCP candidate |
| `srcset` + `sizes` | Right size per viewport |
| `width` + `height` | Reserves space (prevents CLS) |
| Format: WebP/AVIF | 25–50% smaller than JPEG |
| `loading="lazy"` | **NEVER for the LCP image.** Lazy = late paint. |

### Render-Blocking Resources

Only load critical CSS in `<head>`. Defer everything else.

```html
<!-- Critical CSS inline -->
<style>/* above-the-fold styles only */</style>

<!-- Non-critical CSS deferred -->
<link rel="preload" href="/styles/full.css" as="style" onload="this.rel='stylesheet'">

<!-- Scripts deferred -->
<script src="/main.js" defer></script>
<script src="/analytics.js" async></script>
```

| Strategy | When |
|---|---|
| Inline critical CSS | Above-the-fold styles in `<head>` |
| `defer` | Scripts that can run after parse |
| `async` | Independent scripts (analytics, ads) |
| `module` | ES modules (defers by default) |

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
```

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;  /* show fallback immediately, swap when font loads */
}
```

| Strategy | Effect |
|---|---|
| `preconnect` | Earlier handshake to font CDN |
| `font-display: swap` | Text visible immediately with fallback |
| Variable fonts | One file replaces 3–9 |
| Self-host critical fonts | Avoid third-party CDN latency |
| Subset fonts | Drop unused glyphs |

## INP — Interaction to Next Paint

INP measures the worst interaction during the user's session. One slow click ruins your INP.

### Common INP Killers

| Cause | Fix |
|---|---|
| Heavy synchronous JS (e.g., parsing 10MB JSON on click) | Move to `requestIdleCallback` or Web Worker |
| Long tasks (>50ms) on main thread | Break into chunks with `setTimeout(fn, 0)` |
| Hydration of client components on interaction | Use `<Suspense>`, server components, islands |
| Re-rendering large React tree on small state change | Memoize, virtualize lists |

### INP Targets per Interaction Type

| Interaction | Target |
|---|---|
| Tap, click, key press | ≤ 100ms perceived response |
| Form input → next paint | ≤ 50ms |
| Heavy operation acknowledgment | Spinner appears within 100ms |

**Rule: every interaction must show acknowledgement within 100ms, even if the actual operation takes longer.**

## CLS — Cumulative Layout Shift

CLS happens when content moves after first paint. Every shift hurts.

### Common CLS Causes

| Cause | Fix |
|---|---|
| Images without `width`/`height` | Always set both |
| Fonts loading and reflowing text | `font-display: swap` + `size-adjust` |
| Ads / iframes without reserved space | Reserve container |
| Dynamic content injected above existing | Reserve via `min-height` or insert below |
| `transform`-based animations | Don't cause CLS (good) |

### Reserve Space for Everything

```css
/* Image: width and height attributes do this in HTML */

/* Iframe: explicit dimensions */
.video-embed {
  aspect-ratio: 16 / 9;
  width: 100%;
}

/* Skeleton matches final size */
.card-skeleton {
  height: 240px;  /* matches loaded card */
}

/* Web font fallback adjusts to match metrics */
@font-face {
  font-family: 'Inter';
  src: url('...') format('woff2');
  size-adjust: 100%;     /* match fallback metrics */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

## Bundle Size

| Type | Target |
|---|---|
| Critical JS (blocking) | < 100KB compressed |
| Total JS first load | < 200KB compressed |
| Critical CSS | < 50KB compressed |
| LCP image | < 200KB |
| Total page weight | < 1MB on 75p mobile |

### Bundle Diet Strategies

1. **Tree-shake.** Use ES modules. Avoid `import * as X`.
2. **Code-split** by route. Don't ship the admin bundle to the marketing page.
3. **Lazy-load** below-the-fold components and below-the-fold images.
4. **Audit** with `webpack-bundle-analyzer` or `rollup-plugin-visualizer`. Find the bloat.
5. **Replace heavy libraries.** Moment.js (290KB) → date-fns (modular) or `Intl.DateTimeFormat` (0KB).
6. **Use platform features.** `Intl`, `Intl.NumberFormat`, native `dialog`, native lazy-loading. Saves vs polyfills.

## Image Optimization

| Format | Use |
|---|---|
| **AVIF** | Modern, best compression. Use when supported. |
| **WebP** | Wide support, good compression. Default. |
| **JPEG** | Photos, fallback for AVIF/WebP |
| **PNG** | Transparency, screenshots with text |
| **SVG** | Icons, logos, illustrations |

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="..." width="800" height="600">
</picture>
```

### Image Sizing Rules

- Never serve a 4000px image to a 400px viewport. Use `srcset`.
- Compress aggressively. JPEG quality 75–80 is usually indistinguishable from 100.
- SVG icons: inline if used once, sprite if reused.
- Decorative images: empty `alt=""`. Don't lazy-load above-the-fold or LCP candidates.

## Lazy Loading

```html
<img src="..." loading="lazy" decoding="async" width="800" height="600" alt="...">
<iframe src="..." loading="lazy" width="..." height="..."></iframe>
```

| Don't lazy-load | Do lazy-load |
|---|---|
| LCP image | Below-the-fold images |
| Above-the-fold images | Comments section |
| Critical CSS | Heavy widgets (maps, video players) |

## Caching Strategy

```
Cache-Control: public, max-age=31536000, immutable    /* fingerprinted assets */
Cache-Control: public, max-age=0, must-revalidate     /* HTML */
Cache-Control: private, max-age=300                    /* user data */
```

Fingerprint static assets (`/main.abc123.js`) so they can be cached forever. HTML revalidates so updates ship immediately.

## Perceived Performance

Even when actual time is fixed, perceived time can shrink:

| Trick | Effect |
|---|---|
| Skeleton screens | -20% perceived wait |
| Optimistic UI updates | Action feels instant |
| Show acknowledgement < 100ms | Feels responsive |
| Defer non-critical animations until after LCP | Faster paint |
| Preload next-route resources on hover | Click feels instant |

```html
<!-- Preload on hover -->
<link rel="prefetch" href="/next-page" as="document">
```

## Anti-Patterns

| Anti-pattern | Impact | Fix |
|---|---|---|
| `loading="lazy"` on hero image | Slow LCP | Remove; use `fetchpriority="high"` |
| Image without `width`/`height` | High CLS | Always set both |
| `font-display: block` (default) | FOIT, slow text paint | Use `swap` |
| Render-blocking JS in `<head>` | Slow LCP | Use `defer` or `async` |
| Inline `<script>` in `<head>` doing work | Slow paint | Defer to end of body |
| Loading 5 weight variants of one font | Slow font load | Use variable fonts |
| 4MB hero JPG | Slow LCP, blown bandwidth | Compress to < 200KB, use WebP/AVIF |
| Auto-playing background video | Battery, bandwidth | Use static image or short loop |
| Loading entire JS framework for marketing site | 200KB+ overhead | Use HTML/CSS/light JS for marketing |
| Re-rendering on every keystroke (uncontrolled debounce) | Bad INP | Debounce or use `useDeferredValue` |
| Long tasks (>50ms) on main thread | Bad INP | Break into chunks |
| `setInterval` running every 100ms | Battery drain | `requestAnimationFrame` or longer interval |
| Sub-pixel rendering with `transform: translate(0.5px)` | Forces compositor work | Round to whole pixels |

## Decision Tree

```
Building a page?
├─ Hero image: fetchpriority=high, no lazy, WebP, srcset, dimensions set
├─ Fonts: preconnect, font-display: swap, variable if possible
├─ Critical CSS: inline in <head>, < 50KB
├─ Scripts: defer or async, < 200KB total
├─ Below-fold images: loading=lazy, dimensions set
└─ Cache: fingerprint static assets, max-age=31536000
```

## Audit Checklist

1. Run **PageSpeed Insights** on production. Mobile score >= 90?
2. Check LCP <= 2.5s, INP <= 200ms, CLS <= 0.1.
3. Find the LCP element. Has `fetchpriority="high"`? No `loading="lazy"`?
4. Check every image has `width` and `height` attributes.
5. Check fonts. `font-display: swap`? Variable fonts where possible?
6. Run a bundle analyzer. JS first load < 200KB compressed?
7. Search for `loading="lazy"` on above-the-fold images. Remove.
8. Search for `<script>` in `<head>` without `defer` or `async`. Fix.
9. Open DevTools Performance panel. Long tasks > 50ms? Break up.
10. Check cache headers. Static assets immutable? HTML revalidating?

## Citations

- Core Web Vitals: https://web.dev/vitals/
- LCP guide: https://web.dev/lcp/
- INP guide: https://web.dev/inp/
- CLS guide: https://web.dev/cls/
- Optimize fonts: https://web.dev/font-best-practices/
- Optimize images: https://web.dev/fast/#optimize-your-images
- HTTP Archive Web Almanac: https://almanac.httparchive.org
- PageSpeed Insights: https://pagespeed.web.dev
