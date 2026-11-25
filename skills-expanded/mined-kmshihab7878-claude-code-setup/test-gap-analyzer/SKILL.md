---
name: "test-gap-analyzer"
description: "Automated test coverage gap detection and targeted test generation. Analyzes codebase for untested functions, uncovered branches, missing edge cases, and regression gaps. Produces prioritized test generation targets ranked by bug risk. Use when assessing test coverage, finding untested code, planning test sprints, or running the Quality department's UAOP self-improvement loop."
risk: low
tags: [quality, testing, analysis, coverage]
created: 2026-03-23
updated: 2026-03-23
---

# Test Gap Analyzer — Quality Intelligence Engine

Automated coverage gap detection that feeds the Quality department's UAOP loop. Find what's untested, rank by risk, generate tests for the highest-risk gaps first. This is UAOP Stage 1 (Intelligence) + Stage 5 (Self-Improvement) for Quality.

## When to use

- Before a release — "are we covered?"
- After adding new features — "what's untested?"
- After a production bug — "why didn't our tests catch this?"
- Sprint planning — "what should we test next?"
- Monthly quality review — "where are we improving, where are we regressing?"

## When NOT to use

- Writing individual tests (use `test-driven-development`)
- Debugging a specific failure (use `debug`)
- Reviewing test methodology (use `testing-methodology`)

## Pipeline

### Step 1: Coverage Scan

Run coverage tools and collect raw data:

```bash
# Python coverage
python -m pytest tests/ --cov=src/coremind --cov-report=json --cov-report=term-missing -q

# Frontend coverage
cd frontend && npx vitest run --coverage

# E2E coverage (count vs. critical user flows)
# Compare existing E2E tests against documented user flows
```

Extract:
- **Line coverage %** — per module, per file
- **Branch coverage %** — conditional paths not exercised
- **Uncovered functions** — public functions with zero test coverage
- **Uncovered files** — entire files with no tests

### Step 2: Risk-Rank Gaps

Not all gaps are equal. Rank by bug risk:

```
RISK SCORE = (Complexity × Change Frequency × User Impact) / Existing Coverage

Where:
  Complexity:       High (10) = many branches, external calls, state mutation
                    Medium (5) = moderate logic
                    Low (1) = simple getters, constants

  Change Frequency: Count of git commits touching this file in last 90 days

  User Impact:      Critical (10) = auth, payments, data mutation, API endpoints
                    High (7) = core business logic, agent execution
                    Medium (4) = internal utilities, helpers
                    Low (1) = dev tools, scripts, docs

  Existing Coverage: 0-100% (inverted — lower coverage = higher priority)
```

### Step 3: Classify Gap Types

| Gap Type | Description | Priority | Test Type Needed |
|----------|-------------|----------|-----------------|
| **Critical path uncovered** | Auth, payments, data mutation with 0% coverage | P0 | Unit + integration |
| **High-change no-test** | Files changed >5x in 90 days with <50% coverage | P0 | Regression tests |
| **Branch gaps** | Conditional paths (error handling, edge cases) never exercised | P1 | Edge case + property-based |
| **API contract gaps** | Endpoints without request/response validation tests | P1 | Contract tests |
| **E2E flow gaps** | Critical user journeys without end-to-end tests | P1 | E2E (Playwright) |
| **Integration gaps** | DB/Redis/external API interactions untested with real deps | P2 | Integration tests |
| **Regression gaps** | Production bugs that had no test (and still don't) | P0 | Regression tests |
| **Flaky tests** | Tests that pass/fail non-deterministically | P1 | Fix or quarantine |

### Step 4: Produce Gap Report

```markdown
# Test Gap Report — [Date]

## Coverage Summary
| Suite | Current | Target | Delta | Status |
|-------|---------|--------|-------|--------|
| Python (pytest) | [X]% | 80% | [+/-Y]% | [OK/GAP] |
| Frontend (Vitest) | [X]% | 80% | [+/-Y]% | [OK/GAP] |
| E2E (Playwright) | [X/Y flows] | all critical | [N missing] | [OK/GAP] |
| API contracts | [X/Y endpoints] | all public | [N missing] | [OK/GAP] |

## Top 10 Gaps by Risk Score

| Rank | File/Function | Gap Type | Risk Score | Coverage | Recommendation |
|------|--------------|----------|------------|----------|---------------|
| 1 | [path:function] | [type] | [score] | [%] | [test type + approach] |

## Regression Debt
[List of production bugs without regression tests]

## Flaky Test Report
[List of flaky tests with failure rate and last occurrence]

## Improvement Trend
| Metric | Last Month | This Month | Delta |
|--------|-----------|------------|-------|
| Line coverage | [X]% | [Y]% | [+/-Z]% |
| Branch coverage | [X]% | [Y]% | [+/-Z]% |
| Bug escape rate | [X] | [Y] | [+/-Z] |
| Flaky test count | [X] | [Y] | [+/-Z] |
```

### Step 5: Generate Test Targets

For each P0 gap, produce a test specification:

```markdown
## Test Target: [File:Function]

**Gap type:** [Critical path / High-change / Branch / etc.]
**Risk score:** [X]
**Current coverage:** [X]%
**Why it matters:** [What could go wrong if this isn't tested]

### Tests to Write
1. `test_[function]_happy_path` — [expected behavior]
2. `test_[function]_returns_error_when_[condition]` — [error handling]
3. `test_[function]_handles_[edge_case]` — [boundary condition]
4. `test_[function]_with_[invalid_input]` — [input validation]

### Test Approach
- Pattern: [AAA / Property-based / Contract / E2E]
- Dependencies: [Real DB / Mock external / Fixture]
- Estimated effort: [S/M/L]
```

### Step 6: Self-Improvement Loop (UAOP Stage 5)

After tests are written and run:

```
MEASURE:
  - Did new tests catch any existing bugs? (validation)
  - What's the coverage delta? (progress)
  - Any new flaky tests introduced? (quality)
  - Bug escape rate trend (effectiveness)

REINFORCE:
  - Test patterns that caught real bugs → prioritize more of these
  - Files that keep needing more tests → flag for refactoring
  - Coverage plateaus → switch from unit to property-based/mutation testing

REGENERATE:
  - Update gap report with new coverage data
  - Re-rank remaining gaps
  - Feed into next sprint's test targets
```

## Cadence

```
WEEKLY:
  Monday:  Run coverage scan + produce gap report
  Tuesday: Prioritize top 5 gaps for the sprint
  Sprint:  Write tests targeting gaps
  Friday:  Re-scan, measure improvement, feed into next week

MONTHLY:
  Trend analysis — are we improving?
  Flaky test cleanup sprint
  Regression debt review
```

## Tools Used

| Tool | Purpose |
|------|---------|
| pytest --cov | Python line + branch coverage |
| vitest --coverage | Frontend coverage |
| playwright | E2E test execution |
| github MCP | PR coverage diffs, change frequency |
| code-review-graph MCP | Blast radius analysis for risk ranking |
| sequential MCP | Multi-step gap analysis reasoning |

## Agents

| Agent | Role |
|-------|------|
| quality-engineer (L2) | Owns the gap analysis, sets priorities |
| tester (L6) | Writes tests targeting identified gaps |
| test-results-analyzer (L6) | Analyzes results, identifies flaky tests |
| code-reviewer (L6) | Reviews test quality before merge |
| debugger (L6) | Investigates why gaps exist (missing test or untestable code?) |

## UAOP Integration

```
Stage 1 (Intelligence):  Coverage scan → gap identification → risk ranking
Stage 2 (Context):       Load quality/domain.md + quality/rules.md before any test writing
Stage 3 (Generation):    Produce test targets → write tests in parallel
Stage 4 (Split):         Auto-generated unit tests (T0) vs. human-designed E2E (T1)
Stage 5 (Loop):          Measure coverage delta → reinforce patterns → regenerate targets
```

## Quality KPIs (Self-Improvement Metrics)

| Metric | Target | Alert |
|--------|--------|-------|
| Line coverage | >80% | Drops below 75% |
| Branch coverage | >70% | Drops below 65% |
| Bug escape rate | <5% | Rises above 10% |
| Flaky test count | 0 | Any new flaky test |
| Regression debt | 0 | Any prod bug without regression test |
| Time to first test (new code) | Same PR | Tests in separate PR |
