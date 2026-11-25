---
name: feature-flag-configuration-launchdarkly-and-unleash
description: >
  Designs and operates feature flag configuration with LaunchDarkly or
  Unleash, covering flag lifecycle (create, target, roll out, retire),
  kill-switch patterns for fast incident mitigation without a redeploy,
  targeting/segmentation rules, and cleaning up stale flag debt before it
  accumulates into unreadable conditional logic. Use when the user asks to
  "add a feature flag for X," "set up a kill switch for this feature,"
  "configure LaunchDarkly/Unleash targeting rules," "roll out a flag
  gradually by percentage," "clean up old feature flags," or "should we use
  LaunchDarkly or self-host Unleash."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Feature Flag Configuration (LaunchDarkly and Unleash)

## Purpose

Feature flags decouple *deploying* code from *releasing* a capability:
new code ships dark behind a flag, then gets turned on for a percentage
of traffic, a specific segment, or instantly rolled back — all without a
redeploy. That decoupling is what makes flags valuable operationally, not
just as an A/B-testing convenience: a flag that wraps a risky code path
gives on-call a sub-second kill switch that a `git revert` and redeploy
pipeline cannot match. The operational risk flags introduce is the
opposite failure mode — flag debt. Every flag is a live branch in
production code, and a flag left in place after its rollout is "done"
becomes permanent conditional complexity, a source of confusing bugs
(the flag evaluates differently than anyone remembers), and eventually a
security/compliance question ("why does this old admin-bypass flag still
exist"). This skill covers the flag lifecycle and its cleanup, not just
the initial `if (flag.isEnabled())` wiring.

## When to use

- Introducing a new feature behind a flag so it can be deployed to
  production before it's released to any real users.
- Wrapping a risky code path (a new payment provider integration, a
  rewritten hot path) with a flag specifically so it can be instantly
  disabled — a kill switch — if it misbehaves in production.
- Configuring percentage-based or attribute-based (segment) rollout rules
  so a flag reaches users gradually rather than all-at-once.
- Deciding between LaunchDarkly (managed SaaS) and Unleash (open-source,
  self-hostable) for a team's flagging platform.
- Auditing a codebase or flag dashboard for stale flags that should be
  removed, and safely retiring them.
- Wiring flag evaluation into CI/CD so a deploy and a release become
  independent events (deploy dark, flip the flag separately).

## Prerequisites & environment

- A flagging platform account/instance: LaunchDarkly (SaaS, requires an
  SDK key per environment and a project/environment hierarchy) or Unleash
  (open-source; self-hosted via Docker/Helm, or Unleash's own hosted
  offering — requires a running Unleash server plus a client/frontend API
  token).
- An SDK for each language/runtime that evaluates flags — both platforms
  ship server-side and client-side SDKs; server-side SDKs stream/poll
  flag state and evaluate locally (low latency, no network call per
  evaluation), which is the pattern this skill assumes.
- A defined **flag naming/lifecycle convention** before flags proliferate
  (e.g. `release-`, `experiment-`, `ops-` prefixes signaling expected
  lifetime) — retrofitting a convention onto hundreds of ungoverned flags
  is far more expensive than establishing one at project start.
- For kill-switch use specifically: the flag must be checked in the
  actual failure path (not just at startup/initialization), and the
  flagging platform's own availability/latency must not become a new
  single point of failure — confirm the SDK's local-evaluation/fallback
  behavior (see pitfalls) before relying on a flag as an incident lever.
- Read access to whatever holds flag *definitions* as code if flags are
  managed via Terraform/config-as-code (LaunchDarkly's Terraform provider,
  Unleash's API-driven config) rather than only through a web console.

## Step-by-step guidance

1. **Name and tag every flag with its intended lifetime up front.** A
   flag meant to be removed within weeks (a release/rollout flag) is a
   different governance category than one meant to live indefinitely (an
   ops kill switch or a permanent entitlement flag):
   ```
   release-new-checkout-flow      # temporary — remove after full rollout
   experiment-pricing-page-v2     # temporary — remove after experiment ends
   ops-disable-recommendations    # permanent — kill switch, keep
   entitlement-enterprise-sso     # permanent — plan-gated capability
   ```
   Record the intended removal date/condition in the flag's description
   field in the platform itself (both LaunchDarkly and Unleash support a
   free-text description), not only in a ticket that will be forgotten.

2. **Wrap the flag check at the narrowest point that lets you cleanly
   remove it later**, not scattered through business logic:
   ```javascript
   // LaunchDarkly server-side SDK (Node.js)
   const showNewCheckout = await ldClient.variation(
     "release-new-checkout-flow",
     { key: user.id, custom: { plan: user.plan } },
     false // default value if evaluation fails
   );
   if (showNewCheckout) {
     return renderNewCheckout(user);
   }
   return renderLegacyCheckout(user);
   ```
   ```javascript
   // Unleash server-side SDK (Node.js)
   const { unleash } = require("unleash-client");
   if (unleash.isEnabled("release-new-checkout-flow", { userId: user.id })) {
     return renderNewCheckout(user);
   }
   return renderLegacyCheckout(user);
   ```
   A single evaluation call at the top of the request path (not one call
   per sub-decision inside `renderNewCheckout`) keeps the eventual flag
   removal a small, mechanical diff.

3. **Roll out gradually with percentage or segment targeting rather than
   a single on/off flip**, so a bad release affects a bounded slice of
   traffic before it affects everyone:
   ```json
   // LaunchDarkly targeting rule (simplified)
   {
     "rules": [
       {
         "clauses": [{ "attribute": "plan", "op": "in", "values": ["internal"] }],
         "variation": 0
       },
       {
         "rollout": {
           "variations": [
             { "variation": 0, "weight": 10000 },
             { "variation": 1, "weight": 90000 }
           ]
         }
       }
     ]
   }
   ```
   Start internal-only (dogfood), then 5-10% of real traffic, then
   ramp — watching error rate/latency at each step before increasing the
   percentage, the same staged-rollout discipline covered generically in
   [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md),
   here implemented at the application-logic layer instead of the
   infrastructure-routing layer.

4. **Design kill-switch flags to fail safe on platform unavailability.**
   Both SDKs stream/poll flag state to a local cache and keep serving the
   last-known value (or a supplied default) if the flagging service is
   unreachable — verify which behavior a given flag needs:
   ```javascript
   // Default value is the fail-safe: if LaunchDarkly is unreachable,
   // this evaluates to `false` (recommendations stay ON) rather than
   // throwing or blocking the request.
   const disableRecs = await ldClient.variation(
     "ops-disable-recommendations", context, false
   );
   ```
   For a kill switch specifically, decide deliberately which failure mode
   is safer: defaulting to "feature enabled" (fail open) or "feature
   disabled" (fail closed) depends on what the flag protects — a kill
   switch for a flaky third-party integration should default to
   *disabled* (fail closed) if the flag platform itself can't be reached,
   since the whole point is protecting against the integration being
   unreliable.

5. **Track flag debt as a first-class metric, not an afterthought.** Run
   a periodic audit (scripted against the platform's API) for flags at
   100%/0% rollout for longer than a defined threshold (e.g. 30 days) with
   no experiment/ops tag:
   ```bash
   # Unleash: list flags and their environment states via the Admin API
   curl -s -H "Authorization: ${UNLEASH_ADMIN_TOKEN}" \
     "https://unleash.internal.example.com/api/admin/projects/default/features" \
     | jq '.features[] | {name, stale, lastSeenAt}'
   ```
   Unleash has a built-in `stale` marker surfaced in its UI/API for this
   exact purpose; for LaunchDarkly, use the flag's "code references"
   integration (via `ld-find-code-refs`) plus its dashboard's
   last-evaluated timestamp to spot flags no longer referenced in code but
   still defined.

6. **Retire a flag in two steps, never one**, to avoid a hard cutover
   surprise:
   1. Flip the flag to its final value for 100% of traffic and leave it
      in that state for a full business cycle (covering weekday/weekend
      traffic patterns, batch jobs, etc.) to confirm no dependency on the
      old path remains.
   2. Remove the conditional from code entirely (keeping only the
      winning branch), then archive/delete the flag definition from the
      platform.
      > **Warning:** Deleting a flag definition while code still
      > references it will make the SDK evaluate to the configured
      > default (or throw, depending on SDK/error-handling mode) — always
      > remove the code reference *before* deleting the flag definition,
      > not the other way around.

7. **Manage flag definitions as code where the volume justifies it.**
   LaunchDarkly's Terraform provider and Unleash's OpenAPI-driven admin
   API both allow flag creation/targeting rules to be defined
   declaratively and reviewed in a PR, the same review discipline as
   [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)
   applies to infrastructure:
   ```hcl
   # LaunchDarkly Terraform provider
   resource "launchdarkly_feature_flag" "new_checkout" {
     project_key = "checkout-service"
     key         = "release-new-checkout-flow"
     name        = "New checkout flow"
     description = "Temporary rollout flag — remove after 100% for 2 weeks. Owner: checkout-team."
     variation_type = "boolean"
     variations {
       value = true
     }
     variations {
       value = false
     }
   }
   ```

## Best practices

- Default every new flag's initial state to the *current* (safe,
  pre-change) behavior — a flag that defaults to the new/untested path is
  not actually decoupling deploy from release.
- Give every flag a clearly named owner (team, not individual) and an
  expected removal date in its description — an unowned flag is the one
  that survives three reorgs and nobody remembers what it does.
- Prefer boolean flags for kill switches and simple rollouts; reserve
  multivariate flags (string/JSON variations) for genuinely multi-branch
  decisions (e.g. selecting between three algorithm implementations) —
  multivariate flags used as a substitute for config management add
  complexity without a corresponding operational win.
- Alert on kill-switch flag state changes (a flag flipping off unexpectedly
  in production is itself an incident signal worth a Slack/PagerDuty
  notification, not silent).
- Keep local SDK evaluation (streaming/polling to a local cache) as the
  default rather than a remote evaluation call per request — a
  request-path dependency on the flagging service's live availability
  turns a convenience feature into a new outage cause.
- Test both flag states in CI, not just the one currently rolled out —
  a flag at 100% "on" in production for months can silently rot its "off"
  branch until nobody notices it no longer compiles/works, at which point
  the flag can never be safely used as a rollback lever again.

## Common pitfalls

- **Symptom:** An incident kill-switch flag is flipped off, but the
  service keeps behaving as if it's still on.
  **Fix:** The flag is likely checked once at process startup/cached
  in a long-lived variable rather than evaluated per-request (or the
  SDK's streaming connection silently dropped and fell back to a stale
  cache). Evaluate the flag at the point of use, and confirm the SDK's
  connection/cache-refresh status is itself monitored.

- **Symptom:** A rollout flag has been at 100% for eight months and is
  still in the codebase, and three more flags have since been layered
  on top of the same code path, producing nested conditionals nobody can
  reason about.
  **Fix:** This is flag debt — run the periodic stale-flag audit (step 5)
  and treat "flag has been at a terminal value for N days" as an
  actionable backlog item with the same priority as other tech debt, not
  a someday task.

- **Symptom:** Two flags that are supposed to be mutually exclusive
  (e.g. `release-new-checkout-flow` and `experiment-checkout-v3`) are
  both enabled for the same user, and the resulting behavior is undefined.
  **Fix:** Either consolidate into a single multivariate flag with
  explicit variations, or add an application-level guard that treats
  conflicting flag combinations as an error to alert on rather than
  silently picking one — flag interactions should be designed
  deliberately, not discovered in production.

- **Symptom:** A flag's targeting rule change made in the platform's web
  console during an incident isn't reflected anywhere in version control,
  and nobody can explain a week later why the rule looks the way it does.
  **Fix:** For any flag whose targeting logic matters beyond a quick
  on/off flip, manage the definition via Terraform (LaunchDarkly) or a
  reviewed API script (Unleash) so changes are diffable and reviewable;
  reserve console/dashboard edits for genuine emergency kill-switch flips,
  and follow up with a PR that reconciles code-as-config with whatever was
  changed live.

- **Symptom:** Choosing LaunchDarkly vs. Unleash becomes a stalled debate
  with no clear criteria.
  **Fix:** LaunchDarkly is a managed SaaS with a polished console,
  built-in experimentation/analytics, and per-seat/per-MAU pricing that
  scales with usage — pick it when the team wants flagging to be
  someone else's operational problem and budget allows. Unleash is
  open-source and self-hostable (or available hosted), giving full data
  control and no per-seat cost at the price of running/upgrading the
  Unleash server yourself — pick it when data residency, cost at scale,
  or avoiding a SaaS dependency for a request-path-adjacent system
  matters more than turnkey polish. Both support the same core lifecycle
  in this skill; the choice is an operational-ownership tradeoff, not a
  capability gap.

## Worked example

**Scenario:** A payments team is migrating to a new payment provider
integration. They want it dark-deployed, dogfooded internally, rolled out
gradually, and instantly killable if the new provider misbehaves —
without redeploying.

Flag definitions (LaunchDarkly, managed via Terraform):
```hcl
resource "launchdarkly_feature_flag" "new_payment_provider" {
  project_key    = "payments"
  key            = "release-new-payment-provider"
  name           = "New payment provider integration"
  description    = "Temporary rollout flag. Owner: payments-team. Remove after 100% for 2 weeks (target: 2026-09-01)."
  variation_type = "boolean"
  variations { value = true }
  variations { value = false }
  defaults {
    on_variation  = 1  # false — new path off by default even when flag targeting is "on"
    off_variation = 1
  }
}

resource "launchdarkly_feature_flag" "kill_new_payment_provider" {
  project_key    = "payments"
  key            = "ops-disable-new-payment-provider"
  name           = "Kill switch: force legacy payment provider"
  description    = "Permanent ops kill switch. Fails CLOSED (legacy provider) if unreachable. Owner: payments-team."
  variation_type = "boolean"
  variations { value = true }
  variations { value = false }
}
```

Application code (Node.js, evaluating both flags at the point of use):
```javascript
async function chargeCustomer(order) {
  const killed = await ldClient.variation(
    "ops-disable-new-payment-provider",
    { key: order.merchantId },
    true // fail CLOSED: if LaunchDarkly is unreachable, force legacy path
  );
  const useNewProvider = !killed && await ldClient.variation(
    "release-new-payment-provider",
    { key: order.merchantId, custom: { internal: order.isInternalAccount } },
    false // fail-safe default: legacy provider
  );

  return useNewProvider
    ? newProviderClient.charge(order)
    : legacyProviderClient.charge(order);
}
```

Rollout sequence: internal accounts only (via `internal` targeting
rule) for one week -> 10% of external merchants for three days, watching
the payment-success-rate dashboard at each step -> 50% -> 100%. Two weeks
after reaching 100% with no incident, `release-new-payment-provider` is
removed from code (only the `newProviderClient.charge` branch remains)
and its Terraform resource deleted; `ops-disable-new-payment-provider`
stays permanently as the team's ongoing kill switch for that integration.

## Cross-references

- [gremlin-chaos-engineering-configuration](../gremlin-chaos-engineering-configuration/SKILL.md) — blast-radius scoping and halt conditions for deliberately injected failure, a close cousin of the kill-switch fail-safe design here.
- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the same plan-reviewed, code-as-config discipline applied to flag definitions managed via the LaunchDarkly Terraform provider.
- [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md) — infrastructure-layer progressive rollout that flag-based percentage rollout complements at the application-logic layer.
- [emergency-hotfix-deployment-procedure](../../../devops/skills/emergency-hotfix-deployment-procedure/SKILL.md) — the redeploy-based mitigation path for incidents a kill-switch flag isn't already wired to cover.
