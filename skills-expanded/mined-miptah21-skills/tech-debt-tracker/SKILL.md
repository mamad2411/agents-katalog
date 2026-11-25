---
name: tech-debt-tracker
description: Scan codebases for technical debt, score severity, track trends, and generate prioritized remediation plans. Use when users mention tech debt, code quality, refactoring priority, cleanup sprints, or code health assessment.
---

# Tech Debt Tracker

**Category:** Engineering Process

## Overview

Identify, score, prioritize, and track technical debt across a codebase. Provides a systematic framework for making data-driven decisions about debt remediation vs. feature development.

## When to Use

- Codebase health assessments
- Sprint planning — allocating debt reduction time
- Before major refactors — understand what to prioritize
- New team member onboarding — "where are the landmines?"
- Quarterly engineering reviews

## Debt Classification

### Categories

| Category | Signal Patterns | Impact |
|----------|----------------|--------|
| **Code Debt** | TODOs, FIXMEs, complex functions, duplicated code | Development velocity |
| **Architecture Debt** | Circular deps, god objects, missing abstractions | Scalability, maintainability |
| **Test Debt** | Low coverage, missing edge cases, flaky tests | Reliability, confidence |
| **Dependency Debt** | Outdated packages, known CVEs, abandoned deps | Security, compatibility |
| **Documentation Debt** | Missing docs, outdated READMEs, no architecture docs | Onboarding, knowledge sharing |
| **Infrastructure Debt** | Manual deployments, no monitoring, missing CI steps | Reliability, velocity |

### Severity Scoring

| Score | Level | Criteria |
|-------|-------|----------|
| 1-3 | Low | Cosmetic, doesn't affect functionality |
| 4-6 | Medium | Slows development, increases cognitive load |
| 7-8 | High | Causes bugs, blocks features, hurts reliability |
| 9-10 | Critical | Security risk, data loss potential, system instability |

## Scan Workflow

### Step 1: Automated Signals

```bash
# Count TODO/FIXME/HACK markers
rtk grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMP\|WORKAROUND" src/ --include="*.ts" --include="*.tsx" --include="*.py" | wc -l

# List them with context
rtk grep -rn "TODO\|FIXME\|HACK" src/ --include="*.ts" --include="*.tsx"

# Find long files (>300 lines — potential god objects)
rtk find src/ -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -rn | head -20

# Find large functions (crude heuristic)
rtk grep -c "function\|=>" src/**/*.ts | sort -t: -k2 -rn | head -20

# Duplicated code (if jscpd available)
rtk bunx jscpd src/ --min-lines 10 --min-tokens 50

# Test coverage
rtk test bun test -- --coverage 2>/dev/null | tail -5

# Outdated dependencies
rtk bun outdated 2>/dev/null
```

### Step 2: Manual Assessment

Review and score each finding:

| Item | Category | Severity | Effort | Business Impact |
|------|----------|----------|--------|----------------|
| [description] | Code/Arch/Test/etc | 1-10 | S/M/L/XL | Low/Med/High |

### Step 3: Prioritization

Use **Cost of Delay** framework:

```
Priority Score = (Severity × Business Impact) / Effort

High priority = High severity, high impact, low effort
Low priority = Low severity, low impact, high effort
```

**Prioritization matrix:**

| | Low Effort | High Effort |
|---|-----------|-------------|
| **High Impact** | 🔴 Do First | 🟡 Plan & Schedule |
| **Low Impact** | 🟢 Quick Wins | ⚪ Backlog |

### Step 4: Remediation Plan

```markdown
## Tech Debt Remediation Plan

### Sprint N: Quick Wins (1-2 points each)
- [ ] Fix 15 TODO items in src/services/
- [ ] Remove 3 unused dependencies
- [ ] Add missing error handling in auth flow

### Sprint N+1: Medium Items (3-5 points each)
- [ ] Refactor UserService (450 lines → split into 3 services)
- [ ] Add integration tests for payment flow
- [ ] Update React from 18 to 19

### Quarter Q+1: Major Items (8+ points)
- [ ] Extract shared types into separate package
- [ ] Migrate from REST to tRPC for internal APIs
- [ ] Implement proper caching layer
```

## Report Format

```markdown
## Tech Debt Report: [Project Name]

**Date:** [date]
**Health Score:** 72/100

### Summary
| Category | Items | Avg Severity | Trend |
|----------|-------|-------------|-------|
| Code | 23 | 4.2 | ↑ (was 18) |
| Architecture | 5 | 7.8 | → (stable) |
| Test | 8 | 6.1 | ↓ (was 12) |
| Dependencies | 11 | 5.5 | ↑ (was 8) |
| Documentation | 6 | 3.2 | → (stable) |

### Top 5 Priority Items
1. [Severity 9] Missing auth check on /api/admin/* endpoints
2. [Severity 8] N+1 query in dashboard — 200+ queries per page load
3. [Severity 7] No error boundary in payment flow
4. [Severity 7] 4 critical CVEs in dependencies
5. [Severity 6] UserService is 450 lines with 12 responsibilities

### Recommendations
- Allocate 20% of sprint capacity to debt reduction
- Address all severity 8+ items this quarter
- Schedule dependency update sprint next month
```

## Common Pitfalls

1. **Analysis paralysis** — Don't spend more time analyzing than fixing
2. **Perfectionism** — Some debt is acceptable, manage it
3. **Ignoring business context** — Tie debt to business outcomes
4. **Inconsistent tracking** — Make it part of standard workflow
5. **Over-engineering tools** — Start simple, iterate
