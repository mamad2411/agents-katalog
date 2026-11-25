---
name: performance-patterns
description: Performance optimization patterns — lazy loading, caching, memoization, code splitting, bundle optimization.
---

# Performance Patterns

## Frontend Performance

### Lazy Loading
```javascript
const HeavyComponent = lazy(() => import('./HeavyComponent'))
```
Load components only when needed. Use for routes, modals, below-fold content.

### Memoization
```javascript
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b])
const memoizedFn = useCallback(() => doSomething(a, b), [a, b])
```
Cache expensive computations and function references.

### Code Splitting
Split your bundle by route or feature. Users only download what they need.

### Image Optimization
- Use WebP/AVIF formats
- Lazy load below-fold images
- Use responsive images (srcset)
- Compress images (tinyPNG, Sharp)

### CSS Performance
- Use `transform` and `opacity` for animations (GPU-accelerated)
- Avoid `layout` triggers (width, height, margin, padding)
- Use `will-change` sparingly
- Minimize repaints with `contain`

## Backend Performance

### Caching
- Cache database queries (Redis, in-memory)
- Cache API responses (HTTP caching headers)
- Cache expensive computations (memoization)
- Cache rendered pages (SSR cache)

### Database Optimization
- Add indexes for frequent queries
- Use connection pooling
- Batch inserts/updates
- Avoid N+1 queries
- Use EXPLAIN ANALYZE

### Async Operations
- Don't block the event loop
- Use worker threads for CPU-intensive tasks
- Stream large responses
- Queue background jobs

## Measurement

- **Lighthouse** — overall performance score
- **Core Web Vitals** — LCP, FID, CLS
- **Chrome DevTools** — Performance tab, Lighthouse tab
- **webpack-bundle-analyzer** — bundle size visualization
- **ab / wrk** — load testing

## Common Anti-Patterns

- Loading everything upfront
- Not caching expensive operations
- Synchronous database calls in loops
- Large bundle sizes (no code splitting)
- Unoptimized images (no lazy loading, wrong format)
- Layout thrashing (reading layout then writing)
