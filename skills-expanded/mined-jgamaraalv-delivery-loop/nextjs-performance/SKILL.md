---
name: nextjs-performance
description: Next.js performance optimization for Core Web Vitals, image/font optimization, caching, streaming, bundle size, and Server Components. Use when fixing LCP/INP/CLS, implementing next/image or next/font, configuring unstable_cache, converting Client to Server Components, streaming with Suspense, or reducing bundle size. Covers Next.js 16 + React 19 patterns.
---

# Next.js Performance Optimization

## Before Starting

1. **Analyze current performance** with Lighthouse
2. **Identify bottlenecks** - check Core Web Vitals in Chrome DevTools or PageSpeed Insights
3. **Determine optimization priority**:
   - LCP issues → Focus on images, fonts
   - INP issues → Reduce JS, use Server Components
   - CLS issues → Add dimensions, use next/font

## Core Principles

1. **Prefer Server Components** - Only use 'use client' when necessary (browser APIs, interactivity)
2. **Load components as low as possible** - Keep Client Components at leaf nodes
3. **Use Suspense boundaries** - Enable streaming and progressive loading
4. **Cache appropriately** - Use tags for granular revalidation
5. **Measure before/after** - Always verify improvements with real metrics

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/core-web-vitals.md` — LCP/INP/CLS targets, diagnostics, and per-metric optimizations · read when measuring or fixing Core Web Vitals.
- `references/image-optimization.md` — next/image sizing, priority, blur placeholder, remotePatterns config · read when fixing LCP or image-related CLS.
- `references/font-optimization.md` — next/font setup, subsets, display swap, CSS variable integration · read when eliminating font-related CLS or FOUT.
- `references/caching-strategies.md` — unstable_cache, revalidateTag/Path, ISR, cache tags, TTL guidance · read when configuring data or route caching.
- `references/server-components.md` — Client-to-Server conversion patterns, RSC constraints, Suspense boundaries · read when moving components server-side or wiring streaming.
- `references/streaming-suspense.md` — Suspense boundaries, progressive loading, fallback skeletons · read when implementing streaming or reducing TTFB.
- `references/bundle-optimization.md` — dynamic(), code splitting, tree shaking, modularizeImports, bundle-analyzer · read when reducing initial JS bundle size.
- `references/metadata-seo.md` — static/generateMetadata, Open Graph, canonical, sitemap · read when configuring metadata or SEO.
- `references/api-routes.md` — Route Handler patterns, Edge runtime, input validation, error handling · read when optimizing API routes.
- `references/nextjs-16-patterns.md` — async params Promise, use() hook, useOptimistic, React 19 patterns · read when adopting Next.js 15+/React 19 APIs.

## Common Conversions

| From | To | Benefit |
|------|-----|---------|
| `useEffect` + fetch | Direct async in Server Component | -70% JS, faster TTFB |
| `useState` for data | Server Component with direct DB access | Simpler code, no hydration |
| Client-side fetch | `unstable_cache` or ISR | Faster repeated loads |
| `img` tag | `next/image` | Optimized formats, lazy loading |
| CSS font import | `next/font` | Zero CLS, automatic optimization |
| Static import of heavy component | `dynamic()` | Reduced initial bundle |

## Constraints and Warnings

### Server Components Limitations
- Cannot use browser APIs (window, localStorage, document)
- Cannot use React hooks (useState, useEffect, useContext)
- Cannot use event handlers (onClick, onSubmit)
- Cannot use dynamic imports with ssr: false

### Image Optimization Constraints
- `priority` should only be used for above-the-fold images
- External images require configuration in next.config.js
- `width` and `height` are required unless using `fill`
- Animated GIFs are not optimized by default

### Caching Considerations
- Cache tags must be manually invalidated
- Data cache is per-request in development
- Edge runtime has different caching behavior
- Be careful caching user-specific data

### Bundle Size Warnings
- Dynamic imports can impact SEO if critical content
- Tree shaking requires proper ES module usage
- Some libraries cannot be tree shaken (avoid barrel exports)
- Client Components increase bundle size - use sparingly

## Performance Checklist

- [ ] All images use `next/image` with proper dimensions
- [ ] LCP images have `priority` attribute
- [ ] Fonts use `next/font` with subsets
- [ ] Server Components used where possible
- [ ] Client Components at leaf level only
- [ ] Suspense boundaries for data fetching
- [ ] Caching configured for expensive operations
- [ ] Bundle analyzed for duplicates
- [ ] Heavy components lazy loaded
- [ ] Lighthouse score verified before/after

## Common Mistakes

```tsx
// ❌ DON'T: Fetch in useEffect
'use client'
useEffect(() => { fetch('/api/data').then(...) }, [])

// ✅ DO: Fetch directly in Server Component
const data = await fetch('/api/data')

// ❌ DON'T: Forget dimensions on images
<Image src="/photo.jpg" />

// ✅ DO: Always provide dimensions
<Image src="/photo.jpg" width={800} height={600} />

// ❌ DON'T: Use priority on all images
<Image src="/photo1.jpg" priority />
<Image src="/photo2.jpg" priority />

// ✅ DO: Priority only for LCP
<Image src="/hero.jpg" priority />
<Image src="/photo.jpg" loading="lazy" />

// ❌ DON'T: Cache everything with same TTL
{ revalidate: 3600 }

// ✅ DO: Match TTL to data change frequency
{ revalidate: 86400 } // Categories rarely change
{ revalidate: 60 }     // Comments change often
```

