---
name: ssr-and-hydration
description: Implement server-side rendering and hydration. Use when building or
  debugging SSR apps.
metadata:
  tags: ssr, hydration
---

# SSR & Hydration

## Use this skill when
- Rendering pages on the server for SEO and first paint
- Debugging hydration mismatches
- Choosing between SSR, SSG, and CSR
- Streaming SSR for faster TTFB

## Do not use this skill when
- A pure static site (use SSG)
- A client-only internal tool

## Instructions
1. Match SSR HTML with the client render to avoid hydration mismatches.
2. Fetch data on the server before rendering what can be.
3. Stream HTML and hydrate asynchronously where possible.
4. Avoid browser-only APIs during the initial render.
5. Keep client and server renders deterministic (stable IDs, no random).
6. Cache SSR output for repeatable content.
7. Measure TTFB and LCP after each change.

## Checklist
- No hydration mismatch warnings in dev
- Repeated requests reuse cached HTML

## Output Format
- Rendering strategy | data flow | hydration plan | perf targets

## Common Mistakes
- Ignoring hydration mismatches
- Doing heavy server work that delays TTFB
- Random/time-based output in first render
