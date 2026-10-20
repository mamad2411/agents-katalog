---
name: feature-flags-rollout
description: Implements feature flags and progressive delivery — kill switches, percentage/targeted rollouts, sticky hashed bucketing, fail-safe evaluation, 1→10→50→100 ramps with guardrail-metric rollback, and TTL-enforced stale-flag cleanup — so changes ship decoupled from deploys and reverse in seconds.
when_to_use: Adding a flag, gating a feature, running a percentage/canary/ring rollout decoupled from deploy, building a kill switch, targeting by user/segment/plan, or paying down flag debt. Covers OpenFeature-compatible managed flag platforms, vendor SDKs, and homegrown flag tables. Distinct from deploy-release (ships the artifact; flags gate behavior inside it) and auth-jwt-session (establishes entitlement; flags must never compute it).
---

## When to Use

Reach for this skill when the request is about **decoupling a behavior change from the deploy that carries it**:

- "Put this behind a flag so we can turn it off without redeploying"
- "Roll it out to 1% / 10% / a canary ring, then ramp"
- "Add a kill switch for the new checkout / payments path"
- "Only enable for plan=enterprise / this segment / our internal allowlist"
- "Migrate from env-var booleans to a managed flag platform / OpenFeature"
- "Clean up dead flags / we have 300 flags and nobody knows which are live"

NOT this skill:
- Shipping/promoting the build, blue-green, canary *infra*, rollback of the artifact → deploy-release
- Deciding *who the user is* or whether they paid → auth-jwt-session (a flag gates rollout; it does not grant entitlement)
- Computing experiment lift / significance / metric tables from exposure logs → write-analytical-sql
- Hiding the provider SDK key / signing flag payloads → secrets-management
- Gating prompt/model changes behind a regression score → llm-eval-harness

## Steps

1. **Classify the flag first — type dictates lifetime, owner, and removal policy.** Do not create a flag without picking one.

   | Type | Purpose | Lifetime | Owner | Removal |
   |---|---|---|---|---|
   | **Release** | Gate in-progress code, ramp it | days–weeks | feature author | **delete at 100% or revert** — TTL-enforced |
   | **Kill switch (ops)** | Instantly disable a risky path | permanent | on-call/SRE | keep; review yearly |
   | **Ops/config** | Tunables (timeouts, batch size, region) | permanent | platform | keep; document |
   | **Experiment** | A/B exposure split | length of test | data/PM | delete when test concludes |
   | **Permission/entitlement** | Plan/role gating | permanent | product | keep — but source of truth is auth, not the flag |

   Release flags are 90% of debt. Every one gets an owner + removal date at creation (step 7). Default any new flag to **release** unless it's clearly a permanent switch.

2. **Pick the evaluation locus — server-side by default.** Evaluate where the decision is *trusted and cheap*.

   | Locus | Use for | Hard rule |
   |---|---|---|
   | **Server** (default) | entitlement-adjacent gating, anything secret, backend behavior | rule logic + flag values never leave the server |
   | **Client** | pure UX (show new button, layout) | only flags in the **public** set; client can lie |
   | **Edge/CDN** | geo/ring routing at the boundary | static rules only |

   **Never evaluate an entitlement or paywall in the browser** — the user controls the client and can flip any client-side flag with devtools. Gate the *capability* server-side; the client flag only hides the UI. Server SDKs evaluate locally against a streamed ruleset (no per-request network call); client SDKs fetch a bootstrapped, scoped flag set.

3. **Define a deterministic key + a fail-safe default.** The default is what runs when the provider is unreachable — and it *will* be unreachable.

   ```ts
   // ONE typed helper, the only place flags are read (step 5).
   export function flag<T>(key: FlagKey, ctx: EvalContext, fallback: T): T {
     try {
       return client.variation(key, ctx, fallback); // local eval, no network
     } catch (e) {
       metrics.increment("flag.eval_error", { key });
       return fallback;                              // FAIL-SAFE: never throw
     }
   }
   // Release flag → fallback = OFF (old code path). Kill switch → fallback = "killed/safe".
   ```

   Rules: a flag read **must not throw, block, or call out per request**. Fall to **last-known-good** (SDK cache) → then the **hardcoded fallback**. For release flags the fallback is the *old* behavior (fail-off). For kill switches the fallback is the *safe* state (path disabled). Never let SDK init failure crash startup — init async with a timeout and serve fallbacks until ready.

4. **Targeting — percentage by stable hashed bucketing, not RNG.** Bucketing must be **sticky**: the same user sees the same variant across requests, servers, and deploys.

   ```ts
   // Deterministic bucket 0..9999 — identical on every server, no shared state.
   function bucket(flagKey: string, unitId: string): number {
     const h = sha1(`${flagKey}:${unitId}`); // salt with flagKey so flags are independent
     return parseInt(h.slice(0, 8), 16) % 10000;
   }
   const inRollout = bucket("new-checkout", user.id) < rolloutPct * 100; // 10% → <1000
   ```

   - **Bucketing unit** = a stable id (userId / accountId / deviceId) — **never** session id, request time, or `Math.random()` (those reshuffle users every request → broken/flickering UX and uninterpretable experiments).
   - Salt the hash with the flag key so two flags at 10% don't hit the *same* 10% of users (correlated rollouts).
   - **Rule order:** allowlist (force-on for QA/internal) → segment/plan rules → percentage → default. First match wins; make precedence explicit.
   - Ramping the percentage must only *add* users, never reshuffle: monotonic threshold on a fixed hash guarantees a user inside 10% stays inside 50%.

5. **Wrap every read behind the one typed helper from step 3.** No raw `client.variation(...)` or `process.env.FEATURE_X` scattered in code. Centralizing gives you: a single fallback policy, one audit point for cleanup, typed keys (no stringly-typed typos), and a place to log exposure for experiments. Key names are namespaced and stable: `team.feature.scope` (e.g. `checkout.new-flow.enabled`).

6. **Ramp on a schedule with a guardrail metric and a one-flip rollback.** Decoupled from deploy means rollback = flip the flag, not redeploy.

   | Stage | Audience | Hold | Watch (guardrail) |
   |---|---|---|---|
   | 0% + allowlist | internal/QA | until smoke passes | manual QA |
   | 1% | canary cohort | ≥1 peak hour | error rate, p99 latency, the feature's own success metric |
   | 10% | — | ≥1 business day | + downstream load, support tickets |
   | 50% | — | ≥1 day | + cost / DB / queue depth |
   | 100% | everyone | bake 1 week | then **delete the flag** (step 7) |

   Pick the guardrail **before** ramping (e.g. "5xx rate must stay <0.5%, checkout-success must not drop >1pp"). Wire an automated trip if you can: guardrail breach → set flag to 0% (kill). A flag flip propagates in seconds; a redeploy does not — that gap is the entire point. Never jump 1%→100%.

7. **Lifecycle = owner + removal date + CI enforcement.** A flag with no expiry is permanent debt.
   - At creation, record `{ owner, type, created, removeBy }` (flag description, a registry table, or `// @flag-owner @removeBy=YYYY-MM-DD` next to the helper call).
   - **CI fails the build when a `release` flag passes its `removeBy`** — grep flag metadata, exit nonzero on any overdue release flag. This is the single highest-leverage anti-debt control.
   - Cleanup is a real PR: delete the flag key in the provider **and** the `flag()` call **and** the now-dead branch — keep the winning path, remove the loser. Archive the flag (don't hard-delete history) so old exposure logs stay interpretable.
   - Kill switches and ops flags are exempt from TTL but get an annual review.

8. **Test both branches; flag-off is the safe default.** Every gated change has two live code paths — both must be tested and shippable. Default the flag **off** in test config (proves old path still works), then run the suite again with it **on**. A PR that only works with the flag on is not done.

## Common Errors

- **`Math.random()` / time / session id as the bucketing unit.** Users flicker between variants every request — broken UX and uninterpretable experiments. Hash a stable user/account id.
- **Two flags at 10% hitting the *same* users.** Forgot to salt the hash with the flag key, so rollouts are correlated. Salt = `flagKey:unitId`.
- **Reshuffling on ramp.** Changing the hash scheme/seed when going 10%→50% moves users *out* of the rollout, regressing them mid-flight. Use a monotonic threshold on one fixed hash.
- **Flag read that throws or blocks.** Provider hiccup takes down the request path. Wrap in the helper; fail to last-known-good then fallback; never network-call per request (server SDKs eval locally).
- **SDK init crashes startup.** Synchronous blocking init against an unreachable provider hangs boot. Init async with timeout, serve fallbacks until ready.
- **Entitlement evaluated client-side.** A client-side flag "unlocks" a paid feature — trivially bypassed in devtools. Gate the capability server-side; the client flag only hides UI (auth-jwt-session owns the grant).
- **Fail-open release flag.** Provider down → fallback is the *new, unfinished* path. Release fallback must be **off** (old path); only ops defaults bias to "on".
- **`process.env.FEATURE_X` booleans.** Env flags need a redeploy to flip — that's a config change, not a runtime kill switch, and defeats decoupling. Use the provider/table behind the helper.
- **Only testing the on-path.** Flag-off regressions ship silently because nobody ran the suite with the flag off. Test both states; off is the default.
- **Flag never removed.** 100% rolled out months ago, both branches still in code, the loser rotting. CI must fail past `removeBy`; cleanup deletes the dead branch.
- **Stale flag still referenced after provider deletion.** Deleting the key in the dashboard but leaving the `flag()` call → it silently serves the fallback forever (often the wrong one). Delete provider key and code in the same PR.

## Verify

1. **Determinism / stickiness:** Evaluate the same flag for the same user id 1000× across ≥2 processes → identical variant every time. Restart the service → still identical.
2. **Independent rollouts:** Two flags at the same percentage do **not** select the same user set (hash is flag-salted) — compare the bucketed cohorts, overlap ≈ percentage², not 100%.
3. **Monotonic ramp:** Take the users inside the 10% rollout; raise to 50% → every one of them is still inside (no user regresses out). Lower back → only the added tail leaves.
4. **Fail-safe:** Block/kill the provider (firewall the SDK endpoint), send traffic → every read returns the fallback, nothing throws, requests still succeed, and `flag.eval_error` is emitted (not silent).
5. **Kill switch latency:** Flip a kill switch to off → the gated path stops within the SDK's stream/poll interval (seconds), with **no deploy**. Time it.
6. **Both branches green:** Full test suite passes with the flag **off** (default) and again with it **on**. CI runs at least the off state.
7. **No raw reads:** `grep -rE "\.variation\(|process\.env\.FEATURE" src/` returns only the single helper file — every other read goes through `flag()`.
8. **TTL enforcement:** A `release` flag with a past `removeBy` makes CI **exit nonzero**. Verify by backdating one in a throwaway branch.
9. **Entitlement is server-trusted:** With the client-side flag forced on in devtools, the server still refuses the gated capability (403/empty), proving the browser can't unlock it.

Done = bucketing is deterministic + flag-salted + monotonic under ramp, every read goes through the fail-safe helper (provider-down test serves fallbacks without throwing), the kill switch flips in seconds with no deploy, both flag branches pass tests with off as default, no entitlement is decided client-side, and CI fails on any release flag past its removal date.
