# packages/analytics-browser — AGENTS.md

## What this package owns

`@t/analytics-browser` is the **browser (Next.js / web) platform implementation** of the
`AnalyticsTracker` port. It adapts `posthog-js` to the abstract port surface defined in
`@t/analytics-types`, provides React hooks (`useAnalytics`, `useIdentify`, `usePageView`),
and owns `registerAnalyticsBrowserDI()` — the single call `apps/web` makes at its client
composition root to bind the browser tracker. It is safe to import in browser bundles; it
must never be imported in Node/server-only paths.

## Layout

```
src/
  infrastructure/
    PostHogBrowserAnalyticsTracker.ts  # posthog-js impl — god-node (~18 edges)
    NoOpAnalyticsTracker.ts            # browser-side no-op (extends @t/analytics NoOp pattern)
    init.ts                            # posthog-js bootstrap (called once at app boot)
  react/
    useAnalytics.ts    # hook: exposes capture / captureException on the resolved tracker
    useIdentify.ts     # hook: calls identify() on mount / userId change
    usePageView.ts     # hook: fires capturePageView() on route change
  dependency-injection/
    registerAnalyticsBrowserDI.ts      # composition-root entry point (see below)
  types.ts             # browser-specific type re-exports / augmentations
```

Note: no `entities/` or `utils/` directories. Add `utils/` for pure browser helpers; never add
provider-specific code there.

## DI registrar

File: `packages/analytics-browser/src/dependency-injection/registerAnalyticsBrowserDI.ts`

```ts
registerAnalyticsBrowserDI(container: Container, opts: RegisterAnalyticsBrowserDIOptions): void
// opts: { config: BrowserConfigAccessor, noOp?: boolean, pii?: ScrubOptions }
```

Selection order (first match wins):
1. `opts.noOp === true` → `NoOpAnalyticsTracker`
2. `typeof window === 'undefined'` → `NoOpAnalyticsTracker` (SSR guard)
3. `!config.get('NEXT_PUBLIC_POSTHOG_KEY')` → `NoOpAnalyticsTracker` + `console.warn`
4. otherwise → `PostHogBrowserAnalyticsTracker`

Lifetime: singleton (`dependencyKeys.global.ANALYTICS`).
Env vars: `NEXT_PUBLIC_POSTHOG_KEY`, `NEXT_PUBLIC_POSTHOG_HOST`.

## Consumers

- `apps/web` — the only consumer; calls `registerAnalyticsBrowserDI` in its client composition root
  and mounts the React hooks in `_app` / layout boundary

## Conventions

- Port-first: never import `PostHogBrowserAnalyticsTracker` directly in app code — resolve via DI.
- `NoOpAnalyticsTracker` is the safe default whenever posthog-js cannot initialise (SSR, missing
  key, test env).
- PII scrubbing (`scrubPiiFromProperties`, `scrubPiiFromTraits`) from `@t/analytics-types` is
  called inside `PostHogBrowserAnalyticsTracker` on every user-controlled payload — do not send raw
  properties directly to `posthog.capture`.
- `posthog-js` must not be imported outside `infrastructure/`; hooks and DI registrar are
  decoupled from the SDK.
- The `pii?: ScrubOptions` option threads through `registerAnalyticsBrowserDI` →
  `PostHogBrowserAnalyticsTracker`; add new scrub controls there only.

## Links

- Architecture spec: `docs/architecture/platform/analytics/analytics.md`
- Port definition: `packages/analytics-types/AGENTS.md`
- Server-side registrar: `packages/analytics/AGENTS.md`
- RN impl (parallel): `packages/analytics-rn/AGENTS.md`
