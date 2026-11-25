---
name: test-effectiveness-measurement
description: Measure whether tests actually catch defects — defect detection percentage (DDP), mutation score, escape rate, stability — beyond coverage. Use to evaluate suite quality and target investment.
source: self
date_added: 2026-05-01
---

# Test Effectiveness Measurement

Coverage tells you what code is *executed* by tests; effectiveness tells you what code is *verified*. This skill applies multiple complementary signals so a high-coverage suite isn't mistaken for a high-quality one.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Coverage | JaCoCo, c8, Coverage.py, dotCover, gocover |
| Mutation testing | Stryker (TS/JS), PIT (Java), mutmut (Python), Mull (C/C++), go-mutesting |
| Escape analysis | Defect tracker query — phase_found = prod (per `escaped-defect-analysis`) |
| Stability | Flake rate, retry rate, reproducibility per test |
| Effectiveness composite | DDP, mutation score, leakage trend, MTTD-by-test |
| Storage | Quality dashboard panels |

## When to Use

- Coverage high; defects still escape.
- Investing in a new test suite — measure if it pays off.
- Comparing two suites or two test strategies.
- Deciding what to delete in a maintenance pass.
- Justifying / defending the test budget.

## Core Metrics

### 1. Defect Detection Percentage (DDP)

`DDP = caught_in_phase / (caught_in_phase + escaped_to_later_phase)`

- DDP per phase shows the suite's discriminating power.
- Target unit DDP ≥ 70%, integration ≥ 50%, prod-leakage ≤ 10%.

### 2. Mutation Score

% of artificially introduced bugs your tests catch.

- Targets: critical libs ≥ 80%, application code ≥ 60%.
- Watch *survived mutants* — they reveal weak assertions.

### 3. Escape Rate / Leakage

% of defects discovered in prod / total defects (28-day or per release).

- Targets: tier-1 ≤ 5%; standard ≤ 10%.

### 4. Stability

`stability = 1 - flake_rate`. Unstable tests deliver false positives that cost trust.

- Target ≥ 99%.

### 5. MTTD-by-test

Time from defect introduction (commit) to detection by a test.

- Long MTTD = test exists but ran too late (push earlier in pipeline).

### 6. Composite Health Score

Weighted blend (org-tunable):

```
TestHealth = 0.35 × (1 - leakage)
           + 0.25 × mutation_score
           + 0.20 × stability
           + 0.10 × (DDP_unit + DDP_integration)/2
           + 0.10 × (1 - max(0, suite_p95 - target)/target)
```

Report TestHealth per service; trend on dashboard.

## Mutation Testing — Practical Use

Mutate code, run tests, see which mutants survive (= bugs your tests don't catch).

```jsonc
// stryker.conf.json
{
  "mutate": ["src/billing/**/*.ts", "!src/**/*.test.ts"],
  "testRunner": "vitest",
  "thresholds": { "high": 80, "low": 70, "break": 65 },
  "concurrency": 8,
  "incremental": true
}
```

Investigate survived mutants: if a mutant survives, **add or strengthen an assertion**. Mutation testing is slower than coverage; run on PRs that touch critical paths and nightly across the codebase.

## Coverage Done Right

- **Coverage is a floor**, not a goal. Set per-module floors enforced in CI.
- Combine **line + branch + condition** when supported.
- Diff-coverage on PR (touched lines must reach floor).
- Do not chase 100% — last 10% rarely catches defects, often boilerplate or guards.

## Effectiveness vs. Cost

Plot effectiveness vs. cost per suite/layer:

```
Effectiveness ↑
              │ unit (high effect / low cost)        ← invest more
              │ component                             ← invest more
              │ contract
              │ integration
              │ E2E (medium / high cost)              ← prune; promote signals down
              │ visual (low effect / high cost)       ← scope to design system only
              └────────────────────────────→ Cost
```

## CI Wiring

```yaml
- name: coverage
  run: npm run test -- --coverage --reporter=junit
- name: mutation (changed files)
  run: npx stryker run --files "$(git diff --name-only origin/main...HEAD | grep -E 'src/.*\.ts$' | tr '\n' ',')"
- name: ddp aggregator
  run: node scripts/effectiveness.mjs >> $GITHUB_STEP_SUMMARY
```

## Worked Example

```
Service: orders-api  (period: 90d)
Coverage:    line 86%  branch 78%  ✅
Mutation:    billing 82% ✅  cart 71% ⚠
DDP unit:    74%  ✅
DDP integ:   58%  ✅
Leakage:     11%  ⚠ (target 10%)
Stability:   98.6%  ⚠ (target 99%)
Suite p95:   9m  ✅
TestHealth:  0.79
Notable:    cart mutation gap → assertions weak around discount edges; 12 survived mutants
Action:     strengthen pricing assertions in cart unit suite (owner @sam, ETA 2026-05-15)
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Coverage as KPI | Treat as floor; pair with mutation + leakage |
| 100% coverage chase | Diminishing returns; invest in mutation instead |
| Mutation suite slow | Incremental + scoped to critical libs |
| Stability ignored | Add to composite; flake budget |
| Effectiveness measured per repo only | Per-service for action; team-level for trends |
| One-off measurement | Continuous + dashboard panel |
| Comparing suites without normalizing cost | Plot effectiveness vs. cost |

## Output Format

A per-service "Test Health" panel on the quality dashboard with the metrics above and trend arrows. Quarterly memo identifying suites to invest in vs. prune.

## References

- *Quality Software Project Management* — Futrell et al. (DDP)
- Stryker Mutator: <https://stryker-mutator.io/>
- PIT: <https://pitest.org/>
- Google testing blog — *Mutation testing at scale*
- M. Petrović et al., *On the relation of mutation analysis and code coverage*
- *Software Engineering at Google* — testing chapters
