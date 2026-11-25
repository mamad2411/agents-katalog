---
name: technical-debt-report
description: Technical debt reporting skill. Combines outputs from 8 sub-analyzers (code quality, test, dependency, architecture, security, performance, documentation, process) into a unified report with A-F grades, severity scoring, and phased remediation plan. Used by the technical-debt-analyzer orchestrator.
origin: AI Dev Kit
---

# Technical Debt Report

Combine findings from 8 sub-analyzers into a unified technical debt report with grading, scoring, and phased remediation.

## When to Use

- The `technical-debt-analyzer` orchestrator has completed all 8 sub-analyses
- A comprehensive codebase health audit is requested
- Pre-refactor baseline assessment is needed
- Onboarding to an unfamiliar codebase

## Report Structure

```markdown
# Technical Debt Report: <project-name>

## Executive Summary
<2-3 sentences: overall grade, top risk, estimated remediation effort>

## Category Grades
| Category | Grade | Debt Points | Weight | Findings |
|---|---|---|---|---|
| Security | | /25 | 0.25 | N |
| Architecture | | /20 | 0.20 | N |
| Test | | /15 | 0.15 | N |
| Code Quality | | /15 | 0.15 | N |
| Dependency | | /10 | 0.10 | N |
| Performance | | /8 | 0.08 | N |
| Documentation | | /4 | 0.04 | N |
| Process | | /3 | 0.03 | N |
| **Total** | | **/100** | 1.00 | N |

## Overall Grade: X
<Grade explanation: A=0-10, B=11-25, C=26-50, D=51-80, F=81+>

## Top Critical Findings
| # | Finding | Category | Score | Effort | Recommendation |
|---|---------|----------|-------|--------|----------------|

## Phase 1: Quick Wins (< 2 days)
| # | Finding | Category | Score | Impact |
|---|---------|----------|-------|--------|

## Phase 2: High Leverage (1 week)
| # | Finding | Category | Score | Impact |
|---|---------|----------|-------|--------|

## Phase 3: Structural (2-4 weeks)
| # | Finding | Category | Score | Impact |
|---|---------|----------|-------|--------|

## Phase 4: Nice-to-Have
| # | Finding | Category | Score | Impact |
|---|---------|----------|-------|--------|

## Trend Analysis
<If previous report exists:>
- Previous grade: X → Current grade: Y (delta)
- Resolved findings: N
- New findings: N
- Trend: improving / stable / degrading

## Appendix: All Findings
<Complete list of all deduplicated findings with full details>
```

## Scoring Methodology

Every finding is scored using:

```
priority_score = severity × blast_radius / effort_to_fix

severity:       1 (cosmetic) → 5 (production-risk)
blast_radius:   1 (isolated) → 5 (system-wide)
effort_to_fix:  1 (5 minutes) → 5 (multi-week)
```

Phase assignment:

```
Phase 1 (Quick wins):     score >= 3.0 AND effort <= 2
Phase 2 (High leverage):  score >= 2.0 AND effort <= 3
Phase 3 (Structural):     score >= 1.0
Phase 4 (Nice-to-have):   score < 1.0
```

## Deduplication Rules

When multiple sub-analyzers flag the same issue:

1. Keep the highest severity rating
2. Merge descriptions from all analyzers
3. Count as one finding (not multiple)
4. Attribute to all detecting analyzers

## Integration with Multi-Agent Workflow

This skill is invoked by the `technical-debt-analyzer` orchestrator after all 8 sub-analyzers complete:

```
[8 Sub-Analyzers Complete] → [technical-debt-report skill] → [Unified Report] → [Micro-Task Decomposer]
```

The unified report feeds into the micro-task decomposition phase, where high-priority debt items can be added as remediation micro-tasks alongside feature implementation.
