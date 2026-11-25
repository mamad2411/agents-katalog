---
name: nextjs-16-application-development
description: Builds and refactors Next.js 16 App Router features, Server and Client Component boundaries, Proxy, route handlers, Server Functions, and Cache Components. Use when implementing routes, layouts, mutations, rendering behavior, caching, or request-boundary logic in a Next.js 16 app.
license: MIT
compatibility: Requires a Next.js 16 project. Node.js 20.9.0+ is expected by Next.js 16.
---

# Next.js 16 Application Development

Use this skill for feature implementation and architecture decisions inside a Next.js 16 application.

## When to Use

- Creating or changing App Router routes, layouts, templates, loading states, error boundaries, metadata, or route handlers.
- Designing Server Component and Client Component boundaries.
- Implementing Server Functions or Server Actions.
- Adding or migrating Proxy request-boundary logic.
- Enabling or using Cache Components and `use cache`.
- Debugging rendering, navigation, hydration, or cache behavior.

## Workflows

- `workflows/app-router-feature-workflow.md`: Use for normal feature implementation in App Router.
- `workflows/app-router-design-workflow.md`: Use when designing or refactoring route trees, layouts, route groups, route handlers, and app-level boundaries.
- `workflows/rendering-strategy-review-workflow.md`: Use when choosing SSR, CSR, static rendering, streaming, dynamic rendering, or Cache Components for a route.
- `workflows/cache-components-workflow.md`: Use when enabling, designing, reviewing, or debugging Cache Components and `use cache`.

## Resources

- `resources/nextjs-16-routing-rendering-checklist.md`: Review route structure, rendering mode, Suspense, metadata, Server/Client Component boundaries, and route handlers.
- `resources/nextjs-16-rendering-strategy-matrix.md`: Choose a rendering and caching strategy for App Router routes.
- `resources/nextjs-16-cache-components-decision-tree.md`: Decide whether to leave data uncached, use `use cache`, use tags, use cache lifetimes, or introduce remote/private cache handlers.

## Examples

- `examples/authenticated-server-action.md`: Minimal secure Server Action mutation pattern.
- `examples/proxy-example.md`: Minimal `proxy.ts` request-boundary pattern.

## Operating Guidance

1. Confirm the repository is using Next.js 16 before applying version-specific behavior.
2. Inspect the nearest `package.json`, lockfile, `next.config.*`, `app/` or `src/app/` tree, and existing conventions.
3. Preserve project conventions unless they conflict with Next.js 16 compatibility or security rules.
4. Prefer Server Components by default. Use Client Components only for browser-only behavior.
5. Keep runtime data, auth checks, mutation logic, and data access on the server.
6. Do not mix request-specific data into cached scopes.
7. Keep Proxy small and focused on network-boundary decisions.
8. After implementation, hand off to the `nextjs-16-quality-and-migration` skill for verification when checks, audits, or migration review are needed.

## Decision Tree

- Need browser event handlers, state, refs, browser APIs, or a client-only library? Use a small Client Component boundary.
- Need data fetching without client interactivity? Prefer a Server Component or server-only module.
- Need mutation from a form or transition? Use a Server Function or Server Action with auth, validation, and controlled return values.
- Need request interception before rendering? Use `proxy.ts`, not a route component.
- Need shared cached data or prerenderable shells? Evaluate Cache Components with the cache decision resource.
- Need route-local API behavior? Use a route handler and keep its input/output contract explicit.

## Final Response Expectations

When reporting application changes:

- State which routes/components/actions/config files changed.
- State whether behavior is static, dynamic, cached, or request-time.
- State what checks were run and what remains unverified.
