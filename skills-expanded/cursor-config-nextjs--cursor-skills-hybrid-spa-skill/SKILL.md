---
name: next-hybrid-spa
description: Create a hybrid SPA section with client islands and partial hydration.
disable-model-invocation: true
---
# Next.js Hybrid SPA

Create a client-heavy section within an App Router app with clear
server/client boundaries.

## When to Use

- SPA-like interactions within a Next.js app
- Client-driven state and routing behavior
- Partial hydration for interactive widgets

## Inputs

- Route segment
- Interactive components list
- Client-side state requirements

## Instructions

1. Keep the route entry as a Server Component.
2. Move interactive parts to Client Components.
3. Use `useTransition` for non-urgent updates.
4. Use `useSearchParams`/`useRouter` only in Client Components.
5. Avoid `ssr: false` unless strictly necessary.

## Output

- Hybrid page with server shell and client islands.
