# packages/analytics-types — AGENTS.md

## What this package owns

`@t/analytics-types` is the **zero-dependency shared layer** for the entire analytics cluster.
It owns the canonical `AnalyticsTracker` abstract class (the port), all domain types and Zod
schemas, and the `scrubPii` PII-redaction helpers. Every other analytics package (`@t/analytics`,
`@t/analytics-browser`, `@t/analytics-rn`) imports exclusively from here for types and
redaction — no cross-package coupling to impl details. Placing shared code here instead of in the
server package ensures browser and RN bundles can import it without pulling in Node-only deps.

## Layout

```
src/
  ports/
    AnalyticsTracker.ts       # canonical abstract class — 11-method port surface
    RequestAnalyticsTracker.ts
  types/
    AnalyticsTrackerOptions.ts
    Environment.ts
    LlmEvent.ts
    RevenueEvent.ts
    ReservedSuperProps.ts     # isReservedKey() guard used by scrubPii
    Service.ts
  schemas/
    EventSchema.ts            # Zod schema for the Event envelope
  redaction/
    scrubPii.ts               # scrubPiiFromProperties / scrubPiiFromTraits / scrubEvent
```

Note: no `infrastructure/`, `dependency-injection/`, or `utils/` directories — this package
holds only types, ports, schemas, and pure functions.

## DI registrar

None. `@t/analytics-types` is a types-only package; it is never registered in a DI container
directly. The concrete registrars live in `@t/analytics`, `@t/analytics-browser`, and
`@t/analytics-rn`.

## Consumers

All packages and apps in the analytics cluster:
- `@t/analytics` — imports `AnalyticsTracker`, all domain types, and `scrubPii`
- `@t/analytics-browser` — same; also imports `ScrubOptions` for the DI registrar
- `@t/analytics-rn` — same
- `@t/logging`, `@t/billing` — may import types for cross-module event shapes (Phase 2+)

## Conventions

- Port-first: `AnalyticsTracker` is an **abstract class**, not an interface — this enables
  `instanceof` checks and forces a single nominal type across all impls.
- `scrubPii` is the **authoritative PII boundary** for the entire analytics cluster. Every impl
  must call `scrubPiiFromProperties` / `scrubPiiFromTraits` before forwarding to a PostHog SDK.
  Never add scrubbing logic inside an impl that is not delegating to these helpers.
- `DEFAULT_PII_KEYS` in `scrubPii.ts` mirrors `DEFAULT_REDACT_PATHS` from `@t/logging`. Keep
  these lists in sync; if you add a key to one, add it to the other.
- `isReservedKey()` (from `ReservedSuperProps.ts`) gates reserved super-props from being
  redacted. Reserved keys (`$environment`, `$service`, `$session_id`, etc.) always pass through.
- `ScrubOptions` is the public API for callers that need to customise redaction (`extraKeys`,
  `allowKeys`, `replaceWith`, `skipPatterns`). Extend this type, not `scrubPii`'s internals.
- No Node.js builtins, no SDK imports, no side effects at module level.

## Links

- Architecture spec: `docs/architecture/platform/analytics/analytics.md`
- Redaction source: `packages/analytics-types/src/redaction/scrubPii.ts`
- Server registrar: `packages/analytics/AGENTS.md`
- Browser impl: `packages/analytics-browser/AGENTS.md`
- RN impl: `packages/analytics-rn/AGENTS.md`
