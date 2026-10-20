---
description: Performance rules for frontend, backend and database code, without premature optimization
globs: "**/*.{ts,tsx,js,jsx,mjs,vue,svelte,astro,css,scss,dart,py,go,rs,sql,prisma}"
alwaysApply: false
---

# Performance

Do not optimize speculatively. Do not knowingly ship obvious problems. Measure before micro-optimizing (build size report, Lighthouse, React Profiler, Flutter DevTools, query `EXPLAIN`).

## Bundle and startup
- Code-split by route. Heavy libraries (3D, charts, editors, animation) load only where used.
- Import icons and utilities individually, not whole barrels.
- Check bundle impact when adding a dependency. Justify large chunk growth.

## Rendering
- Avoid unnecessary re-renders/rebuilds: colocate state, stable props, no new objects in hot lists without reason.
- Memoization (`useMemo`, `memo`, `const` widgets) where cost is real or obvious, not everywhere.
- Virtualize long lists (`ListView.builder`, virtual scrollers). Paginate large content.
- Animate `transform`/`opacity` only. Respect reduced motion.

## Assets
- Responsive, modern-format images with explicit dimensions. Lazy-load below the fold, prioritize the LCP image.
- Fonts: subset, `font-display: swap`, only used weights.

## Network
- No duplicate or waterfall requests. Parallelize independent fetches. Minimal payloads.
- Cache with correct headers or framework caching. Abort stale requests.

## Server and database
- Check for N+1 queries, missing indexes on filter/join/sort columns, `SELECT *`, unbounded queries, inefficient joins, missing pagination.
- Use connection pooling, transactions where consistency matters, and timeouts on outbound calls.
- Never list or scan whole collections/namespaces on hot paths.
