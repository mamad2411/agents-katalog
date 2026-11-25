---
name: performance
description: The team's authoritative performance standard for Shopify Dawn-fork themes — lazy-loading (the golden rule), Core Web Vitals (LCP/CLS/INP), image optimization (image_url/widths/sizes), critical rendering path, JS/CSS optimization, bundle size, and third-party script cost. Use this skill whenever building or editing anything that ships images, scripts, iframes/embeds, fonts, or sliders, and whenever the user mentions performance, Lighthouse, PageSpeed, Core Web Vitals, LCP, CLS, slow pages, or layout shift. BUILD-TIME guidance so sections arrive fast; the qa agent runs the actual Lighthouse audit against this same file.
---

# Performance Standard (Shopify Dawn-fork)

Single source of truth for performance. Build against it; the `qa` agent verifies against it with Lighthouse.

## Golden rule of lazy loading

- **Never lazy-load the hero/first visible image** — `loading: 'eager'` + `fetchpriority: 'high'` (it's the LCP element).
- Everything below the fold: `loading: 'lazy'` (images, iframes, videos).
- Unsure if above fold? Default lazy + eager first image, note the call. Sections that can sit anywhere: add a `first_section` schema checkbox so the merchant decides.

## Images (also enforced in the shopify-liquid build)

- Always `image_url` with an explicit `width:` — never raw `| img_url` or unparameterized URLs.
- Always include `widths` + `sizes`:
  `{{ image | image_url: width: 1500 | image_tag: widths: '375, 550, 750, 1100, 1500', sizes: sizes, loading: 'lazy' }}`
- `loading`/`fetchpriority` values must be **quoted strings** in Liquid filters — bare `lazy`/`eager`/`high` resolve to nil and silently drop the attribute.
- `image_tag` emits `width`/`height` — keep them; reserving dimensions is non-negotiable CLS prevention.
- Never feed a 4000px source into a 600px slot. CSS background images can't lazy-load — use real `<img>` for content images.

## CLS (layout stability)

- Every image, embed, and slider reserves its space before it loads/initialises. A slider that pops to full height on init is a CLS defect — reserve the height in CSS.
- Fonts: above-the-fold text fonts preloaded (WOFF2), `font-display: swap`. Watch for the swap causing reflow.
- App blocks and injected content that push layout are flagged (often outside theme control — note, don't necessarily block).

## Critical rendering path & JS

- All custom scripts load with `defer` (`custom.js` already does). No render-blocking custom JS or CSS in `<head>`.
- No `@import` in CSS; `{% stylesheet %}` blocks stay minimal and scoped.
- Iframes always `loading="lazy"`. YouTube/Vimeo via a **facade** (poster + play button that injects the iframe on click) — never a direct embed on load. This is already implemented correctly in `sections/video.liquid` (deferred `<template>` + poster button) — match that pattern, don't reinvent it per new video section.
- Liquid efficiency: `{% assign %}` once instead of recomputing in loops; limit `paginate`/product loops to what the section renders.

## Watch for duplicate-section drift

Before building a near-duplicate of an existing section (a second hero variant, a second video section), check whether one already exists — `sections/custom-hero.liquid` and `sections/custom-hero-new.liquid` both currently ship, both live in `templates/index.json`, and each independently implements its own eager-image/`fetchpriority` LCP logic. Two parallel implementations of the same performance-sensitive pattern drift out of sync silently — a fix applied to one won't reach the other. Prefer extending the existing section (a setting/variant) over creating a second one; if a second file is genuinely required, note in the brief that the LCP/eager-loading logic must be kept in sync with the original.

## Bundle size & third-party

- No asset file over ~500KB uncompressed in `assets/` (excluding Dawn's own). No unused CSS/vars, no unreachable JS, no commented-out code shipping to production.
- No external JS libraries unless bundle cost is justified and recorded in the brief. Carousels use Swiper 11 (already a dependency) — don't add a second slider lib.
- Inventory third-party/app scripts touching a section for awareness; their cost is outside theme control and generally a warning, not a build failure.

## Invisible-fix rule

Performance fixes must never change visuals or behaviour. Global wins (preload, preconnect, `font-display`) are `theme.liquid`-level work — flag them, don't apply them from inside a section.

## Lighthouse verification (used by the qa agent)

Run against the local dev server when it's up; mobile first:

```bash
npx lighthouse http://127.0.0.1:9292/<path> --preset=perf --form-factor=mobile \
  --only-categories=performance --quiet --chrome-flags="--headless"
```

Capture Performance score, LCP, CLS, TBT/INP. If a section isn't in a template yet, place it temporarily to measure. If the dev server is down, audit statically and record the skip with its reason — never silently skip. When talking to a client about live numbers, note that CrUX field data is a 28-day rolling window, so deployed fixes take weeks to show; separate lab (immediate) from field (lagging).

## What counts as a blocker (for the qa gate)

High-impact violations in the section's OWN code: lazy-loaded LCP image, missing reserved dimensions (observed CLS), render-blocking custom script, unreserved slider height, oversized payload. Medium/low findings and anything outside the section's control (apps, global theme files) are warnings.
