---
name: react-nextjs-app-router-rendering
description: "Design Next.js App Router rendering, Server/Client boundaries, cache, SSR, and hydration."
---

# React Next.js App Router Rendering

Design, implement, debug, or review Next.js App Router rendering boundaries with a deliberate split between Server Components, Client Components, Server Functions, Route Handlers, routing, cache, and hydration.

## Process

1. Inspect Next.js version, App Router usage, route tree, layouts, providers, config, deployment mode, and cache features before changing rendering behavior.
2. Use `itsol-current-tech-context` for version-specific App Router, React 19, cache, Server Functions, or React Compiler behavior.
3. Default to Server Components; introduce Client Components only for event handlers, local state, effects, browser APIs, TanStack Query client use, websockets/SSE, or DOM-bound UI libraries.
4. Treat Route Handlers and Server Functions as server code with auth, validation, safe logging, error mapping, cache policy, and telemetry.
5. Verify hydration, route reload, deep link, cache invalidation, and production build behavior when relevant.

## Coordination

Use with `react-nextjs-implementation`, `react-nextjs-debugging`, `react-nextjs-review`, `react-nextjs-api-cache-forms`, `react-nextjs-quality-security`, and `security-frontend-browser-review`.

## Focused References

- [01-server-client-boundaries.md](./references/01-server-client-boundaries.md) - Server Client Boundaries
- [02-server-actions-and-route-handlers.md](./references/02-server-actions-and-route-handlers.md) - Server Actions And Route Handlers
- [03-routing-cache-hydration.md](./references/03-routing-cache-hydration.md) - Routing Cache And Hydration
