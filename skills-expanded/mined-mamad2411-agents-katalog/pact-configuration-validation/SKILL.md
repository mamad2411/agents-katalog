---
name: pact-configuration-validation
description: >
  Gates deploys on actual contract compatibility using Pact's
  can-i-deploy check and deployment-tracking API — verifying a specific
  consumer or provider version is safe to deploy to a specific
  environment given every other currently-deployed party's contract
  state, wiring can-i-deploy into CI/CD as a real deploy gate, and
  recording deployments so the check stays accurate over time. Use when
  the user asks to "check if it's safe to deploy given our Pact
  contracts," "add a can-i-deploy gate to the pipeline," "validate
  contract compatibility before releasing," or "our contract tests pass
  but we're still not sure it's safe to deploy."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Pact Configuration Validation

## Purpose

Writing and passing consumer/provider contract tests (see
[pact-contract-testing-configuration](../pact-contract-testing-configuration/SKILL.md))
answers "does this provider version satisfy this consumer's contract" in
isolation — it does not by itself answer the deploy-time question that
actually matters: "given everything currently deployed in this specific
environment, is it safe to deploy *this* version right now?" A provider
might satisfy the consumer's *latest* contract while the consumer's
*currently deployed* version still depends on an older, incompatible
contract shape. Pact's `can-i-deploy` check and deployment-tracking API
close that gap by asking the broker the actual, environment-specific
compatibility question at deploy time, and this skill covers wiring that
check into CI/CD as a real, enforced gate rather than treating "provider
verification passed at some point" as sufficient.

## When to use

- Deciding whether a specific build of a consumer or provider service is
  safe to deploy to a specific environment (staging, production) given
  what every other service it interacts with currently has deployed
  there.
- Adding a `can-i-deploy` gate to a deployment pipeline so an
  incompatible version is blocked automatically rather than caught after
  a bad deploy causes integration failures.
- Investigating a case where provider verification passed in CI but a
  deploy still broke consumer/provider compatibility in a real
  environment (usually because the *deployed* consumer version wasn't the
  one whose contract was verified).
- Recording which service versions are actually deployed to which
  environment so the broker's compatibility matrix reflects reality, not
  just "verification happened at some point."

## Prerequisites & environment

- A Pact Broker (or PactFlow) already populated with published consumer
  contracts and provider verification results — see
  [pact-contract-testing-configuration](../pact-contract-testing-configuration/SKILL.md)
  for setting that up; this skill assumes it exists.
- The Pact CLI (`pact-broker` / `pact` CLI, bundled with most Pact
  language SDKs or installable standalone) available in the CI/CD
  pipeline's deploy stage.
- A consistent versioning scheme for both consumer and provider
  deployable artifacts (commit SHA or semantic version) used identically
  when publishing contracts, publishing verification results, and
  running `can-i-deploy` — a mismatch in what "version" means at each
  step breaks the whole check.
- Environment names in the broker that match the pipeline's actual
  environment names (`staging`, `production`) used consistently when
  recording deployments — see
  [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md).

## Step-by-step guidance

1. **Run `can-i-deploy` as a required, blocking step immediately before
   the actual deploy action**, not as an informational check that's
   logged but ignored:
   ```bash
   pact-broker can-i-deploy \
     --pacticipant order-service \
     --version "$(git rev-parse --short HEAD)" \
     --to-environment production \
     --broker-base-url "$PACT_BROKER_URL" \
     --broker-token "$PACT_BROKER_TOKEN"
   ```
   This asks the broker: "given every provider that `order-service`
   depends on and that is currently recorded as deployed to
   `production`, is *this* `order-service` version compatible with all
   of them?" A non-zero exit code means the deploy should not proceed —
   wire it as a pipeline gate whose failure blocks the deploy job, the
   same way a failing test would.

2. **Check compatibility in both directions** — a consumer being deployed
   needs to check compatibility against currently-deployed providers, and
   a provider being deployed needs to check against currently-deployed
   consumers, so a provider change that breaks an existing consumer is
   caught before the provider ships, not only when the consumer next
   deploys:
   ```bash
   # inventory-service (provider) checking it's safe to deploy given
   # every consumer currently deployed to production
   pact-broker can-i-deploy \
     --pacticipant inventory-service \
     --version "$(git rev-parse --short HEAD)" \
     --to-environment production \
     --broker-base-url "$PACT_BROKER_URL"
   ```

3. **Record every successful deploy back to the broker immediately
   after it completes**, so the next `can-i-deploy` check has an
   accurate picture of what's actually live — a stale deployment record
   makes the check either falsely permissive (checking against a version
   that's no longer deployed) or falsely restrictive (blocking a
   compatible deploy because the broker still thinks an old, incompatible
   version is live):
   ```bash
   pact-broker record-deployment \
     --pacticipant order-service \
     --version "$(git rev-parse --short HEAD)" \
     --environment production \
     --broker-base-url "$PACT_BROKER_URL"
   ```
   Place this call right after the deploy step succeeds, in the same
   pipeline job, so it can never be skipped independently of the deploy
   actually happening.

4. **Handle a failed `can-i-deploy` check as a real deploy block, with a
   clear message about which contract is incompatible**, not a check
   that's silently bypassed under time pressure:
   > **Warning:** Treating a failed `can-i-deploy` result as advisory and
   > deploying anyway defeats the entire purpose of contract validation —
   > if there is a genuine emergency requiring an override, treat it with
   > the same explicit, logged, accountable-approval discipline as any
   > other emergency gate bypass (see
   > [emergency-hotfix-deployment-procedure](../../../devops/skills/emergency-hotfix-deployment-procedure/SKILL.md)),
   > never a silent skip.
   The broker's output names the specific incompatible pact
   (consumer/provider version pair), which should be surfaced directly in
   the pipeline's failure output so the responsible team knows exactly
   what to fix.

5. **For services that deploy independently across multiple
   environments (staging, then production), run `can-i-deploy` at each
   promotion step**, checked against that specific target environment —
   compatibility in staging does not guarantee compatibility in
   production if the two environments have different versions currently
   deployed:
   ```bash
   pact-broker can-i-deploy --pacticipant order-service --version "$SHA" \
     --to-environment staging ...
   # ...later, promoting the same build to production:
   pact-broker can-i-deploy --pacticipant order-service --version "$SHA" \
     --to-environment production ...
   ```

6. **Use `can-i-deploy`'s "pending pacts" / "WIP pacts" features
   deliberately** when a provider team wants early visibility into an
   in-progress consumer contract without blocking the provider's normal
   deploys on a contract that isn't finalized yet — this avoids the
   common failure mode of provider teams disabling contract validation
   entirely because an in-progress consumer change kept blocking
   unrelated provider deploys.

## Best practices

- Run `can-i-deploy` as a hard gate in the deploy job itself, immediately
  before the deploy action, not as a separate report someone checks
  manually.
- Record every deployment back to the broker in the same pipeline run
  that performed it — an out-of-band or manual deployment-recording step
  will eventually be forgotten and silently stale the compatibility data.
- Check `can-i-deploy` in both consumer and provider directions for
  every service that plays both roles, so a breaking provider change is
  caught before *it* ships, not only when its consumers next deploy.
- Keep environment names in the broker in lockstep with the pipeline's
  real environment names — a mismatch here silently makes every
  `can-i-deploy` check meaningless.
- Use WIP/pending-pact features for in-progress consumer contracts so
  provider teams aren't forced to choose between being blocked on
  unfinished work and disabling the gate outright.
- Never treat a failed `can-i-deploy` result as something to bypass
  silently — route any genuine override through the same explicit,
  accountable emergency process as any other deploy gate.

## Common pitfalls

- **Symptom:** `can-i-deploy` reports "safe to deploy" but the deploy
  still breaks integration with a service that was, in fact, already
  deployed.
  **Fix:** Almost always a stale deployment record — the broker thinks
  an old version of the other service is deployed because
  `record-deployment` wasn't called after its last deploy (step 3);
  audit whether every service's deploy pipeline actually calls
  `record-deployment` on success, not just on the service being checked.

- **Symptom:** A provider team disables Pact verification/`can-i-deploy`
  entirely because an in-progress consumer contract keeps blocking their
  unrelated deploys.
  **Fix:** Use pending/WIP pact support (step 6) so an unfinished
  consumer contract doesn't block the provider's normal deploys, instead
  of removing the gate altogether and losing protection against real
  breaking changes too.

- **Symptom:** `can-i-deploy` passes in staging, and the team assumes
  it's therefore also safe for production, but the production deploy
  still breaks compatibility.
  **Fix:** Run `can-i-deploy` separately against each target environment
  (step 5) — staging and production frequently have different versions
  of dependent services currently deployed, so compatibility in one
  doesn't imply compatibility in the other.

- **Symptom:** Under release pressure, someone deploys despite a failed
  `can-i-deploy` check "because the contract change looks harmless."
  **Fix:** Treat this the same as bypassing any other deploy gate under
  pressure — it must go through an explicit, logged, accountable
  emergency-override process (step 4), never a silent manual bypass,
  since "looks harmless" is exactly the judgment `can-i-deploy` exists to
  replace with an actual check.

- **Symptom:** Two services use different version identifiers when
  publishing contracts versus when running `can-i-deploy` (e.g., a
  semantic version tag in one place and a commit SHA in another).
  **Fix:** Standardize on one version identifier scheme (commit SHA is
  simplest and always unique) and use it consistently across contract
  publish, verification publish, `can-i-deploy`, and
  `record-deployment` calls — a mismatch here makes the broker unable to
  correlate records correctly.

## Worked example

**Scenario:** `order-service` (consumer) is ready to deploy build `a1b2c3`
to production, where `inventory-service` (provider) is currently running
build `f9e8d7`.

1. Deploy pipeline for `order-service` runs, immediately before the
   deploy step:
   ```bash
   pact-broker can-i-deploy --pacticipant order-service --version a1b2c3 \
     --to-environment production --broker-base-url "$PACT_BROKER_URL"
   ```
2. The broker checks: does `order-service@a1b2c3`'s published contract
   have a successful verification result recorded against
   `inventory-service@f9e8d7` (the version currently recorded as deployed
   to `production`)? Yes — the check passes, deploy proceeds.
3. Immediately after the deploy succeeds, the pipeline calls:
   ```bash
   pact-broker record-deployment --pacticipant order-service --version a1b2c3 \
     --environment production --broker-base-url "$PACT_BROKER_URL"
   ```
   so the broker now shows `order-service@a1b2c3` as the current
   production version.
4. Two days later, `inventory-service` prepares to deploy build `g1h2i3`
   to production, which renamed a response field in a way that breaks
   compatibility with `order-service@a1b2c3`'s contract (no verification
   result exists for that pair). Its pipeline runs
   `can-i-deploy --pacticipant inventory-service --version g1h2i3
   --to-environment production` and gets a failing result, naming the
   specific incompatible contract with `order-service`. The deploy is
   blocked automatically — the breaking change is caught before it ships,
   not discovered as a production incident.

## Cross-references

- [pact-contract-testing-configuration](../pact-contract-testing-configuration/SKILL.md) —
  writing the consumer/provider tests and publishing the contracts and
  verification results that `can-i-deploy` reads.
- [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md) —
  the gated promotion flow `can-i-deploy` plugs into as one more required
  check before a build moves to the next environment.
- [emergency-hotfix-deployment-procedure](../../../devops/skills/emergency-hotfix-deployment-procedure/SKILL.md) —
  the only acceptable path for overriding a failed `can-i-deploy` result
  under genuine time pressure, handled explicitly rather than silently
  bypassed.
