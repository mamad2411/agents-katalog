---
name: performance-budget
description: >-
  Use when the app feels slow, bundle is large, or optimizing LCP, INP, CLS,
  images, or unnecessary re-renders. Not for SEO copy or accessibility-only
  passes.
---

# Performance budget

## Measure first

Identify: LCP element, large JS chunks, N+1 network, layout shift sources.

## Images

- WebP/AVIF; explicit `width`/`height` or aspect ratio to prevent CLS.
- Lazy load below fold; priority only for LCP hero.

## Data

- No duplicate fetches — dedupe with SWR/React Query keys (`typed-api-hooks-forms` / `tanstack-query-alternative`).
- Prefer one joined Supabase `select` over many parallel hooks on same screen.
- Paginate large lists; virtualize tables > 100 rows when needed.

## React

- Memoize expensive lists only when profiling shows need — avoid premature `useMemo` everywhere.
- Split routes with lazy `React.lazy` + `Suspense` for heavy admin sections.
- Defer non-critical third-party scripts (analytics).

## Bundle

- Import icons/components individually; avoid barrel importing huge libs.
- Check for duplicate date/libs (moment + dayjs).

## Targets (guidance)

- LCP < 2.5s on mid mobile where possible.
- Avoid main-thread long tasks from sync JSON parse of huge payloads.

## Output

List findings: issue | impact (high/med/low) | recommended fix.
