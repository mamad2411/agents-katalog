---
name: api-regression-suite
description: Build a fast, reliable API regression suite gated on every PR and nightly, using tagged smoke/full tiers, deterministic data, parallel execution, and trend-based flake detection. Use to catch breakage without slowing delivery.
source: self
date_added: 2026-04-30
---

# API Regression Suite

A regression suite is the safety net that lets teams ship daily. Optimize for **signal, speed, stability** in that order.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Runner | RestAssured (JVM), pytest+httpx, Bruno/Karate, Postman/Newman |
| Parallelism | pytest-xdist, JUnit 5 parallel, k6 scenarios |
| Reporting | Allure 2.x, ReportPortal, JUnit XML |
| Flake tracking | ReportPortal AI, Datadog Test Visibility, Trunk Flaky Tests |
| Data | Testcontainers, factories (Snaplet, Faker), per-test schema |

## Tiering

| Tier | Runs on | Target wall time | Scope |
| --- | --- | --- | --- |
| Smoke | Every PR | ≤ 3 min | Auth, T1 happy paths |
| Regression | Merge-to-main + nightly | ≤ 20 min | All T1+T2 happy + key negative |
| Full | Nightly + release | ≤ 60 min | All tiers, edge cases, soak smoke |

Tag tests (`@smoke`, `@regression`, `@full`) and select via runner filters; never branch logic on environment.

## Reliability Rules

1. **Isolation** — every test creates its own data; no shared mutable fixtures.
2. **Idempotency** — repeated runs are safe; cleanup in `finally`/`afterEach`.
3. **Determinism** — fixed seeds; freeze clocks; mock external time-sensitive APIs.
4. **No sleeps** — poll with timeout + jitter; assert on outcomes not delays.
5. **Independent ordering** — randomize order in CI to detect coupling.

## CI Pattern (GitHub Actions)

```yaml
jobs:
  api-smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew apiTest -Dgroups=smoke -Pparallel=8
      - if: failure()
        run: ./gradlew allureReport && actions/upload-artifact ...
```

PR gate fails on smoke regression; nightly publishes Allure trend + flake report.

## Flake Management

- Quarantine after 2 flakes in 7 days → auto-skip with linked issue + owner.
- SLA: quarantined tests fixed or deleted within 5 working days.
- Track flake rate per suite; target < 0.5%.
- Never `@retry` to mask flakes — find the cause.

## Coverage Without Bloat

- One happy-path test per endpoint.
- Negative paths from the **error catalog**, not invented per endpoint.
- Cross-cutting concerns (auth, pagination, idempotency) tested via parametrised matrices.
- Delete tests when the requirement is gone.

## Common Pitfalls

| Pitfall | Avoidance |
| --- | --- |
| Suite balloons to 60 min on PR | Strict tier gating; profile and prune |
| Tests share DB rows | Per-test namespace/tenant |
| Retries hide flakes | Disable in CI; quarantine instead |
| Manual tests "promoted" without refactor | Reauthor as parametrised, isolated tests |
| No trend visibility | Persist results to ReportPortal/Datadog |

## Output

- Tagged suite with documented runtimes per tier.
- CI gates wired to PR/main/nightly/release.
- Dashboard: pass rate, p95 duration, flake rate, top-flaky tests, MTTR for failed runs.

## References

- ReportPortal — https://reportportal.io/
- Allure — https://allurereport.org/
- Trunk Flaky Tests — https://docs.trunk.io/flaky-tests
- Google Testing Blog — Flaky Tests at Google
- "Software Engineering at Google", chapters on testing
