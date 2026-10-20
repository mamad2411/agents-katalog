---
name: flaky-test-remediation
description: Detect, quarantine, root-cause, and fix flaky tests using deflake tooling (Trunk Flaky Tests, Datadog Test Visibility, ReportPortal AI), reproducible runs, and async-aware patterns. Use when CI signal is degraded or developers ignore failures.
source: self
date_added: 2026-04-30
---

# Flaky Test Remediation

Flaky tests destroy trust in CI. Treat each flake like a P2 incident: detect, quarantine, root-cause, fix, prevent.

## Stack Baseline (2026)

| Need | Tool |
| --- | --- |
| Detection & quarantine | Trunk Flaky Tests, Datadog Test Visibility, ReportPortal AI, BuildPulse |
| Re-run / bisect | `pytest --reruns` (diagnostic only), `mvn -Dsurefire.rerunFailingTestsCount`, GitHub Actions matrix |
| Reproduce | rr (record-replay), Hermit, deterministic Docker, time-travel debug |
| Async helpers | Awaitility (JVM), `await waitFor` (Testing Library), Cypress retries |

## Causes & Patterns

| Cause | Symptom | Fix |
| --- | --- | --- |
| Async race | Random null/missing element | Poll with explicit condition; never `sleep` |
| Order dependency | Fails only after test X | Randomize order in CI; fix shared state |
| Time/timezone | Fails at midnight UTC | Inject clock; freeze with `@freezegun` / `Clock.fixed` |
| External API | Network timeout | Mock at boundary; record/replay |
| Resource leak | Slows then fails | Close handles in `finally`; CI memory monitor |
| Concurrency | Different worker counts fail differently | Per-test isolation (DB schema, tmp dir) |
| Animation/transition | Element not visible yet | `await locator.waitFor()` or disable animations |
| Snapshot drift | Random IDs in snapshot | Mask volatile fields |

## Triage Workflow

1. **Auto-detect** — deflake tooling tags tests with > 2 conflicting outcomes in 7 days.
2. **Auto-quarantine** — move to skipped suite; CI green, but test still tracked.
3. **File issue** — owner from `CODEOWNERS`; SLA = 5 working days.
4. **Reproduce locally** — run 100× with same seed; if non-repro, run with prod-like load.
5. **Root-cause** — classify (table above); fix the cause, not the symptom.
6. **Re-enable with guard** — require 50 consecutive passes before un-quarantine.
7. **Add prevention rule** — lint rule, helper, or doc to stop recurrence.

## Anti-Patterns

- **Blanket retries** — hides flakes; allow retries only as **diagnostic** signal, not pass-the-build.
- **Sleep instead of poll** — use `Awaitility`/`waitFor` with timeout + interval.
- **Time bombs** — hardcoded dates; tests fail in 2027.
- **Shared mutable state** — singletons, static caches, shared DB rows.
- **Resurrecting tests without fix** — quarantine → fix or delete; never silently re-enable.

## Metrics to Track

- Flake rate per suite (target < 0.5%).
- Mean time to deflake (target < 5 days).
- Quarantined test count + age.
- CI false-failure rate.

## Output

- Quarantine list with owners and ages.
- Root-cause taxonomy report (which categories dominate).
- Trend dashboard: flake rate over time per suite.

## References

- Google Testing Blog — "Flaky Tests at Google and How We Mitigate Them"
- Microsoft Research — "An Empirical Analysis of Flaky Tests"
- Trunk Flaky Tests docs — https://docs.trunk.io/flaky-tests
- Awaitility — http://www.awaitility.org/
