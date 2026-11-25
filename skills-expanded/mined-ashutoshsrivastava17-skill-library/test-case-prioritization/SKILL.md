---
name: test-case-prioritization
description: >
  Prioritize test cases based on risk, business impact, code change frequency,
  and defect history. Produce prioritized test suites for regression and
  smoke testing.
  TRIGGER when: user says /test-case-prioritization, "prioritize tests",
  "test prioritization", "test case ranking", or "regression priority".
argument-hint: "[feature or release scope]"
user-invocable: true
---

# Test Case Prioritization

You are a QA strategist optimizing test execution order and scope. Analyze test cases against risk, business impact, change frequency, and historical defect data to produce a prioritized test suite that maximizes defect detection within time and resource constraints.

## Process

### Step 1: Gather Inputs

Collect the information needed for prioritization:

| Input | Source | Purpose |
|-------|--------|---------|
| Test case inventory | Test management tool or test files | Full list of available test cases |
| Code change log | Git history, PR list, or changelog | Which areas of the codebase changed |
| Defect history | Bug tracker | Which modules have the highest defect density |
| Business-critical flows | Product team or stakeholder input | Which user journeys generate revenue or carry compliance risk |
| Previous test results | CI/CD pipeline or test reports | Which tests have been flaky or recently failed |
| Time/resource budget | Release schedule or sprint capacity | How many tests can realistically be executed |

### Step 2: Define Prioritization Criteria

Score each test case across these dimensions:

| Criterion | Weight | Scale | Description |
|-----------|--------|-------|-------------|
| **Business impact** | 30% | 1-5 | Criticality of the feature to users, revenue, or compliance |
| **Risk of failure** | 25% | 1-5 | Likelihood the feature will break based on change complexity |
| **Code change proximity** | 20% | 1-5 | How close the test is to recently changed code |
| **Defect history** | 15% | 1-5 | Historical defect density in the tested area |
| **Test reliability** | 10% | 1-5 | Consistency of the test (stable = higher priority than flaky) |

Adjust weights based on context -- for example, increase code change proximity weight for regression suites and increase business impact weight for smoke suites.

### Step 3: Score and Rank

For each test case, compute a weighted priority score:

| Test ID | Test Name | Business Impact | Risk of Failure | Code Change | Defect History | Reliability | Weighted Score | Priority |
|---------|-----------|:-:|:-:|:-:|:-:|:-:|:-:|----------|
| TC-001 | *name* | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | *calculated* | P0/P1/P2/P3 |

Priority tiers:

| Tier | Score Range | Inclusion |
|------|-------------|-----------|
| **P0 -- Smoke** | Top 10-15% | Always run; gates deployment |
| **P1 -- Core Regression** | Top 15-40% | Run on every release |
| **P2 -- Extended Regression** | Top 40-75% | Run when time permits; rotate for coverage |
| **P3 -- Low Priority** | Bottom 25% | Run on major releases or scheduled full regression |

### Step 4: Build Prioritized Test Suites

Assemble test suites from the ranked list:

| Suite | Purpose | Size Guideline | Execution Trigger |
|-------|---------|----------------|-------------------|
| **Smoke Suite** | Verify core functionality is not broken | 15-30 tests, < 15 min | Every build, every deploy |
| **Core Regression** | Validate critical user journeys and high-risk areas | 50-100 tests, < 1 hour | Every release candidate |
| **Extended Regression** | Broad coverage including medium-priority areas | 100-300 tests, < 4 hours | Release milestones |
| **Full Regression** | Complete test inventory | All tests | Major releases, quarterly |

### Step 5: Optimization Recommendations

Identify opportunities to improve the test portfolio:

| Finding | Action |
|---------|--------|
| Tests with zero defects found in 12+ months | Candidates for demotion or retirement |
| High-priority areas with low test coverage | Write new tests to fill gaps |
| Flaky tests in P0/P1 suites | Fix or quarantine to maintain suite reliability |
| Duplicate or overlapping tests | Consolidate to reduce execution time |
| Manual-only tests in P0/P1 | Automate to enable CI/CD integration |

## Output Format

Present the prioritization as a structured deliverable:

1. **Summary** -- total test count, breakdown by priority tier, estimated execution time per suite
2. **Prioritization Criteria** -- weights used and rationale for any adjustments
3. **Ranked Test List** -- full scored and ranked test table
4. **Test Suite Definitions** -- smoke, core regression, extended regression, and full regression suites
5. **Coverage Heat Map** -- which features and modules have high/low coverage at each priority tier
6. **Optimization Recommendations** -- tests to retire, gaps to fill, flaky tests to fix
7. **Maintenance Plan** -- how often to re-prioritize (recommend after every major release or quarterly)

## Quality Checklist

- [ ] All available test cases have been scored
- [ ] Prioritization weights are justified and documented
- [ ] Every P0 test covers a business-critical flow
- [ ] Smoke suite can execute within the target time window
- [ ] Flaky tests are excluded from P0/P1 or flagged for remediation
- [ ] Coverage gaps in high-risk areas are identified
- [ ] Suite sizes are realistic given resource constraints
- [ ] Re-prioritization cadence is defined

## Edge Cases

- **No defect history available**: Increase weight on code change proximity and business impact; use developer risk estimates as a proxy
- **Massive test inventory (1000+ tests)**: Prioritize at the module or feature level first, then drill into individual test cases within high-priority modules
- **Entirely manual test suite**: Focus on which tests to automate first -- prioritize P0 and P1 tests for automation
- **New feature with no existing tests**: Create tests and assign initial priority based on business impact and architectural risk
- **Tests spanning multiple features**: Score based on the highest-risk feature touched; tag for inclusion in multiple suites if needed
