---
name: react-nextjs-implementation
description: "Implement React 19/Next.js apps with App Router, typed UI, APIs, forms, cache, and tests."
---

# React Next.js Implementation

Build React 19 and Next.js frontend changes around clear rendering boundaries, typed contracts, explicit cache ownership, accessible UI states, secure server/client separation, and measurable verification.

## Process

1. Inspect repo conventions, `.itsol.md` policy, package versions, routing mode, generated API setup, testing commands, and deployment target before introducing structure.
2. Use `itsol-current-tech-context` for React, Next.js, TanStack Query, Hey API, Tailwind, testing, or package-version decisions.
3. Decide whether the app needs Next.js or a simpler React SPA, then choose the smallest architecture that matches product scope.
4. Keep `app/` thin: routing, layouts, providers, boundaries, and page composition. Put domain behavior in feature modules and shared primitives in `shared`.
5. Prefer Server Components by default and move Client Components as low in the tree as possible.
6. Define loading, empty, error, permission, stale/refetching, mobile, and keyboard behavior before editing visible UI.
7. Use proportionate checks for changed behavior, starting with maintained tests. Add tests only for meaningful gaps; no test-first or exception gate is required. Use TDD only on explicit user request.

## Coordination

Use with `itsol-functional-planning`, `react-nextjs-app-router-rendering`, `react-nextjs-api-cache-forms`, `react-nextjs-quality-security`, `ui-ux-workflow`, `hey-api-openapi-*`, and `security-frontend-browser-review` as relevant.

## Scope And Architecture

- Choose Next.js when the product needs SSR, SSG, SEO, App Router, streaming, Server Components, Route Handlers, Server Functions, or hybrid rendering.
- Prefer a plain React SPA for internal authenticated panels when SEO does not matter, the backend API is separate, SSR adds operational cost, and deployment should be static.
- For MVPs, use vertical slices. For medium apps, use feature modules with public entrypoints. For large apps, consider Feature-Sliced Design or monorepo boundaries only if the team will enforce import rules.
- Keep `app/` responsible for routing, layouts, providers, route boundaries, metadata, and page composition.
- Keep feature-specific API, components, model, hooks, schemas, and permissions inside `features/<feature>`.
- Keep domain-free primitives in `shared/ui`, API infrastructure in `shared/api`, config in `shared/config`, and telemetry in `shared/telemetry`.
- Avoid global `components/`, `utils.ts`, or `types.ts` folders that collect unrelated code.
- Do not introduce Clean Architecture in frontend unless the app has real domain logic, multiple data sources, long lifecycle, and several teams.

## TypeScript And Config

- Require `strict: true`; do not disable production type errors through `typescript.ignoreBuildErrors`.
- Prefer generated OpenAPI types for API data and runtime validation at unstable or external boundaries.
- Use `unknown` plus narrowing instead of `any`; avoid `as SomeType` to hide unsafe data.
- Use `satisfies` when checking object shape while preserving inference.
- Model statuses, roles, permissions, event types, and domain states as unions or enum-like objects.
- Consider branded types for tenant IDs, entity IDs, money, dates, and other domain values.
- Keep public component props explicit when components are shared.
- Use `@ts-expect-error` only with a reason; avoid `@ts-ignore`.
- Set `poweredByHeader: false`.
- Do not put secrets in `NEXT_PUBLIC_*`, `next.config.ts env`, Client Components, or static files.
- Separate build-time env from runtime env for Docker/self-hosted deployments.

## React 19 Components And Hooks

- Keep render pure with respect to props and state. Do not do mutating I/O, storage writes, requests, subscriptions, or logging side effects in render.
- Use `useState` for local UI state, `useReducer` for complex component transitions, and `useRef` for mutable values that should not render.
- Do not duplicate state that can be derived from props, query data, or URL params.
- Use `useMemo`, `useCallback`, and `React.memo` for measured or API-specific reasons, not as default ceremony.
- Use `useTransition` for slow UI transitions that should not block typing or clicking.
- Use `useOptimistic` only with a backend source of truth and rollback/sync behavior.
- Use `useActionState` and `useFormStatus` for forms backed by Server Functions or React Actions.
- Use `use` only with a deliberate Suspense/rendering boundary.
- Treat Strict Mode warnings and double-invocation symptoms as defect signals.

## UI States And Components

- Every data view should define loading, empty, error, partial error, permission denied, stale/refetching, and success states when relevant.
- Skeletons should approximate final dimensions to reduce layout shift.
- Errors should offer a concrete action such as retry, change filter, go back, or contact support.
- Distinguish `401`, `403`, `404`, validation errors, network errors, and server errors in UI behavior.
- Base components such as Button, Input, Dialog, Select, and Table must stay domain-free.
- Domain components may know business states, for example `OrderStatusBadge`.
- Component props should express intent: `variant`, `size`, `tone`, `state`, not `isBlue` or `hasMargin`.
- Split components when independent modes, API calls, permissions, forms, and layout concerns make one file hard to reason about.

## Tailwind, Accessibility, And Responsive UI

- Use Tailwind as a design-system implementation detail, not a source of random values.
- Keep color, spacing, radius, typography, and z-index tokens central; use Tailwind v4 `@theme` when the project uses Tailwind v4.
- Avoid arbitrary values unless they come from a design requirement.
- Use semantic HTML before ARIA.
- Inputs need labels or accessible names. Field errors should be connected with `aria-describedby`.
- Keyboard support must cover Tab, Shift+Tab, Enter, Space, Escape, and arrows where patterns require them.
- Dialogs must manage focus and return it to the trigger.
- Color cannot be the only carrier of information.
- Hover cannot be the only interaction path because mobile has no hover.
- Respect `prefers-reduced-motion`.

## Verification

- Run the narrowest relevant verification first: typecheck, lint, component/unit tests, generated client check, build, Playwright, accessibility checks, bundle analysis, or smoke testing.
- For legacy repos without maintained tests, use proportionate supported verification. Do not scaffold a framework without agreed scope or require a TDD exception.
- For visible UI, verify important states, mobile/desktop behavior, long text, keyboard access, slow API, and error paths.
