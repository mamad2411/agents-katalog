---
name: review-react-rsc
description: How to review React Server Components (RSC) for correctness, perf, and the use server/use client boundary
when_to_use: Reviewing TSX/JSX in Next.js app/ or pages/ directories that mix server and client code
matches:
  extensions: [".tsx", ".jsx"]
  imports: ["next", "react-server"]
  filename_patterns: ["**/app/**/*", "**/pages/**/*"]
  frameworks: ["nextjs", "react"]
---

# Reviewing React Server Components

When reviewing RSC code, focus on these concerns:

1. **Boundary violations**: Calling client hooks (`useState`, `useEffect`) inside
   a server component, or importing server-only modules from client code.
2. **Data fetching anti-patterns**: Sequential `await` instead of `Promise.all`,
   missing `cache()` wrapping for shared queries.
3. **Hydration mismatches**: Date/random/non-deterministic content in server
   render without `suppressHydrationWarning`.
4. **Bundle bloat**: Importing heavy client libraries in components that don't
   need interactivity — should be server components.
