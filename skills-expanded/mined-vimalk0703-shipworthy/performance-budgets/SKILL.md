---
name: performance-budgets
description: Bundle size limits, API response time budgets, query limits, image optimization, lazy loading, and caching strategies.
invoke_when: Use when writing frontend bundles, creating API endpoints, optimizing performance, or when architecture.md defines performance budgets.
---

# Performance Budgets

## Default Budgets (customize in architecture.md)

### Frontend
- **Initial bundle**: <250KB gzipped (JavaScript)
- **Per-route chunk**: <50KB gzipped
- **Largest Contentful Paint**: <2.5s
- **First Input Delay**: <100ms
- **Cumulative Layout Shift**: <0.1
- **Images**: WebP/AVIF, lazy-loaded below fold, explicit width/height

### API
- **Response time (p95)**: <200ms for reads, <500ms for writes
- **Payload size**: <1MB per response
- **Database queries per request**: <10

### Database
- **Query execution**: <100ms (log anything slower)
- **Connection pool**: sized for expected concurrency

## Enforcement Strategies

### Frontend
- Analyze bundle with `npx next build` / `npx vite build` — check output sizes
- Use dynamic imports / `React.lazy()` for non-critical routes
- Tree-shake unused code — avoid barrel exports (`index.ts` re-exporting everything)
- Prefer CSS over JavaScript for animations

### API
- Paginate list endpoints (never return unbounded results)
- Use caching headers (`Cache-Control`, `ETag`)
- Compress responses (gzip/brotli)
- Use database indexes for queried fields

### General
- Measure before optimizing — don't guess at bottlenecks
- Set budgets early, enforce them in CI
- Performance regression = bug, not technical debt
