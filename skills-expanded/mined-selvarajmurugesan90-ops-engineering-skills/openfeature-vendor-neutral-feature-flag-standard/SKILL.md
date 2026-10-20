---
name: openfeature-vendor-neutral-feature-flag-standard
description: >
  Guides adopting the OpenFeature specification and SDKs as a
  vendor-neutral abstraction layer over feature flag providers
  (LaunchDarkly, Unleash, Flagsmith, a config file, or a homegrown
  service) — provider architecture, evaluation context design, hooks for
  cross-cutting logging/metrics, and swapping or multi-provider testing
  without touching application call sites. Use when the user asks to
  "use OpenFeature instead of a vendor SDK directly," "avoid vendor
  lock-in for feature flags," "abstract our flag evaluation behind a
  standard interface," "swap our flag provider without rewriting call
  sites," or "add an OpenFeature hook for flag evaluation logging."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# OpenFeature: Vendor-Neutral Feature Flag Standard

## Purpose

Calling a feature-flag vendor's SDK directly from application code
(`ldClient.variation(...)`, `unleash.isEnabled(...)`) works fine until
the organization needs to switch vendors, run two providers side by
side during a migration, or simply wants flag-evaluation logic that
doesn't leak a specific vendor's method names and object shapes through
every call site in the codebase. **OpenFeature** (a CNCF specification
with SDKs for most major languages) solves this the same way SLF4J
solved logging-framework lock-in: application code calls one standard
API (`client.getBooleanValue(...)`, evaluation context, hooks), and a
swappable **provider** underneath does the actual evaluation against
whichever vendor or homegrown system is configured — LaunchDarkly,
Unleash, Flagsmith, a static config file provider for tests, or an
in-house flag service, all through the identical call-site shape. This
skill covers OpenFeature's provider architecture, evaluation context
design, and hooks — it is the abstraction *layer*, distinct from
[feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md),
which covers the flag lifecycle, rollout, and kill-switch discipline
*within* a specific vendor and applies equally whether that vendor sits
behind OpenFeature or is called directly.

## When to use

- Starting a new project's feature-flag integration and wanting to avoid
  hardcoding a specific vendor's SDK into every call site from day one.
- Migrating from one flag provider to another (LaunchDarkly to Unleash,
  or either to a homegrown system) and wanting the migration to be a
  provider swap, not a call-site rewrite across the whole codebase.
- Running two providers side-by-side temporarily during a vendor
  migration or evaluation, without maintaining two entirely separate
  code paths.
- Writing tests that need deterministic flag values without depending on
  a real vendor SDK/network call.
- Adding cross-cutting behavior around every flag evaluation — logging,
  metrics, tracing span attributes — without threading that logic
  through every call site individually.
- Deciding whether OpenFeature is worth the abstraction for a given
  team's size/vendor-commitment level, versus calling a vendor SDK
  directly.

## Prerequisites & environment

- An OpenFeature SDK for the application's language (Java, .NET,
  Go, JavaScript/Node.js, Python, PHP, Ruby SDKs are all part of the
  CNCF project) — the specification itself defines the API shape every
  language SDK implements, so the concepts transfer directly even though
  package names differ per language.
- A **provider** implementation for whichever underlying flag system is
  actually in use — most major vendors (LaunchDarkly, Unleash,
  Flagsmith, Split, ConfigCat) publish an official or community
  OpenFeature provider; confirm one exists and is maintained for the
  target vendor and language before assuming OpenFeature adds zero
  integration work.
- The vendor/provider-specific setup already done underneath (an
  Unleash server running, a LaunchDarkly project/environment
  configured) — OpenFeature does not replace
  [feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md)'s
  setup, it sits on top of it.
- Clarity on what belongs in the **evaluation context** (the equivalent
  of a vendor SDK's "user context" or "targeting key" object) — a
  stable identifier (user ID, request ID) plus whatever attributes
  targeting rules key on (plan tier, region, internal-account flag),
  designed once as a shared shape across the application rather than
  built ad hoc per call site.
- OpenFeature 1.x SDKs (the specification reached a stable 1.0 across
  major language SDKs) — check the specific language SDK's own
  changelog for provider-interface breaking changes between minor
  versions before pinning an exact version.

## Step-by-step guidance

1. **Install the OpenFeature SDK and a provider for the current
   vendor**, and set the provider once at application startup — this is
   the one place vendor-specific configuration lives:
   ```javascript
   // Node.js: OpenFeature core SDK + the Unleash provider
   const { OpenFeature } = require('@openfeature/server-sdk');
   const { UnleashProvider } = require('@openfeature/unleash-provider');

   await OpenFeature.setProviderAndWait(
     new UnleashProvider({
       url: 'https://unleash.internal.example.com/api',
       appName: 'checkout-service',
       instanceId: 'checkout-service-1',
       clientKey: process.env.UNLEASH_CLIENT_KEY,
     })
   );
   ```
   ```javascript
   // swapping to LaunchDarkly later touches only this one setup block,
   // not any of the call sites in step 2
   const { LaunchDarklyProvider } = require('@openfeature/launchdarkly-provider');
   await OpenFeature.setProviderAndWait(
     new LaunchDarklyProvider(process.env.LAUNCHDARKLY_SDK_KEY)
   );
   ```

2. **Evaluate flags through the standard client API**, never importing a
   vendor SDK directly in application/business logic:
   ```javascript
   const client = OpenFeature.getClient();

   const showNewCheckout = await client.getBooleanValue(
     'release-new-checkout-flow',
     false, // default value if evaluation fails
     { targetingKey: user.id, plan: user.plan }
   );

   if (showNewCheckout) {
     return renderNewCheckout(user);
   }
   return renderLegacyCheckout(user);
   ```
   This call site is identical whether the provider underneath is
   Unleash, LaunchDarkly, or a static-file provider used in tests — the
   whole point is that this code never needs to change when the
   provider does.

3. **Design a shared evaluation context shape used consistently across
   every call site**, rather than each call site inventing its own ad
   hoc context object:
   ```javascript
   function buildEvaluationContext(user, request) {
     return {
       targetingKey: user.id,       // stable identifier every provider needs
       plan: user.plan,
       region: request.region,
       internalAccount: user.isInternalAccount,
     };
   }

   const context = buildEvaluationContext(user, request);
   const showNewCheckout = await client.getBooleanValue('release-new-checkout-flow', false, context);
   const useNewProvider = await client.getBooleanValue('release-new-payment-provider', false, context);
   ```
   A consistent context shape is what actually makes a provider swap
   painless later — if half the call sites pass ad hoc, inconsistent
   attribute names, the underlying provider's targeting rules (however
   they're re-created against a new vendor) have nothing reliable to key
   on.

4. **Use hooks for cross-cutting behavior around every evaluation** —
   logging, metrics, or tracing span attributes — instead of wrapping
   every individual call site by hand:
   ```javascript
   const { OpenFeature } = require('@openfeature/server-sdk');

   const loggingHook = {
     after: (hookContext, details) => {
       logger.info('flag evaluated', {
         flag: hookContext.flagKey,
         value: details.value,
         reason: details.reason,
         targetingKey: hookContext.context.targetingKey,
       });
     },
     error: (hookContext, error) => {
       logger.error('flag evaluation failed', { flag: hookContext.flagKey, error });
     },
   };

   OpenFeature.addHooks(loggingHook);
   ```
   A hook registered once at the client (or global) level applies to
   every subsequent evaluation automatically — this is the OpenFeature
   equivalent of the "flag evaluation should be observable" guidance in
   [feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md),
   implemented once instead of per call site.

5. **Use the in-memory/static-file provider for deterministic tests**,
   rather than mocking the vendor SDK or hitting a real flag service in
   CI:
   ```javascript
   const { InMemoryProvider } = require('@openfeature/in-memory-provider');

   await OpenFeature.setProviderAndWait(new InMemoryProvider({
     'release-new-checkout-flow': { variants: { on: true, off: false }, defaultVariant: 'off', disabled: false },
   }));
   ```
   Testing against the real vendor SDK's mock/test mode still works, but
   the in-memory provider removes any dependency on that specific
   vendor's testing conventions from the test suite itself.

6. **Run two providers side-by-side only as a deliberate, time-boxed
   migration step**, using OpenFeature's multi-client support (a
   named client bound to a specific provider) rather than a permanent
   dual-provider architecture:
   ```javascript
   // during a LaunchDarkly -> Unleash migration: the "old" domain still
   // reads from LaunchDarkly while newly-migrated flags read from Unleash
   await OpenFeature.setProviderAndWait('legacy', new LaunchDarklyProvider(ldKey));
   await OpenFeature.setProviderAndWait('unleash', new UnleashProvider({ url, appName }));

   const legacyClient = OpenFeature.getClient('legacy');
   const newClient = OpenFeature.getClient('unleash');
   ```
   Treat this dual-provider state as a migration in progress with an
   end date, not a permanent architecture — the goal is a single
   provider per environment once the migration completes.

7. **Decide deliberately whether OpenFeature's abstraction is worth it
   for a given team.** The abstraction pays off clearly when a vendor
   switch or multi-provider period is a real, foreseeable scenario, or
   when many services across an org need a consistent flag-evaluation
   interface regardless of which team picked which vendor. It's a real
   but smaller cost — one more dependency, one more layer to understand
   — for a single small service with no plausible vendor-switch
   scenario on the horizon, where calling the vendor SDK directly (per
   [feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md))
   may be the simpler, sufficient choice.

## Best practices

- Set the provider exactly once, at application startup, and never
  import a vendor-specific flag SDK anywhere else in the codebase —
  this is the entire point of the abstraction, and a single stray
  direct import defeats it for that call site.
- Design and share one evaluation-context-building function/shape across
  the codebase rather than letting each call site construct its own
  context ad hoc — consistency here is what makes a future provider
  swap actually painless.
- Register hooks for logging/metrics/tracing once rather than wrapping
  individual `getBooleanValue`/`getStringValue` calls by hand across the
  codebase.
- Use the in-memory/static-file provider for unit and CI tests so test
  suites don't depend on network access to a real flag backend or on a
  specific vendor's test-mode conventions.
- Treat a dual-provider setup as a bounded migration state with a target
  end date, not a long-term architecture — consolidating back to one
  provider per environment keeps the system's actual complexity in
  check.
- Keep the flag lifecycle/governance discipline (naming conventions,
  stale-flag audits, kill-switch fail-open/fail-closed design) from
  [feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md)
  fully in force underneath OpenFeature — the abstraction layer changes
  *how* application code calls into flags, not the operational
  discipline needed around flag lifecycle itself.

## Common pitfalls

- **Symptom:** A "vendor swap" turns into a large codebase-wide rewrite
  anyway, despite using OpenFeature.
  **Fix:** Some call sites were bypassing OpenFeature and calling the
  vendor SDK directly (often for a vendor-specific feature OpenFeature's
  common API doesn't expose, like a vendor's specific experimentation
  analytics call). Audit for direct vendor SDK imports outside the
  provider-setup code, and either find the OpenFeature-standard
  equivalent or explicitly document the vendor-specific escape hatch as
  a deliberate, isolated exception rather than letting it spread.

- **Symptom:** After swapping providers, targeting rules that worked
  correctly under the old vendor evaluate inconsistently or incorrectly
  under the new one, even though the flag names match.
  **Fix:** The evaluation context attributes passed at call sites were
  never consistent to begin with (step 3) — one part of the codebase
  passed `plan`, another passed `tier` for the same concept, and the old
  vendor's targeting rules happened to tolerate the inconsistency in
  ways the new provider's rule engine doesn't. Standardize the
  evaluation context shape across the codebase before or during a
  provider migration, not after problems surface.

- **Symptom:** A test suite is flaky or slow because it depends on
  reaching a real flag backend over the network.
  **Fix:** Tests are using the real provider instead of the in-memory/
  static-file provider (step 5). Swap the provider in test setup/bootstrap
  code specifically, keeping the real provider only for actual
  integration tests that deliberately want to exercise the network path.

- **Symptom:** A default value passed to `getBooleanValue` silently
  becomes "the" behavior in production because the provider never
  successfully initializes, and nobody notices for a while.
  **Fix:** This mirrors the vendor-level "fail-safe default" pitfall in
  [feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md)
  — a default value is a legitimate fail-safe, but a provider that never
  actually connects (a misconfigured Unleash URL, an invalid
  LaunchDarkly SDK key) evaluating every single flag to its default is
  a silent, standing degradation, not a one-off. Add a hook (step 4) or
  provider-status check that alerts specifically when the provider is
  in a not-ready/error state, rather than only ever seeing individual
  evaluation results.

- **Symptom:** Adding OpenFeature to a small, single-service project
  with one flag and no foreseeable vendor change adds a dependency and a
  layer of indirection with no apparent payoff.
  **Fix:** This is a case where OpenFeature's abstraction cost may
  genuinely outweigh its benefit (step 7) — it's not free, and a small
  project calling a vendor SDK directly per
  [feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md)
  is a legitimate, simpler choice; reserve OpenFeature for genuine
  multi-service or plausible-vendor-switch scenarios rather than
  applying it as a default on every project regardless of size.

## Worked example

**Scenario:** A platform team standardizes on OpenFeature across
services currently split between LaunchDarkly (older services) and
Unleash (a newer, cost-motivated self-hosted choice), and plans to
consolidate everything onto Unleash within two quarters.

Provider setup (`checkout-service`, currently on LaunchDarkly, migrating
to Unleash):
```javascript
const { OpenFeature } = require('@openfeature/server-sdk');
const { LaunchDarklyProvider } = require('@openfeature/launchdarkly-provider');
const { UnleashProvider } = require('@openfeature/unleash-provider');

// Phase 1: still on LaunchDarkly, but already behind OpenFeature
await OpenFeature.setProviderAndWait(new LaunchDarklyProvider(process.env.LAUNCHDARKLY_SDK_KEY));
```

Application call sites, unaffected by the provider migration:
```javascript
const client = OpenFeature.getClient();

function buildContext(user, request) {
  return { targetingKey: user.id, plan: user.plan, region: request.region };
}

async function chargeCustomer(order, user, request) {
  const context = buildContext(user, request);
  const useNewProvider = await client.getBooleanValue(
    'release-new-payment-provider', false, context
  );
  return useNewProvider
    ? newProviderClient.charge(order)
    : legacyProviderClient.charge(order);
}
```

Logging hook registered once, capturing every evaluation regardless of
which underlying provider is active:
```javascript
OpenFeature.addHooks({
  after: (hookContext, details) => {
    metrics.increment('flag_evaluation', { flag: hookContext.flagKey, value: String(details.value) });
  },
});
```

Migration day: the target environment's flags are recreated in Unleash
with matching targeting rules using the same `plan`/`region` context
attributes (consistent because `buildContext` was shared from the
start), and the provider setup line becomes:
```javascript
await OpenFeature.setProviderAndWait(
  new UnleashProvider({ url: process.env.UNLEASH_URL, appName: 'checkout-service' })
);
```
No call site, hook, or test in `checkout-service` changes — the
migration is entirely contained in the one provider-setup block, and
the same in-memory-provider-backed test suite continues to pass
unmodified throughout.

## Cross-references

- [feature-flag-configuration-launchdarkly-and-unleash](../feature-flag-configuration-launchdarkly-and-unleash/SKILL.md) — the flag lifecycle, rollout, and kill-switch discipline that applies underneath OpenFeature regardless of which provider is active; this skill is the abstraction layer on top, not a replacement for that operational discipline.
- [pact-contract-testing-configuration](../pact-contract-testing-configuration/SKILL.md) — a comparable "avoid coupling to one specific implementation's exact interface" discipline, applied to service contracts rather than flag providers.
- [infrastructure-post-deployment-validation-and-smoke-testing](../infrastructure-post-deployment-validation-and-smoke-testing/SKILL.md) — where a provider-status/evaluation-health check from this skill's hooks could be wired into a post-deploy smoke test.
