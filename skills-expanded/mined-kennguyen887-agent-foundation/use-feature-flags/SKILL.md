---
name: use-feature-flags
description: Use when gating a code path behind a feature flag or rolling something out gradually — evaluating a flag from a central flag service (scoped by service + flag name + user/session + targeting properties), failing safe (unknown/error/timeout = off), caching the lookup, and choosing a flag over a NODE_ENV/env branch. Covers flag lifecycle (name, owner, removal) and its tie to safe releases. NestJS/TS reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Use feature flags

Gate behaviour behind a runtime flag instead of a redeploy or an environment branch. Examples NestJS/TS,
neutral domain. principle → **▸ Example** → **▸ Other stacks**. Pairs with `release-safety` (flags are
how you ramp + roll back a release) and restates the global *Feature Flags & Observability* rule.

## Core principle
**Gate rollouts on an explicit flag evaluated at runtime, never on `NODE_ENV` or a redeploy — and fail
safe.** A flag turns a feature on/off (or picks a variant) for a user/cohort *without shipping code*; if
the flag service is unreachable or the flag is unknown, the code must fall back to a **safe default
(usually OFF)**, never crash.

## 1. Evaluate against a central flag service (with targeting context)
- A small shared client asks a **central flag/config service** to evaluate a flag, passing the
  **targeting context** — which service is asking, the flag name, and who for (user/session) plus
  optional properties — so the service can do **% rollouts and cohort targeting** centrally.
  ```ts
  // query → central service (message pattern / SDK); response is the decision
  const { isEnabled } = await this.flags.get({
    service: SERVICE_NAME, flagName: 'new-checkout',
    userId, sessionId, properties: { country, plan },   // targeting context for gradual rollout
  });
  if (isEnabled) { /* new path */ } else { /* current path */ }
  ```
- Keep flag **names as constants**, not inline strings; the service owns the rollout %/rules, the caller
  just passes context and branches.
▸ *Other stacks:* LaunchDarkly / Unleash / Flagsmith / OpenFeature SDKs — same shape: `evaluate(flag,
context) → decision`. The central service + targeting context is the point, not the vendor.

## 2. Fail safe + cache
- **Default OFF on any failure** — unknown flag, timeout, or service down → return the safe default and
  log it; a flag-service outage must not break the feature path. (Wrap the call; never let it throw into
  the handler.)
  ```ts
  async isOn(flag: string, ctx: Ctx): Promise<boolean> {
    try { return (await this.flags.get({ flagName: flag, ...ctx })).isEnabled; }
    catch (e) { this.logger.warn('flag eval failed → default off', { flag, e }); return false; }
  }
  ```
- **Cache the evaluation** briefly (per-request, or a short TTL keyed by flag+context) so you don't hit
  the service on every check in a hot path.
▸ *Other stacks:* SDKs stream/cache flag rules locally; if you call a service, add your own short cache +
default. Principle: availability of the flag service is never on the critical path.

## 2b. A flag is not a `NODE_ENV` branch (global rule)
**Never** `if (process.env.NODE_ENV === 'production')` to gate business logic — that's not toggleable,
not targetable, and couples behaviour to where it runs. Use a flag/config value instead. Typical uses:
pick a provider (e.g. which payment gateway), dark-launch a rewrite, enable a feature for a cohort,
kill-switch a flaky integration.

## 3. Flag lifecycle — name it, own it, remove it
- A flag is **temporary scaffolding**. Give it a clear name, record an **owner + a removal condition**
  ("remove after new-checkout is 100% for 2 weeks"), and once fully ramped, **delete the flag and the
  dead branch** — stale flags rot into permanent hidden config. (This is exactly what `release-safety`
  ramps + the comment policy track.)
- Log every flag-driven branch + the fallback path (observability), so you can see which path ran.
▸ *Other stacks:* same discipline — flags have owners and expiry; a "flag debt" review removes ramped flags.

## Verification
- Behaviour is gated on a **named flag evaluated at runtime**, not `NODE_ENV` or a redeploy.
- The eval passes **targeting context** (service + user/session + properties) for gradual rollout.
- Failure/unknown **defaults OFF** (wrapped, logged) and the result is **cached** off the hot path.
- Each flag has an **owner + removal condition**; ramped flags (and their dead branches) get deleted.

## Related
- `release-safety` — flags are how you ramp a release and roll back without a deploy; comment policy for transition code.
- `integrate-internal-services` — the client that calls the central flag/config service (RPC + fail-safe).
- `write-service-code` §7 (log the fallback path) · global *Feature Flags & Observability*, *Anti-patterns (no `NODE_ENV` gating)*.
