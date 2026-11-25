---
name: seo-core-web-vitals
description: >-
  Use when optimizing LCP, INP, or CLS specifically for SEO in a Lovable SPA:
  PageSpeed/CrUX issues, hero image too heavy, layout shift from web fonts, slow
  interactions on mobile. Not for backend-only perf (use performance-budget).
---

# SEO Core Web Vitals (LCP, INP, CLS)

Core Web Vitals are a Google ranking signal. Each public page must pass on **mobile** (the harder threshold).

| Metric | Good | Poor |
|--------|------|------|
| LCP — Largest Contentful Paint | ≤ 2.5 s | > 4.0 s |
| INP — Interaction to Next Paint | ≤ 200 ms | > 500 ms |
| CLS — Cumulative Layout Shift | ≤ 0.10 | > 0.25 |

Companion skills: [`performance-budget`](../performance-budget/), [`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/), [`dashboard-charts-recharts`](../dashboard-charts-recharts/), [`accessibility-pass`](../accessibility-pass/).

## Measure first

- [PageSpeed Insights](https://pagespeed.web.dev/) — field (CrUX) + lab (Lighthouse).
- Chrome DevTools → Performance → record on mobile throttling.
- `web-vitals` package + your analytics for real-user monitoring.

```ts
import { onLCP, onINP, onCLS } from "web-vitals";
onLCP((m) => track("web_vital", { name: "LCP", value: m.value }));
onINP((m) => track("web_vital", { name: "INP", value: m.value }));
onCLS((m) => track("web_vital", { name: "CLS", value: m.value }));
```

## LCP — biggest fix is the hero image

Almost always: **the hero image is the LCP element on marketing pages.**

- Preload it: `<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">`.
- Use `<img fetchpriority="high" loading="eager" decoding="async">`, never `loading="lazy"`.
- Serve WebP/AVIF; use `srcset` for responsive sizes.
- Explicit `width`/`height` attributes — avoids CLS too.
- Inline critical CSS for the hero region; defer the rest.

```tsx
<img
  src="/hero-960.webp"
  srcSet="/hero-480.webp 480w, /hero-960.webp 960w, /hero-1440.webp 1440w"
  sizes="(max-width: 768px) 100vw, 960px"
  width={960}
  height={540}
  alt="Acme dashboard preview"
  fetchPriority="high"
  decoding="async"
/>
```

Other LCP wins:

- Prerender the public route (`seo-ssr-and-prerendering`) — kills "white screen until JS".
- Use system fonts or `font-display: swap` + preconnect to Google Fonts.
- Avoid client-side fetch for above-the-fold copy; ship as HTML.

## INP — keep the main thread free

Common culprits:

- Heavy JSON parsing on render.
- Mega-renders triggered by uncontrolled state updates.
- Third-party tags (chat widgets, analytics) blocking input.

Fixes:

- **Defer third-party scripts**: `async` or `defer`, load chat widgets after user intent.
- Code-split routes (`React.lazy` + `Suspense`).
- Break large lists with virtualization (`tanstack-infinite-queries`).
- Memoize expensive renders (`useMemo`, `React.memo`) only after profiling.
- Use `startTransition` for non-urgent updates (search filtering, tab switches).

```tsx
const [pending, startTransition] = useTransition();
const onFilter = (v: string) => startTransition(() => setQuery(v));
```

## CLS — reserve space for every dynamic element

- Always set `width`/`height` (or aspect-ratio) on images, video, iframes, ads.
- Web fonts: `font-display: swap` + `size-adjust` or matching fallback metrics.
- Skeleton loaders sized to match real content.
- Avoid injecting banners (cookie, "subscribe!") **above** existing content after load.

```css
@font-face {
  font-family: "Inter";
  src: url(/Inter.woff2) format("woff2");
  font-display: swap;
  size-adjust: 107%; /* match fallback metrics */
}
```

For shadcn projects, the default `next/font` or local font setup typically handles this — verify with Lighthouse.

## Third-party tags audit

Most SPAs ship with: PostHog, GA4, Stripe.js, Sentry, Intercom, Hotjar, Crisp. Each blocks the main thread.

- Load **only on routes that need them** (Stripe.js only on `/checkout`).
- Use Partytown to move analytics to a worker if you can't remove.
- Audit your `<head>`: every `<script>` should justify its bytes.

## Mobile reality check

PageSpeed runs on a throttled 4G mobile. Your dev MacBook is not the customer.

- Test in DevTools with Mobile + Slow 4G + 4× CPU throttling.
- Open the site on a real mid-range Android once per release.

## Avoid

- `loading="lazy"` on the hero image (it's the LCP element, must load immediately).
- Hundreds of `useMemo`/`useCallback` "for safety" — they cost too.
- Hydrating a giant initial state on every route.
- Cookie banners that move all the content down 100 px after 2 seconds.
- Ignoring INP — it replaced FID in 2024 and trips up many SPAs.

## Checklist

- [ ] LCP image preloaded + sized + WebP/AVIF.
- [ ] No `loading="lazy"` on LCP element.
- [ ] Fonts use `font-display: swap`.
- [ ] All images, embeds have explicit dimensions.
- [ ] Third-party scripts deferred or route-scoped.
- [ ] PageSpeed Mobile shows green for LCP, INP, CLS.
