---
name: qa-regression-suite
version: 1.0.0
description: Design or prune a regression suite by risk and change surface so it catches regressions without bloating runtime.
author: matrixx0070
tags: [qa, regression, risk, pruning, change-surface]
capabilities: []
---

## When to use

When building a regression suite from scratch, or when an existing one is too slow, too flaky, or full of tests nobody trusts. Regression testing protects what already works from new changes. The goal is maximum defect-catch per minute of runtime — not the largest test count.

**Not for:** testing brand-new functionality (that's the test plan for this release), exploratory bug hunting (see qa-exploratory-charter), or one-off verification. This is about the standing safety net and keeping it lean.

## Method

1. **Seed from risk.** Every High-risk area (money, auth, data integrity, external contracts) gets permanent regression coverage. These earn their runtime regardless of change frequency.
2. **Add by change surface.** Map what the current release touched; ensure each modified path plus its immediate neighbors has a regression test. Decision point: if a change touches a shared module, cover the callers too, not just the change.
3. **Always add a test for every fixed bug** — the canonical regression trigger. A bug that recurs uncaught is a suite failure.
4. **Prune ruthlessly.** Decision point: remove/merge a test if it duplicates coverage, tests dead code, or has never failed meaningfully in a long window. Redundant tests cost runtime and hide signal — but confirm coverage isn't unique before deleting.
5. **Tier for speed:** a fast smoke subset (critical paths, minutes) runs on every commit; the full suite runs pre-release or nightly.
6. **Track flake and value.** Quarantine flaky tests immediately; review low-value tests each cycle. A suite people skip because it's slow or red protects nothing.

## Example

```
Service: payments. Full regression 400 tests / 22 min — devs skip it.
Risk-seed keeps: charge, refund, auth, idempotency (permanent).
Change surface this release: refund path -> add refund-partial + refund-caller tests.
Bug fix #812 (double-charge on retry) -> add regression test.
Prune: 60 duplicate card-format tests -> 8; delete 15 tests for removed coupon module.
Tier: smoke (charge/refund/auth, 90s) on commit; full 300 tests nightly.
```

## Pitfalls

- **Add-only suite** — tests accumulate forever, runtime balloons, devs stop running it.
- **Coverage by count** — 400 shallow tests that miss the money path's edge cases.
- **Deleting without checking uniqueness** — pruning a test that was the only cover for a real path.
- **Ignoring the change surface** — running the same suite every release while modified code goes uncovered.

## Output format

```
Suite scope: <service/area + current size & runtime>
Risk-seeded (permanent): <High-risk areas always covered>
Change-surface additions: <modified paths + neighbors this release>
Bug-fix regressions: <fixed bug -> test added>
Pruned/merged: <removed + why, uniqueness confirmed>
Tiers: smoke (on commit) | full (nightly/pre-release) — runtimes
Flake/value watch: <quarantined + review notes>
```
