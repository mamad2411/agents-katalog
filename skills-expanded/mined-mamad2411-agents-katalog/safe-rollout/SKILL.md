---
name: safe-rollout
description: Design a safe progressive rollout — flags, canary/blue-green, ring stages, SLO health gates, automated rollback, kill switch. Rollout mechanics, not env promotion or A/B experiments.
---

# safe-rollout

> Ship change to users gradually, watch the signals that matter, and make rollback the default reflex — not a heroic incident response.

## When to use

- A change is risky enough that an all-at-once deploy is unwise: large blast radius, new infra, irreversible data path.
- The user asks how to roll out behind a flag, do a canary, or stage a percentage rollout safely.
- A workflow invokes `polymath-release:safe-rollout`.

This designs *rollout mechanics*. It is not promoting a build across environments (`polymath-devops:env-promotion`), running an A/B experiment to learn (`polymath-data:run-experiment` / the `experimentToGA` workflow), or defining the SLO itself (`polymath-sre:slo-design` — consume it here).

## Inputs

- The change and its blast radius (who/what breaks if it's wrong).
- Reversibility: is it flag-toggleable, or does it touch data/schema?
- The SLIs/SLOs that define "healthy" for the affected journey.

## Procedure

1. **Choose the technique** by reversibility and infra:
   - *Feature flag* — app-level, instant off; the default for code-path changes.
   - *Canary / ring* — route a small % (or internal ring) to the new version; widen on health.
   - *Blue-green* — full standby environment; instant cutover + cutback. Use for infra/runtime swaps.
2. **Stage the ramp** — e.g. internal → 1% → 5% → 25% → 100%, with a bake time per stage.
3. **Define health gates** — the SLIs and thresholds that must hold to advance; tie to `polymath-sre:slo-design`. Breach = halt + auto-rollback, not a page-and-wait.
4. **Automate rollback** — flag-off / route-back / redeploy-previous; state the trigger and the expected time-to-safe.
5. **Kill switch** — a single, tested control that disables the change instantly, independent of the deploy pipeline.
6. **Data/irreversibility** — for schema/data changes, pair with expand/contract migration; a flag cannot roll back a destructive write.
7. Output the rollout plan: technique, stages + bake times, health gates, rollback trigger, kill switch, irreversibility notes.

## Quality bar

- Every stage has an explicit advance criterion (a metric + threshold), not "looks fine".
- Rollback is automated and its trigger is a measured signal, not human judgment alone.
- A kill switch exists and is independent of a full redeploy.
- Irreversible (data) changes are called out and not hidden behind a flag that can't actually undo them.

## Anti-patterns

- "Canary" that is one box for five minutes with no health gate (theater).
- Flag with no kill switch or no removal plan (flags become permanent tech debt).
- Rollback that requires a manual redeploy under incident pressure.
