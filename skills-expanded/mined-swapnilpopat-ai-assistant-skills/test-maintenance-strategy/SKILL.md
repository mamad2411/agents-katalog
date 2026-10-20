---
name: test-maintenance-strategy
description: Keep an automation suite fast, green, and trusted as code evolves — quarantine flakes, prune dead tests, refactor selectors, and budget maintenance time. Use when suite signal degrades or growth is unbounded.
source: self
date_added: 2026-05-01
---

# Test Maintenance Strategy

Suites rot if you don't tend them. This skill institutes the practices and budgets that keep your suite a **trusted signal** — not the thing engineers `--no-verify` past at 5pm.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Flake tracking | Currents.dev, Datadog Test Visibility, Allure TestOps, Trunk Flaky Tests, GitHub Actions test summary |
| Quarantine | Annotation (`@Tag("quarantine")`, `test.fixme`, `it.skip`), separate job, must-fix SLA |
| Coverage signal | JaCoCo, c8, Coverage.py — used as a **floor**, not a goal |
| Mutation testing | Stryker (JS/TS), PIT (Java), mutmut (Python), Pitest |
| Selector audit | ESLint Playwright plugin, custom AST scripts |
| Refactor tools | OpenRewrite, codemod, ts-morph |
| Ownership | CODEOWNERS, Trunk-style metadata, Backstage `tests` plugin |

## When to Use

- Suite > 30 min wall clock or > 1% flake rate.
- "Just retry it" has become a culture.
- Every refactor breaks 50 unrelated tests.
- Suite keeps growing; nothing is ever deleted.
- Coverage is up but escaped defects didn't drop.

## The Maintenance Budget

Allocate **15–20% of QA + dev capacity** explicitly to test maintenance. Track it like product work:

- Sprint goal: flake rate ≤ 1%, suite ≤ 10 min, quarantine ≤ 5 tests, 0 tests > 30 days quarantined.
- Maintenance backlog has its own swimlane and is prioritized in planning.
- Treat suite SLOs (duration, flake, coverage) like production SLOs with alerts.

## Practices

1. **Detect flake automatically.** Run each test twice on PR; mark inconsistent as flake. Tools: Currents, Datadog TV, Trunk.
2. **Quarantine, don't ignore.** Move flakes to a quarantine project; it runs but doesn't block. Owner + SLA (e.g., 7 days) attached.
3. **Flake budget alert.** > 1% triggers a Sev-3 on the QA on-call.
4. **Selector hygiene reviews.** Quarterly grep for CSS selectors / brittle XPaths; replace with role/testid.
5. **Prune dead tests.** Tests that never fail and assert nothing meaningful (mutation score 0) → delete.
6. **Mutation testing on critical modules** to expose tests that pass but don't actually verify behavior.
7. **Owner per suite** via CODEOWNERS. PR auto-assigns to owners on test changes.
8. **Refactor with codemods.** When a component renames, update selectors via AST script — not 200 manual edits.
9. **Coverage as floor.** Set min coverage per module; do not treat 100% as a goal.
10. **Suite duration budget.** Each new test must declare its bucket (unit/component/api/E2E); if E2E budget breached, downgrade or merge.

## Code

### Playwright flake annotation + quarantine project

```ts
// playwright.config.ts
projects: [
  { name: 'main',       testIgnore: /\.flaky\./ },
  { name: 'quarantine', testMatch: /\.flaky\./, retries: 2 },
],
```

```ts
test('checkout @flaky reason=infra-2026-04-22 owner=@payments', async () => { /* ... */ });
```

### Mutation testing (Stryker)

```jsonc
// stryker.conf.json
{
  "mutate": ["src/billing/**/*.ts", "!src/**/*.test.ts"],
  "thresholds": { "high": 80, "low": 70, "break": 65 },
  "testRunner": "vitest"
}
```

### Flake detector (PR re-run summary)

```yaml
# .github/workflows/flake-check.yml
- run: npm test -- --reporter=json --outputFile=run1.json
- run: npm test -- --reporter=json --outputFile=run2.json
- run: node scripts/diff-runs.mjs run1.json run2.json >> $GITHUB_STEP_SUMMARY
```

## Pruning Heuristics

Delete or merge a test when **all** are true:

- Touches code unchanged > 12 months.
- Coverage of its target ≥ 95% via other tests.
- Mutation score on its target ≥ 80% without it.
- Has never failed (true positive) in last 6 months.
- Owner agrees in PR review.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| "We'll fix flakes later" | Quarantine + SLA; later never comes |
| Retrying a test 5 times to make it pass | Use 1 retry max + investigate; 5 retries hides bugs |
| Deleting flaky tests | Move to quarantine first; deletion needs owner sign-off |
| Selector refactor by manual edit | Codemod; cheaper, safer, repeatable |
| Coverage as KPI | Track defect escape, MTTR, flake rate too |
| Suite duration unbounded | Budget per layer; reject PRs that breach without trade-off |
| No owner | CODEOWNERS for `tests/**` per service; PR auto-assigns |
| Snapshot-update as default fix | Treat snapshot diff as code review; require justification |

## Output Format (monthly health report)

```
Suite Health — April 2026
  Total tests: 4,820 (+38 / month)
  Wall clock (CI median): 8m12s   target ≤ 10m   ✅
  Pass rate (PR runs): 99.2%      target ≥ 99%   ✅
  Flake rate: 0.7%                target ≤ 1%    ✅
  Quarantine: 4 tests (max age 5d) target ≤ 7d   ✅
  Coverage: 86% line, 79% branch  floor 80/75    ✅
  Mutation score (billing): 82%   target ≥ 80%   ✅
  Top flake offenders:
    1. checkout.refund-flow.spec — async toast race (owner @payments, ETA 2026-05-04)
```

## References

- Google Testing Blog — *Flaky Tests at Google*: <https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html>
- Microsoft — *Detecting Flaky Tests* research papers
- Stryker Mutator: <https://stryker-mutator.io/>
- Trunk Flaky Tests: <https://trunk.io/products/flaky-tests>
- Currents.dev: <https://currents.dev/>
- Martin Fowler — *Eradicating Non-Determinism in Tests*: <https://martinfowler.com/articles/nonDeterminism.html>
