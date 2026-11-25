---
name: regression-strategy
description: How to maintain and select a regression suite mapped to user-critical flows, choose impact-based scope per change vs full suite before releases, keep a manual smoke checklist, run an escaped-bug feedback loop, and track suite-health metrics. Use when deciding what to re-test after a change or before a release.
---

# Regression Strategy

Regression testing answers one question: did this change break something that used to work? You cannot re-run everything on every change, and you must not skip re-running the things that matter. The strategy is a suite mapped to what users depend on, plus a selection rule that scales scope to risk.

## Maintain a suite mapped to user-critical flows

Keep a living inventory of the flows that hurt most if broken, ranked. First-class citizens, always:

1. **Checkout / payment** — money movement.
2. **Auth** — login, session, password reset, permission boundaries.
3. **Core create/read** of the product's primary object.

Then the next tier (search, notifications, profile, etc.). Each flow entry names the automated test(s) that cover it and the manual steps that don't automate. When a feature ships, its critical path joins this map — the suite grows with the product, not as an afterthought.

## Selection strategy — scale scope to the change

**Per change (impact-based).** Re-run the tests covering **what the diff touches plus its dependents** — the modules that import or call the changed code, the endpoints that hit a changed service, the screens that render a changed component. Derive dependents from the actual dependency graph, not memory. Any critical flow that passes through the touched code runs regardless of how small the change looks.

**Before a release.** Run the **full** regression suite plus the manual smoke checklist. Release boundaries are where accumulated small risks combine; this is not the place to be selective.

**Hotfix.** Impact-based scope around the fix, plus the specific critical flow it affects, plus the smoke checklist for the affected area — fast but never zero.

## Automation-first, with a manual smoke checklist

Automate everything deterministic. But keep a **short manual smoke checklist** for what automation genuinely can't judge:

- Visual polish, spacing, alignment, brand correctness.
- "Feel" — perceived latency, animation smoothness, jank.
- Cross-surface sanity a human notices at a glance.

Keep it short (a few minutes) so it actually gets run. It supplements automation; it does not replace automated functional coverage.

## Escaped-bug feedback loop

Every bug that reached production is a hole in the regression suite. The rule, no exceptions:

> **A production bug gets a failing regression test that reproduces it *before* the fix merges.** The test goes red, the fix turns it green, and it stays in the suite forever.

This is how the suite gets smarter over time and how the same bug never escapes twice. A fix PR that closes a production bug without an accompanying regression test is incomplete — flag it in review.

## Suite-health metrics

A regression suite is infrastructure; monitor it or it rots:

- **Runtime** — total wall clock. When it grows past the point of being run per change, parallelize or tier it. A suite too slow to run provides zero protection.
- **Flake rate** — % of tests that pass/fail non-deterministically. Above a small threshold, trust collapses and people ignore red. Quarantine and fix flakes (see `e2e-web-testing`).
- **Critical-flow coverage** — every flow in the critical map has a current, passing automated test. Gaps here are the highest-priority thing to close.

Report these alongside QA status so suite decay is visible before it bites.

## Anti-patterns

- Re-running only the changed feature's own tests, ignoring dependents.
- Skipping the full suite before a release "because the change was small".
- Fixing a production bug without adding a regression test — guaranteeing it can recur.
- Letting flake rate creep until the suite is ignored.
- A smoke checklist so long nobody runs it.
- No critical-flow map, so selection is guesswork.

## Final step

Record the selected scope (impact-based set or full) and the reason on the issue, run it, and attach results. For any production/escaped bug, confirm the regression test exists and is linked before the fix is allowed to merge.
