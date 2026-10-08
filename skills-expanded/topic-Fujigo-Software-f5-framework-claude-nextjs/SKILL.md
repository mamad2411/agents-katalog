---
name: nextjs-skills
description: Next.js framework patterns, SSR/SSG, and App Router best practices
category: stacks/frontend/nextjs
applies_to: nextjs
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Next.js Skills

React framework for production with hybrid static & server rendering.

## Sub-Skills

### Architecture
- [app-router.md](architecture/app-router.md) - App Router patterns
- [pages-router.md](architecture/pages-router.md) - Pages Router patterns
- [project-structure.md](architecture/project-structure.md) - Project organization

### Rendering
- [server-components.md](rendering/server-components.md) - Server Components
- [client-components.md](rendering/client-components.md) - Client Components
- [ssr.md](rendering/ssr.md) - Server-side rendering
- [ssg.md](rendering/ssg.md) - Static generation
- [isr.md](rendering/isr.md) - Incremental Static Regeneration

### Data Fetching
- [server-actions.md](data-fetching/server-actions.md) - Server Actions
- [fetch-api.md](data-fetching/fetch-api.md) - Fetch patterns
- [caching.md](data-fetching/caching.md) - Caching strategies

### Routing
- [dynamic-routes.md](routing/dynamic-routes.md) - Dynamic routes
- [route-handlers.md](routing/route-handlers.md) - API routes
- [middleware.md](routing/middleware.md) - Middleware patterns
- [layouts.md](routing/layouts.md) - Layout patterns

### Performance
- [image-optimization.md](performance/image-optimization.md) - next/image
- [font-optimization.md](performance/font-optimization.md) - next/font
- [bundle-analysis.md](performance/bundle-analysis.md) - Bundle optimization

### Authentication
- [next-auth.md](authentication/next-auth.md) - NextAuth.js
- [middleware-auth.md](authentication/middleware-auth.md) - Middleware auth

### Testing
- [jest.md](testing/jest.md) - Jest patterns
- [playwright.md](testing/playwright.md) - E2E testing

## Detection
Auto-detected when project contains:
- `next.config.js` or `next.config.mjs`
- `next` package
- `getServerSideProps` or `getStaticProps` patterns
