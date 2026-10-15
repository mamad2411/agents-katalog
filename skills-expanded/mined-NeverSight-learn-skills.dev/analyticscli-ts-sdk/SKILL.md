---
name: analyticscli-ts-sdk
description: Use when integrating or upgrading the AnalyticsCLI TypeScript SDK in web, TypeScript, React Native, or Expo apps.
license: MIT
homepage: https://github.com/wotaso/analyticscli-skills
metadata: {"author":"wotaso","version":"1.6.6","analyticscli-target":"@analyticscli/sdk","analyticscli-supported-range":">=0.1.0-preview.3 <0.2.0","openclaw":{"emoji":"🧩","homepage":"https://github.com/wotaso/analyticscli-skills"}}
---

# AnalyticsCLI TypeScript SDK

## Use This Skill When

- adding AnalyticsCLI analytics to a JS or TS app
- instrumenting onboarding, paywall, purchase, or survey events
- upgrading within the current `@analyticscli/sdk` line
- validating SDK behavior together with `analyticscli`

## Supported Versions

- Skill pack: `1.6.6`
- Target package: `@analyticscli/sdk`
- Supported range: `>=0.1.0-preview.3 <0.2.0`
- If a future SDK major changes APIs or event contracts in incompatible ways, add a sibling skill such as `analyticscli-ts-sdk-v1`

See [Versioning Notes](references/versioning.md).

## Core Rules

- Initialize exactly once near app bootstrap.
- For generated host-app code, prefer object init with explicit identity mode (`init({ apiKey, identityTrackingMode: 'consent_gated', ... })`).
- `init('<YOUR_APP_KEY>')` shortform is acceptable for quick demos/tests.
- `initFromEnv(...)` is also valid when env-first bootstrap is preferred.
- Keep init options minimal: all init attributes are optional; `apiKey` is enough for ingest.
- In host apps, use client-safe publishable env names (for example `ANALYTICSCLI_PUBLISHABLE_API_KEY`).
- Do not use `WRITE_KEY` env names in generated host-app snippets (`ANALYTICSCLI_WRITE_KEY`, `EXPO_PUBLIC_ANALYTICSCLI_WRITE_KEY`, etc.).
- `runtimeEnv` is auto-attached. Do not pass a `mode` string.
- `debug` is only a boolean for SDK console logging.
- Do not pass `endpoint` and do not add endpoint env vars in app templates. Use the SDK default collector endpoint.
- For `platform`, do not use framework labels (`react-native`, `expo`).
- Use only canonical platform values (`web`, `ios`, `android`, `mac`, `windows`) or omit the field.
- In React Native/Expo, pass `Platform.OS` directly; the SDK normalizes values like `macos -> mac` and `win32 -> windows`.
- In React Native/Expo, prefer `appVersion` from `expo-application` (`nativeApplicationVersion`); nullable values can be passed directly.
- Do not specify `dedupeOnboardingStepViewsPerSession` in generated host-app code by default; SDK default is `true`. Only set it explicitly when the user requests a different behavior or asks for explicit config.
- Prefer SDK trackers over host-side wrapper utilities. Keep integration code close to call sites.
- Keep event properties stable and query-relevant.
- Avoid direct PII.
- Set `identityTrackingMode` explicitly in generated host-app bootstrap code; use `'consent_gated'` as the default.
- For EU/EEA/UK user traffic, keep `identityTrackingMode: 'consent_gated'` (or `strict`) unless legal counsel approves a different setup.
- `identify` / `setUser` only work when full tracking is enabled (`always_on`, or after `setFullTrackingConsent(true)` in `consent_gated`).
- Do not force storage adapters in generated bootstrap code by default.
- Avoid top-level `Promise` singletons in app utility files.
- Use neutral file names like `analytics.ts` (not provider-specific names such as `aptabase.ts`).
- Avoid re-exporting `PAYWALL_EVENTS` / `PURCHASE_EVENTS` from host app utility files. Import SDK constants directly when needed, or use `createPaywallTracker(...)`.
- When using `createPaywallTracker(...)`, create one tracker per stable paywall context and reuse it across `shown`/`skip`/purchase calls. Recreate only when defaults change.
- If your paywall provider exposes an offering/paywall identifier, pass it as `offering` in tracker defaults.
  RevenueCat: offering identifier; Adapty: paywall/placement identifier; Superwall: placement/paywall identifier.
- In hosted paywall screens (RevenueCat UI / Adapty / Superwall or custom wrappers around them), do not use generic `track(...)` / `trackEvent(...)` for paywall or purchase milestones.
  Use one memoized `createPaywallTracker(...)` per screen/context and route lifecycle callbacks to tracker methods:
  `shown` (visible), `purchaseStarted`, one terminal event (`purchaseSuccess`/`purchaseFailed`/`purchaseCancel`), and `skip` (dismiss/close/back).
- If multiple paywall screens exist, each screen/context must have its own stable tracker defaults (`source`, `paywallId`, optional `offering`) so events are not mixed across screens.
- Prefer SDK identity helpers (`setUser`, `identify`, `clearUser`) directly instead of wrapping identify logic in host-app boilerplate.
- Do not keep legacy analytics providers or event aliases active in generated host-app code.
- For touched paywall/purchase/onboarding flows, use canonical AnalyticsCLI event names only.
- For generated docs or README snippets, write from tenant developer perspective (`your app`, `your workspace`) and avoid provider-centric phrasing such as `our SaaS`.
- Default to canonical SDK event names at call sites.
- Before generating host-app code, ensure `@analyticscli/sdk` is upgraded to the newest preview in that repo.
- For onboarding instrumentation, use dedicated SDK onboarding APIs instead of generic `track(...)`/`trackEvent(...)`:
  `createOnboardingTracker(...)`, `trackOnboardingEvent(...)`, `trackOnboardingSurveyResponse(...)`,
  plus step helpers (`step(...).view()`, `step(...).complete()`, `step(...).surveyResponse(...)`).
- For onboarding survey events, prefer `trackOnboardingSurveyResponse(...)` (or tracker survey helpers) so SDK sanitization/normalization is preserved.

## Host App Minimalism Guardrails

When this skill writes host-app code, optimize for low boilerplate by default.

- Do not generate a large event translation layer such as `mapEventToCanonical(...)` with many `switch` branches.
- Do not create host-side wrappers around `identify`/`setUser` unless required by an existing app contract.
- Do not add per-call `try/catch` wrappers around every analytics helper unless the user asked for that policy.
- Do not duplicate SDK constants/events in host utility files.
- Prefer direct SDK calls in feature code (`trackPaywallEvent`, tracker helpers, `screen`, `track`) instead of generic proxy helpers.
- Keep a single screen-tracking owner per route boundary (parent layout or screen component, not both).
- If a thin `analytics.ts` is needed, keep it focused to bootstrap + a few shared helpers. Avoid becoming an event-translation layer.

## Hard Fail Patterns

Do not generate these patterns:

- giant `switch`/`if` trees that translate event names
- helpers like `mapEventToCanonical(...)` spanning many event cases
- broad catch-all wrappers around every analytics call
- top-level `Promise<AnalyticsClient | null>` bootstrap patterns
- host-side re-exports of SDK constants/events
- creating a new `createPaywallTracker(...)` instance inside each paywall callback/event helper
- helper wrappers that create a fresh paywall tracker per call (for example `trackPaywallTrackerEvent(...)`)
- hosted paywall screens that only emit `screen(...)` / `trackScreenView(...)` but never emit `paywall:shown`
- paywall/purchase milestones emitted via generic `track(...)` / `trackEvent(...)` although stable paywall context is available
- onboarding step/survey milestones emitted via generic `track(...)` / `trackEvent(...)` although dedicated onboarding APIs are available
- legacy/alias event names for onboarding/paywall/purchase milestones (for example `view_paywall`, `purchase_completed`)
- dual-write analytics emission to preserve old event names/providers
- `apiKey` fallback chains using `*WRITE_KEY*` env variables in host-app code
- duplicate screen tracking for the same route transition from both parent layout and child screen

If such a pattern already exists in the target codebase:
- do not expand it
- prefer reducing it while keeping behavior stable

## Pre-Ship Self-Check

Before finishing, verify the generated integration code meets all checks:

1. bootstrap uses `init('<API_KEY>')`, `init({...})`, or `initFromEnv(...)` (latest supported minimal equivalent)
2. no explicit `endpoint` env var in host app templates
3. no large event translation layer added
4. SDK APIs used directly at call sites for onboarding/paywall/purchase milestones
5. identity uses SDK methods directly (`identify`/`setUser`/`clearUser`) without extra wrappers
6. `platform` is `web`/`ios`/`android`/`mac`/`windows` or omitted (never framework labels)
7. generated bootstrap sets `identityTrackingMode` explicitly (default `'consent_gated'`)
8. paywall flow reuses a tracker instance per stable paywall context (no per-event tracker re-creation)
9. host-app snippets only use publishable API key env names (no `*WRITE_KEY*` fallback)
10. if provider exposes offering/paywall id, `createPaywallTracker(...)` defaults include `offering`
11. exactly one screen-tracking owner exists per route transition
12. touched onboarding/paywall/purchase call sites emit canonical AnalyticsCLI events only (no legacy aliases, no dual-write)
13. every touched hosted paywall screen emits `paywall:shown` via tracker when shown becomes visible (not only screen-view events)
14. every touched hosted paywall screen maps purchase lifecycle callbacks to tracker methods (`purchaseStarted` + exactly one terminal outcome)
15. every touched paywall dismissal path (close/back/skip) emits tracker `skip(...)`
16. touched onboarding step milestones use dedicated onboarding APIs (tracker step helpers or `trackOnboardingEvent(...)`) instead of generic `track(...)`
17. touched onboarding survey milestones use `trackOnboardingSurveyResponse(...)` (or tracker survey helpers), not ad-hoc generic `track(...)` payloads

## Dashboard Credentials Checklist

Before SDK bootstrap, collect the required values from your dashboard:

- Open [dash.analyticscli.com](https://dash.analyticscli.com) and select the target project.
- In **API Keys**, copy the publishable ingest API key for SDK init.
- If you will verify ingestion with CLI, create/copy a CLI `readonly_token` in the same **API Keys** area.
- Optional for CLI verification: set a default project once with `analyticscli projects select` (arrow-key picker), or pass `--project <project_id>` per command.

## Minimal Web Setup

```ts
import { init } from '@analyticscli/sdk';

const analytics = init({
  apiKey: process.env.NEXT_PUBLIC_ANALYTICSCLI_PUBLISHABLE_API_KEY ?? '',
  platform: 'web',
  identityTrackingMode: 'consent_gated', // default
});
```

`init(...)` accepts:
- shortform string: `init('<YOUR_APP_KEY>')`
- object form: `init({ apiKey: '<YOUR_APP_KEY>', ...optionalConfig })`

`initFromEnv(...)` default env key lookup order:
- API key: `ANALYTICSCLI_PUBLISHABLE_API_KEY`, `NEXT_PUBLIC_ANALYTICSCLI_PUBLISHABLE_API_KEY`, `EXPO_PUBLIC_ANALYTICSCLI_PUBLISHABLE_API_KEY`, `VITE_ANALYTICSCLI_PUBLISHABLE_API_KEY`

If the host app uses custom env naming, set `apiKeyEnvKeys` explicitly.

Missing config behavior:
- default is safe no-op client when API key is missing
- use `missingConfigMode: 'throw'` when startup should fail fast

## React Native Setup

```ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Application from 'expo-application';
import { Platform } from 'react-native';
import { init } from '@analyticscli/sdk';

const analytics = init({
  apiKey: process.env.EXPO_PUBLIC_ANALYTICSCLI_PUBLISHABLE_API_KEY,
  debug: __DEV__,
  platform: Platform.OS,
  appVersion: Application.nativeApplicationVersion,
  identityTrackingMode: 'consent_gated', // default
  storage: AsyncStorage, // optional for RN if you want persistent IDs after consent
});
```

Consent gate for full tracking:

```ts
// user accepts full tracking
analytics.setFullTrackingConsent(true);

// user declines full tracking (strict analytics can continue)
analytics.setFullTrackingConsent(false);
```

There is no "do not start yet" init flag. Tracking starts on `init(...)`; `ready()` (or `initAsync(...)`) is only for explicitly blocking first-flow logic until async storage hydration is done.

## Integration Depth Checklist

The integration should cover more than SDK bootstrap:

1. onboarding flow boundaries and step progression
2. paywall exposure, skip, purchase start, success, fail, cancel
3. screen views for core routes/screens
4. key product actions tied to user value (for example: first calibration complete, first result generated, export/share, restore purchases)
5. stable context properties (`appVersion`, `platform`, `source`, flow identifiers)

## Instrumentation Rules

- Use `createOnboardingTracker(...)` for onboarding flows.
- For onboarding steps in touched flows, prefer `createOnboardingTracker(...).step(...).view()/complete()` over generic `track(...)`.
- For onboarding surveys in touched flows, prefer `trackOnboardingSurveyResponse(...)` or tracker survey helpers over generic `track(...)`.
- Use `createPaywallTracker(...)` when paywall context is stable in a flow (`source`, `paywallId`, experiment variant).
- Keep `createPaywallTracker(...)` instance lifetime aligned to one stable paywall context (for example one screen flow); do not create a new tracker for every paywall event.
- Include `offering` in paywall tracker defaults when available from provider metadata (RevenueCat/Adapty/Superwall).
- Use `trackPaywallEvent(...)` for one-off paywall and purchase milestones.
- Hosted paywall callback mapping is mandatory for touched flows:
  - paywall visible callback -> `paywallTracker.shown(...)`
  - purchase started callback -> `paywallTracker.purchaseStarted(...)`
  - purchase success callback -> `paywallTracker.purchaseSuccess(...)`
  - purchase cancelled callback -> `paywallTracker.purchaseCancel(...)`
  - purchase error callback -> `paywallTracker.purchaseFailed(...)`
  - close/back/dismiss callback -> `paywallTracker.skip(...)`
- Use canonical event names from `ONBOARDING_EVENTS`, `PAYWALL_EVENTS`, and `PURCHASE_EVENTS`.
- Keep `onboardingFlowId`, `onboardingFlowVersion`, `paywallId`, `source`, and `appVersion` stable.
- The SDK built-in dedupe currently applies only to `onboarding:step_view` and is enabled by default (`dedupeOnboardingStepViewsPerSession: true`).
- Prevent duplicate tracking for the same user action across nested layouts/components.
- Use a single tracking owner per route or lifecycle boundary; if multiple hooks can fire, gate with a session-local idempotency key.
- For each paywall attempt, emit each milestone once (`paywall:shown`, `purchase:started`, and one terminal event: `purchase:cancel` or `purchase:failed` or `purchase:success`).

## No-Legacy Policy

For pre-production integrations, do not preserve legacy compatibility by default:

1. Remove legacy analytics providers from touched flows instead of dual-writing.
2. Replace legacy/alias milestone names with canonical AnalyticsCLI events in the same change.
3. Prefer dedicated SDK helpers (`createOnboardingTracker(...)`, `trackOnboardingSurveyResponse(...)`, `createPaywallTracker(...)`) over ad-hoc generic tracking wrappers.

## Validation Loop

After integration or upgrade, verify ingestion with stable CLI checks:

```bash
analyticscli schema events
analyticscli goal-completion --start onboarding:start --complete onboarding:complete --last 30d
analyticscli get onboarding-journey --last 30d --format text
```

## References

- [Onboarding And Paywall Contract](references/onboarding-paywall.md)
- [Minimal Host Template](references/minimal-host-template.md)
- [Storage Options](references/storage.md)
- [Versioning Notes](references/versioning.md)
