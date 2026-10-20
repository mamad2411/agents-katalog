# packages/analytics-rn — AGENTS.md

## What this package owns

`@t/analytics-rn` is the **React Native / Expo platform implementation** of the
`AnalyticsTracker` port. It adapts `posthog-react-native` to the abstract port surface defined
in `@t/analytics-types`, provides RN hooks (`useAnalytics`, `useIdentify`, `useScreen`), and
owns `registerAnalyticsRnDI()` — the single call `apps/mobile` makes at its composition root
to bind the RN tracker. It is safe to import in React Native bundles; it must never be imported
in Node/server-only or browser paths.

## Layout

```
src/
  infrastructure/
    PostHogRnAnalyticsTracker.ts    # posthog-react-native impl — god-node (~19 edges)
    NoOpAnalyticsTracker.ts         # RN-side no-op
    init.ts                         # posthog-react-native bootstrap
    init.test.ts
    NoOpAnalyticsTracker.test.ts
    PostHogRnAnalyticsTracker.test.ts
  react/
    useAnalytics.ts     # hook: exposes capture / captureException
    useIdentify.ts      # hook: calls identify() on mount / userId change
    useScreen.ts        # hook: fires captureScreen() on navigation focus
    useAnalytics.test.ts
    useIdentify.test.ts
    useScreen.test.ts
  dependency-injection/
    registerAnalyticsRnDI.ts        # composition-root entry point (see below)
    registerAnalyticsRnDI.test.ts
  __test__/
    stubLogging.ts      # test helper — stubs @t/logging for unit tests
  types.ts              # RN-specific type re-exports / augmentations
```

Note: no `entities/` directory. Add `utils/` for pure RN helpers; never add SDK-specific code there.

## DI registrar

File: `packages/analytics-rn/src/dependency-injection/registerAnalyticsRnDI.ts`

```ts
registerAnalyticsRnDI(container: Container, opts: RegisterAnalyticsRnDIOptions): void
// opts: { config: RnConfigAccessor, noOp?: boolean, pii?: ScrubOptions, environment?: string }
```

Selection order (first match wins):
1. `opts.noOp === true` → `NoOpAnalyticsTracker`
2. `!config.get('POSTHOG_API_KEY')` → `NoOpAnalyticsTracker` + `console.warn`
3. otherwise → `PostHogRnAnalyticsTracker` (hardcoded `service: "mobile"`)

Lifetime: singleton (`dependencyKeys.global.ANALYTICS`).
Env vars: `POSTHOG_API_KEY`, `POSTHOG_HOST`.

## Consumers

- `apps/mobile` — the only consumer; calls `registerAnalyticsRnDI` in its composition root and
  mounts hooks in the Expo root layout

## Conventions

- Port-first: never import `PostHogRnAnalyticsTracker` directly in app code — resolve via DI.
- `NoOpAnalyticsTracker` is the safe default whenever posthog-react-native cannot initialise
  (missing key, test env, simulator without network).
- PII scrubbing (`scrubPiiFromProperties`, `scrubPiiFromTraits`) from `@t/analytics-types` is
  called inside `PostHogRnAnalyticsTracker` on every user-controlled payload.
- `posthog-react-native` must not be imported outside `infrastructure/`; hooks and the DI
  registrar are decoupled from the SDK.
- `useScreen` is the RN equivalent of `usePageView`; use it for navigation events instead of
  calling `captureScreen` manually in screen components.
- Tests use `__test__/stubLogging.ts` to silence `@t/logging` — add shared test stubs here, not
  inline in individual test files.

## Links

- Architecture spec: `docs/architecture/platform/analytics/analytics.md`
- Port definition: `packages/analytics-types/AGENTS.md`
- Server-side registrar: `packages/analytics/AGENTS.md`
- Browser impl (parallel): `packages/analytics-browser/AGENTS.md`
