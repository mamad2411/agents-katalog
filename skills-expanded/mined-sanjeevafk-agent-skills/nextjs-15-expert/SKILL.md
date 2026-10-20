---
name: nextjs-15-expert
description: Expert implementation guidance for Next.js 15 App Router, Server Components, and performance-first patterns.
---

# Next.js 15 Expert

## Objective
Design and implement robust Next.js 15 App Router solutions with correct server/client boundaries.

## Implementation Priorities
1. Prefer Server Components and server data fetching.
2. Use Client Components only for browser interactivity.
3. Implement route-level loading/error handling.
4. Use caching and revalidation intentionally.
5. Keep secrets and privileged operations server-side.

## App Router Standards
- Route structure should be clear and co-located.
- Use route handlers for server APIs when needed.
- Use Server Actions for trusted mutations with validation.
- Avoid duplicated fetching across nested layouts/pages.

## Performance and DX
- Minimize client JS bundle size.
- Avoid unnecessary hydration.
- Stream content where helpful.
- Ensure metadata and SEO fundamentals are configured.

## Output Format
- Proposed route/component architecture.
- Data flow and caching strategy.
- Security notes and test checklist.
