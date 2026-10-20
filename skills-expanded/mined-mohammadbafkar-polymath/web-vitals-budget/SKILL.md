---
name: web-vitals-budget
description: Set Core Web Vitals budgets (LCP, INP, CLS) per route and propose the cheapest fix path when one is over budget. Web routes only; not mobile (mobile-perf) or backend (perf-budget).
---

# web-vitals-budget

> Pin budgets for LCP, INP, and CLS per route; if a route is over budget, propose the highest-leverage fix.

## When to use

- A new route ships; we need a target.
- An existing route regresses on a Web Vital.
- The user says "improve performance" without a specific lever.

## Inputs

- Route / page identifier.
- Current measured values (CrUX, RUM, or local Lighthouse — say which).
- Audience tier: `high-end-desktop`, `median-mobile`, `low-end-mobile`.

## Targets (good = 75th percentile of users)

| Metric | Good | Needs improvement | Poor |
| ------ | ---- | ----------------- | ---- |
| LCP    | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP    | ≤ 200ms | 200–500ms | > 500ms |
| CLS    | ≤ 0.1 | 0.1–0.25 | > 0.25 |

Set the budget to "good" unless the route has explicit reason otherwise (e.g. a deliberately heavy media gallery). Document that reason inline.

## Procedure

1. Read or measure each metric for the route.
2. For each metric, classify (good / needs improvement / poor).
3. For each metric in needs-improvement or poor, identify the **dominant cost**:
   - **LCP** — most often the LCP element's network path. Look at: largest contentful element (image / hero text), how it is fetched (`<img>` vs CSS background, `loading=lazy` mistakenly), critical request count before it, render-blocking CSS.
   - **INP** — long tasks blocking the next paint after input. Look at: hydration costs on first interaction, oversized event handlers, unbatched state updates, library responsible.
   - **CLS** — unsized images / iframes / late-loading fonts / ads / dynamic content injection above the viewport.
4. Recommend exactly **one** fix to try first. The cheapest path that moves the metric materially.

## Output

```text
Web Vitals budget: <route>

Audience: median-mobile

           Current   Budget    Status
LCP        3.1 s     2.5 s     needs improvement
INP        180 ms    200 ms    good
CLS        0.03      0.1       good

Dominant cost (LCP):
  Hero image fetched after critical CSS (image is in /img/hero.jpg, 
  220 KB JPEG, no priority hint).

First-try fix:
  Add fetchpriority="high" to the hero <img>; preload via <link rel="preload">.
  Estimated LCP gain: 600–900 ms (based on current critical path).
```

## Anti-patterns to avoid

- "Improve all three at once" — pick the biggest gap.
- Synthetic tests as the only signal; CrUX/RUM beats Lighthouse for the budget number.
- Recommending CDN/HTTP3/etc when the problem is a 600 KB hero image.
