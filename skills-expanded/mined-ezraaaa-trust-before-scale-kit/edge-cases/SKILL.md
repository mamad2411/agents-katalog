---
name: edge-cases
description: "Explore states, timings and actors beyond the happy path using the configured core flows."
---

# Edge Cases

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Read `routine.coreFlows` when set. For each changed flow test empty, loading, error, offline,
retry, double submit, concurrent writers, stale state, revoked access, expiry and cancellation.
Ask what else can happen, rather than only whether the intended input works. Trace each plausible
state to an observable outcome. Flag silent data loss, stuck journeys, incorrect results and
missing guards on core flows. Reproduce introduced blockers with a failing test before fixing;
report test command, red proof and green result. With no core-flow registry, name that limitation
and review the reachable changed flow anyway; do not invent a product-wide registry.
