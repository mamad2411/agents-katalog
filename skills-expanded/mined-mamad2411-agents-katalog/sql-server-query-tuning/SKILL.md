---
name: sql-server-query-tuning
description: Use when diagnosing or improving SQL Server query performance with execution-plan evidence, indexing trade-offs, Query Store signals, and regression-safe validation.
---

# SQL Server Query Tuning

## Specialization

Use this skill to tune slow or regressed SQL Server queries with plan-level evidence, workload context, and the smallest safe change that materially improves performance.

This skill is specialized for query tuning, not broad server-health triage or general SQL standards review.

## Objective

Produce one evidence-backed tuning recommendation, apply the smallest viable change, and prove whether it improved the targeted query or workload slice without introducing uncontrolled regressions.

## Trigger Conditions

- A query, stored procedure, or workload slice is slow, regressed, or unstable.
- Query Store, wait stats, or execution plans indicate a query-level bottleneck.
- Indexing, parameter sensitivity, or cardinality-estimation choices need expert review.
- A team needs a repeatable query-tuning workflow that is safe across projects.

## Scope Boundaries

In scope:

- Query text, stored procedures, views, and indexing decisions tied to the target workload.
- Query Store, estimated/actual plan, memory grant, cardinality, and parameter sensitivity evidence.
- One chosen tuning path with regression-aware validation.

Out of scope:

- Broad estate inventory and server build checks.
- Identity, encryption, and audit hardening.
- Full HA/DR design.
- Generic SQL style guidance when no performance issue exists.

## Inputs

- Target query, procedure, or workload slice.
- Engine version, compatibility level, and database settings.
- Baseline symptoms: duration, CPU, reads, waits, concurrency profile, or user-visible impact.
- Available evidence: Query Store, plans, XE traces, wait data, or reproducible test case.

## Required Outputs

- Bottleneck classification with explicit evidence.
- One recommended tuning path with rejected alternatives.
- Validation plan and success criteria.
- Residual regression risks and rollback path.
- Pragmatic stop decision that states whether the tuning pass is complete.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Improve one isolated statement | One query has a confirmed bottleneck and one validated improvement |
| L2 Delivery | Fix one production-facing query issue | Duration, CPU, logical reads, or concurrency impact improves against baseline |
| L3 Hardening | Reduce regression risk across workload slice | Query Store, plan stability, and index side effects are explicitly evaluated |
| L4 Expert Standardization | Institutionalize repeatable tuning practice | Reusable evidence contract, option pruning, and validation rubric are documented |

## Evidence Contract

Collect the strongest available combination of:

- Query text or procedure body.
- Actual execution plan when possible; estimated plan only when actual is unavailable.
- Query Store runtime and plan-history evidence when available.
- Baseline metrics: duration, CPU, reads, writes, memory grant, row counts, and waits.
- Index footprint and write-side trade-offs for every index proposal.

## Deterministic Workflow

1. Lock scope to one target query or tightly bounded workload slice.
2. Establish baseline metrics and the user-visible failure mode.
3. Classify the dominant bottleneck: bad cardinality, poor indexing, parameter sensitivity, excessive memory grant, spills, parallelism friction, or blocking side effect.
4. Build a short option set and reject weak options early.
5. Choose one smallest viable change: query rewrite, index change, stats action, compatibility adjustment, or plan-stability action.
6. Validate improvement against baseline using the same measurement surface.
7. Check regression risk: write amplification, storage growth, plan stability, and adjacent query behavior.
8. Publish one recommendation with evidence, rejected options, and rollback notes.

## Option Selection Rules

- Prefer query and predicate correctness before adding indexes.
- Prefer one targeted index over overlapping index sprawl.
- Treat forced plans and hints as controlled exceptions, not defaults.
- Do not accept superficial gains that materially worsen write cost or plan stability without explicit approval.
- Require selectivity, cardinality, and row-goal reasoning for significant indexing or rewrite recommendations.

## Rejected Candidate Reasons

Use these deterministic reason codes when pruning options:

- `R1`: Fixes the symptom but not the dominant bottleneck.
- `R2`: Adds excessive write or storage cost.
- `R3`: Depends on unstable hints or brittle plan forcing.
- `R4`: Requires scope expansion beyond the agreed slice.
- `R5`: Evidence is too weak to justify the change.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Evidence-first diagnosis | Evidence Contract |
| One clear recommendation | Deterministic Workflow steps 4 to 8 |
| Explicit trade-off handling | Option Selection Rules + Rejected Candidate Reasons |
| Regression-aware validation | Required Outputs + Deterministic Workflow steps 6 and 7 |
| Cross-project reusability | Depth Modes + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- The slow path can be isolated to a query or small workload slice.
- Baseline metrics are comparable before and after changes.

Trade-offs:

- Aggressive indexing may improve reads while increasing write cost and maintenance overhead.
- Plan forcing can stabilize regressions quickly but may hide deeper optimizer or stats issues.

Open blockers:

- Missing plans or Query Store history weakens root-cause confidence.
- Unclear workload concurrency can make single-query wins misleading.

Recommendation:

- Default to the smallest evidence-backed query or index change, and require before/after proof on the same measurement surface before widening scope.

## Source Governance Summary

- Active sources, evaluation date, and guidance deltas are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active source checks.

## Reference Assets

- Use [query-tuning-evidence-template.md](./references/query-tuning-evidence-template.md) to capture baseline metrics, chosen change, rejected options, and before/after validation.

## Pragmatic Stop Rule

Stop when one dominant bottleneck has a validated improvement, rejected alternatives are recorded, and the remaining risks are smaller than the original performance problem.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete and evidence-backed.
- One recommendation is chosen and rejected options are recorded.
- Validation and rollback expectations are explicit.
- Source catalog is current for this evaluation cycle.
