---
name: tech-debt
description: >
  Audit a codebase for technical debt, categorize and prioritize findings,
  and create a structured remediation plan with effort estimates.
  TRIGGER when: user says /tech-debt, asks to audit code quality, find
  technical debt, prioritize refactoring, or plan a cleanup effort.
argument-hint: "[codebase path, area, or specific concern]"
user-invocable: true
---

# Technical Debt Audit & Remediation

You are a senior engineer auditing a codebase for technical debt. Identify issues systematically, prioritize by business impact, and create an actionable remediation plan.

## Process

### Step 1: Scope the Audit

Determine audit boundaries:
- Full codebase or specific area/module?
- What is the team's primary concern? (Reliability, velocity, onboarding, performance)
- What is the time horizon for remediation? (Sprint, quarter, year)
- Are there upcoming features that depend on cleaning up specific areas?

### Step 2: Identify Technical Debt

Scan for debt across these categories:

#### Code-Level Debt

| Signal | How to Detect | Impact |
|--------|--------------|--------|
| Dead code | Unused exports, unreachable branches, commented-out code | Confusion, maintenance burden |
| Duplication | Similar logic in multiple places, copy-paste patterns | Inconsistent behavior, fix-one-miss-others |
| Long functions | Functions > 50 lines, high cyclomatic complexity | Hard to test, hard to understand |
| Poor naming | Misleading names, single-letter variables, abbreviations | Onboarding cost, bugs from misunderstanding |
| Missing types | `any` types, missing interfaces, untyped parameters | Runtime errors, weak IDE support |
| Magic values | Hardcoded numbers, strings, URLs without explanation | Fragile, hard to change |
| Deep nesting | 4+ levels of indentation, nested callbacks | Hard to follow, error-prone |
| God classes/modules | Single file doing too many things, 1000+ line files | Hard to test, change, and understand |

#### Architecture-Level Debt

| Signal | How to Detect | Impact |
|--------|--------------|--------|
| Circular dependencies | Import cycles, bidirectional coupling | Hard to change, test, and deploy independently |
| Wrong abstraction | Overly generic code, unused flexibility | Complexity without benefit |
| Missing abstraction | Business logic in controllers, SQL in handlers | Duplication, hard to change |
| Inconsistent patterns | Multiple ways to do the same thing | Confusion, onboarding cost |
| Monolith coupling | Cannot deploy parts independently, shared mutable state | Slow deploys, risky changes |
| Missing boundaries | No clear module interfaces, everything accesses everything | Change ripples unpredictably |

#### Infrastructure & Tooling Debt

| Signal | How to Detect | Impact |
|--------|--------------|--------|
| Outdated dependencies | Major version behind, known CVEs | Security risk, missing features |
| Slow CI/CD | Build takes > 10 minutes, flaky tests | Developer productivity loss |
| Missing automation | Manual deploy steps, manual testing, manual config | Human error, slow releases |
| Poor observability | No structured logging, missing metrics, no alerts | Slow incident response |
| Inconsistent environments | Works locally but not in CI/prod | Debugging time, release risk |
| Missing documentation | No README, stale docs, tribal knowledge | Onboarding cost, bus factor |

#### Test Debt

| Signal | How to Detect | Impact |
|--------|--------------|--------|
| Low coverage | Critical paths untested, coverage < 60% | Regressions ship to production |
| Flaky tests | Tests that pass/fail randomly | CI distrust, ignored failures |
| Slow tests | Test suite > 5 minutes | Developers skip tests, slow feedback |
| Missing integration tests | Only unit tests, no end-to-end verification | Integration bugs in production |
| Test duplication | Same scenario tested in multiple ways | Slow suite, maintenance burden |
| Brittle tests | Tests break on unrelated changes, testing implementation details | Refactoring resistance |

### Step 3: Prioritize Findings

Use this prioritization matrix:

| | High Business Impact | Low Business Impact |
|---|---|---|
| **Low Effort** | **Do First** (Quick wins) | **Do When Convenient** |
| **High Effort** | **Plan & Schedule** | **Defer or Accept** |

**Business impact factors:**
- Blocks or slows feature development
- Causes production incidents
- Increases onboarding time for new engineers
- Creates security or compliance risk
- Affects system reliability or performance

**Effort estimation:**

| Size | Time | Description |
|------|------|-------------|
| XS | < 1 hour | Rename, delete dead code, add a type |
| S | 1-4 hours | Extract function, add missing tests, update a dependency |
| M | 1-3 days | Refactor a module, add integration tests, fix a pattern |
| L | 1-2 weeks | Rearchitect a subsystem, major migration, new abstraction layer |
| XL | 1+ months | Rewrite a service, database migration, framework upgrade |

### Step 4: Create Remediation Plan

```markdown
# Tech Debt Remediation Plan

## Executive Summary
- **Total items found:** [N]
- **Critical (do now):** [N]
- **High (this quarter):** [N]
- **Medium (plan for):** [N]
- **Low (accept or defer):** [N]

## Quick Wins (< 1 sprint)
| Item | Category | Effort | Impact | Owner |
|------|----------|--------|--------|-------|
| | | XS/S | High/Med/Low | |

## Planned Work (this quarter)
| Item | Category | Effort | Impact | Dependencies | Sprint |
|------|----------|--------|--------|-------------|--------|
| | | M/L | High/Med | | |

## Deferred / Accepted Debt
| Item | Reason for Deferral | Revisit Date |
|------|-------------------|-------------|
| | | |

## Principles for Ongoing Debt Management
- [ ] Add tech debt items to the backlog as first-class work items
- [ ] Allocate [X]% of sprint capacity to debt reduction
- [ ] Require debt impact assessment on new feature proposals
- [ ] Run this audit quarterly
```

## Debt Scoring Formula

For each item, compute a priority score:

```
Priority = (Business Impact * 3) + (Frequency of Pain * 2) + (Spread * 1) - (Effort * 2)

Business Impact:  1 (cosmetic) to 5 (causes outages)
Frequency:        1 (rare) to 5 (daily pain)
Spread:           1 (isolated) to 5 (everywhere)
Effort:           1 (trivial) to 5 (months of work)
```

Higher score = fix sooner.

## Edge Cases

- If the codebase has no tests, that is the highest-priority debt — everything else is riskier to fix without tests
- If a major framework upgrade is needed, estimate the cost of NOT upgrading (security patches, community support)
- If debt is concentrated in one area, consider a focused rewrite vs incremental fixes
- For legacy systems with no original authors, prioritize adding documentation and tests before changing code
- Accept that some debt is intentional and acceptable — document the decision and revisit date

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
