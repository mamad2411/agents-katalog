---
name: tech-debt
description: Technical debt identification, prioritization, and strategic repayment planning.
---

# Tech Debt Skill

## Purpose

To transform **silent code rot** into **managed, prioritized backlog items**. This skill provides a systematic approach to identifying, quantifying, and scheduling technical debt repayment—preventing the "big bang" rewrite and enabling sustainable development velocity.

**ROI Metric**: Addressing debt early costs 1x. Addressing it late costs 10x. Ignoring it costs 100x (failed projects).

## When to Use

- **Trigger**: When velocity is slowing down (features taking longer).
- **Trigger**: When `reflexion` identifies recurring issues.
- **Trigger**: Before major feature work ("Clean the campsite first").
- **Trigger**: When code complexity metrics exceed thresholds.
- **Trigger**: When `pm-agent` schedules a "debt sprint."

## The Debt Management Protocol (The 4-Step Process)

### 1. Identification (Where Is The Debt?)

**Scan for these debt signals:**

| Signal | Detection Method | Example |
|:-------|:-----------------|:--------|
| **Code Smells** | Static analysis, complexity metrics | Functions >50 lines, nested conditionals >3 levels |
| **Outdated Dependencies** | `npm outdated`, `cargo outdated` | React 16 when 18 is available |
| **Missing Tests** | Coverage reports | Critical path has <50% coverage |
| **Documentation Drift** | Doc vs code comparison | API docs don't match implementation |
| **Workarounds** | Code comments (`// HACK`, `// FIXME`) | Temporary fixes that became permanent |
| **Performance Issues** | Profiling, metrics | Page load >3s, API latency >500ms |
| **Security Vulnerabilities** | `npm audit`, SAST scans | Known CVEs in dependencies |

### 2. Quantification (How Bad Is It?)

Score each debt item across three dimensions:

**Impact (1-10)**: How much does this hurt?
- Development velocity
- System reliability
- Security posture
- User experience

**Effort (1-10)**: How hard to fix?
- Lines of code to change
- Files affected
- Dependencies to update
- Tests to write
- Risk of breaking changes

**Interest Rate (1-10)**: How fast is it growing?
- How often does this code change?
- How many new features touch this area?
- How many workarounds are being added?

**Debt Score = Impact × Interest Rate / Effort**

Higher score = Pay this debt first.

### 3. Categorization (What Type Of Debt?)

| Category | Description | Example | Typical Action |
|:---------|:------------|:--------|:-------------|
| **Design Debt** | Architectural shortcuts | God class, tight coupling | Refactor with ADR |
| **Code Debt** | Implementation shortcuts | Copy-pasted code, long methods | Refactor incrementally |
| **Test Debt** | Missing or poor tests | No integration tests | Write tests before changes |
| **Documentation Debt** | Outdated or missing docs | API changes not documented | Update docs as you go |
| **Dependency Debt** | Outdated libraries | React 16 in 2026 | Scheduled upgrade |
| **Infrastructure Debt** | Ops shortcuts | Manual deploys | Automate via IaC |
| **Skill Debt** | Team knowledge gaps | No one knows GraphQL | Training + pairing |

### 4. Scheduling (When Do We Pay?)

**Strategies:**

**A. Debt Sprints (20% Rule)**
- Reserve 20% of every sprint for debt repayment.
- Pay highest-scored debt items first.
- Track debt burndown like feature burndown.

**B. Boy Scout Rule**
- "Leave the code better than you found it."
- Small improvements with every feature PR.
- Limit: 10-20% of PR scope should be cleanup.

**C. Before New Features**
- Clean debt in the area you're about to modify.
- Prevents building on shaky foundations.

**D. Scheduled Maintenance**
- Quarterly dependency updates.
- Bi-annual architecture reviews.
- Annual security audits.

## Debt Item Template

```markdown
# Tech Debt Item: [TITLE]

## Summary
**ID**: DEBT-XXX  
**Category**: [Design/Code/Test/Doc/Dependency/Infra/Skill]  
**Filed Date**: YYYY-MM-DD  
**Status**: Identified | Scheduled | In Progress | Paid

## Problem Statement
[What is the debt? What are the symptoms?]

[Example: The UserService class has grown to 2000 lines and handles authentication, profile management, and preferences. Changes require touching 15+ methods.]

## Impact Assessment

| Dimension | Score (1-10) | Justification |
|:----------|:------------:|:--------------|
| **Impact** | 8 | Every user feature touches this class. Changes are slow and error-prone. |
| **Effort** | 6 | Requires splitting into 3-4 services. Estimated 3 days. |
| **Interest Rate** | 9 | We add 2-3 new user features per sprint. Debt grows fast. |

**Debt Score**: (8 × 9) / 6 = **12.0** [Pay Immediately: >10]

## Symptoms
- [ ] Feature X took 5 days instead of 2
- [ ] Bug Y introduced because of tight coupling
- [ ] Developer onboarding takes 3 days to understand UserService
- [ ] Tests are flaky due to too many responsibilities

## Proposed Solution
[What should we do to pay this debt?]

[Example: Split UserService into AuthService, ProfileService, and PreferenceService. Each <300 lines.]

### Steps
1. [ ] Step 1: Create ProfileService, move profile methods
2. [ ] Step 2: Update tests for ProfileService
3. [ ] Step 3: Create PreferenceService, move preference methods
4. [ ] Step 4: Update tests for PreferenceService
5. [ ] Step 5: Refactor UserService to AuthService only
6. [ ] Step 6: Update all imports and calls
7. [ ] Step 7: Verify all tests pass

## Risks & Mitigations
- **Risk**: Breaking changes to API → Mitigation: Maintain backward-compatible wrapper during transition
- **Risk**: Tests need major rewrite → Mitigation: Write new service tests before migration

## Payment Schedule
- **Strategy**: Before New Feature
- **Scheduled Sprint**: Sprint 12 (when we build User Preferences v2)
- **Owner**: @backend-team
- **Estimated Effort**: 3 days

## Notes
- **Related PRs**: #123, #456
- **Related ADRs**: ADR-002 (Service Boundaries)
- **Outcome (when paid)**: [To be filled]
```

## Execution Template

*Use this when running a debt audit.*

```markdown
## 🔍 Tech Debt Audit: [Scope]

### 1. Scan Results

| ID | Category | Location | Impact | Effort | Interest | Score | Priority |
|:---|:---------|:---------|:------:|:------:|:--------:|:-----:|:--------:|
| D-001 | Design | UserService.ts | 8 | 6 | 9 | 12.0 | HIGH |
| D-002 | Dependency | React 16.x | 6 | 4 | 7 | 10.5 | HIGH |
| D-003 | Test | auth/ | 7 | 3 | 6 | 14.0 | HIGH |
| D-004 | Code | utils/helpers.js | 4 | 2 | 3 | 6.0 | MEDIUM |

### 2. High Priority Items (Score >10)

#### D-003: Missing Auth Tests
**Problem**: Authentication flows have 23% test coverage.  
**Impact**: Every auth change risks regression.  
**Solution**: Write integration tests for all auth flows.  
**Effort**: 2 days  
**Schedule**: Next sprint (Sprint 11)

### 3. Payment Plan

**This Sprint (Sprint 10)**
- [ ] D-004: Refactor utils/helpers.js (1 day)
- Feature work: 80%
- Debt work: 20%

**Next Sprint (Sprint 11)**
- [ ] D-003: Auth test coverage (2 days)
- [ ] D-002: React upgrade planning (1 day)
- Feature work: 70%
- Debt work: 30%

**Following Sprint (Sprint 12)**
- [ ] D-001: Split UserService (3 days)
- Feature work: 60%
- Debt work: 40%

### 4. Debt Metrics
- **Total Items**: 4
- **High Priority**: 3
- **Estimated Total Effort**: 12 days
- **Debt Burndown Target**: 0 high-priority items by end of Q2
```

## Debt Register

Maintain a central debt register:

```markdown
# Technical Debt Register

## Active Debt
| ID | Title | Category | Score | Status | Owner | Target Sprint |
|:---|:------|:---------|:-----:|:-------|:------|:-------------:|
| D-001 | UserService too large | Design | 12.0 | Scheduled | Backend | 12 |
| D-002 | React 16 outdated | Dependency | 10.5 | Scheduled | Frontend | 11 |
| D-003 | Auth tests missing | Test | 14.0 | In Progress | Quality | 11 |

## Recently Paid
| ID | Title | Category | Paid Date | Effort | Outcome |
|:---|:------|:---------|:----------|:-------|:--------|
| D-000 | Legacy API wrapper | Code | 2026-01-15 | 2 days | API response time -30% |
```

## Integration with Agents

- **`architect`**: Identifies design debt, creates ADRs for major refactors.
- **`backend` / `frontend`**: Identifies code debt during implementation.
- **`quality`**: Identifies test debt from coverage reports.
- **`pm-agent`**: Schedules debt sprints, tracks debt burndown.
- **`reflexion`**: Surfaces recurring issues that become debt items.

## Anti-Patterns (Avoid)

- ❌ **"We'll fix it later"** without scheduling → Becomes permanent
- ❌ **Big Bang Rewrite** → High risk, hard to validate
- ❌ **Perfect is Enemy of Good** → Don't gold-plate while debt accumulates
- ❌ **Debt Amnesty** → Don't ignore debt because "it's always been there"
- ❌ **Paying Low-Score Debt First** → Focus on high-impact, high-interest debt
