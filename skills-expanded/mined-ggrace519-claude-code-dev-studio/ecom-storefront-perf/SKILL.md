---
name: ecom-storefront-perf
description: Storefront performance specialist. Owns Core Web Vitals, edge caching, rendering strategy (SSR / ISR / SSG / streaming), image optimization, and third-party script discipline. Auto-invoked for storefront perf regressions, LCP/CLS/INP issues, or rendering strategy decisions.
---

# E-commerce Storefront Performance

Every 100ms of load time costs conversions, and Core Web Vitals feed Google
ranking — storefront performance is a direct P&L input, not a vanity metric.

## When to reach for this

- Choosing a rendering strategy (SSR / ISR / SSG / streaming / islands) per route
- Diagnosing an LCP, CLS, or INP regression or failing CWV assessment
- Setting up edge caching and invalidation for PDPs and category pages
- Auditing image pipeline or third-party script weight

## Principles

1. **Budget first.** Set per-page-type targets before touching code. The CWV
   "good" thresholds at p75 of real users: **LCP ≤ 2.5s, INP ≤ 200ms,
   CLS ≤ 0.1** — budget tighter than that internally so a regression still
   passes the assessment.
2. **Edge everything cacheable.** PDPs and category pages render at the edge
   with event-driven purge (price/stock change → targeted invalidation);
   personalize and show live stock by deferred client fetch or edge middleware,
   never by making the whole page uncacheable.
3. **Critical-path discipline.** The LCP element (usually the hero/product
   image) gets `fetchpriority="high"`, no lazy-loading, and preconnect to its
   CDN host; everything below the fold is `loading="lazy"`. One misplaced
   `loading="lazy"` on the hero is the most common self-inflicted LCP failure.
4. **Images do the heavy lifting.** AVIF/WebP with fallback, responsive
   `srcset` + accurate `sizes`, explicit width/height (or `aspect-ratio`) on
   every image — that last one is most of CLS prevention.
5. **Third-party scripts are liabilities.** Each tag has an owner, a measured
   cost, and a load tier (blocking is reserved for consent/anti-fraud; tags
   default to deferred or post-interaction). Audit quarterly; delete orphans.
6. **RUM is truth, synthetic is the guard.** Lighthouse/lab catches regressions
   in CI; field data (CrUX / your RUM) decides whether you actually pass. Alert
   on p75 field metrics per page type.

## Rendering strategy by page type

| Page type | Default strategy | Cache / revalidate | Notes |
|---|---|---|---|
| Home / landing | SSG or ISR | minutes–hours, purge on publish | rarely needs request-time data |
| Category / PLC | ISR or edge-cached SSR | short TTL + purge on merch change | facets via client or edge query |
| PDP | ISR + client islands | purge on price/stock event | price/stock badge hydrates live |
| Search results | SSR (or client on cached shell) | no full-page cache | latency budget shared with engine |
| Cart / checkout | SSR/CSR, uncached | none | correctness > cache; keep JS lean — INP risk |
| Account / order | SSR, uncached, private | none | `Cache-Control: private, no-store` |

## Pitfalls

- Lazy-loading the LCP image, or LCP image served full-size and downscaled by CSS
- Cookie-/session-varying headers silently making every page a CDN miss
- Consent banners and A/B-test scripts injected blocking in `<head>`, shifting layout
- Fonts without `font-display: swap` + preload — invisible text and CLS
- Cache purge wired to deploys but not to price/stock/content events (stale prices at the edge)
- Optimizing the lab score while p75 field INP fails on mid-tier Android

---
*Related: `ecom-search-merch` (search latency inside the page budget),
`ecom-inventory` (live stock badges vs cacheability) · domain agent:
`ecom-architect` (storefront topology, CDN choice) · output/ADR format:
`playbook-conventions`*
