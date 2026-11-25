---
name: csharp-async-quality-gate
description: Use when async and concurrency behavior in C# needs an expert, evidence-first quality decision before merge or promotion.
---

# C# Async Quality Gate

## Specialization

Use this skill to evaluate asynchronous correctness, cancellation behavior, exception flow, and concurrency safety in C# code.

This skill is specialized for async quality decisions and does not implement product features.

## Objective

Produce one deterministic async-quality recommendation with auditable evidence and ranked findings.

## Trigger Conditions

- A change introduces async, await, Task, ValueTask, or IAsyncEnumerable behavior.
- A defect indicates deadlocks, starvation, lost cancellation, or swallowed exceptions.
- A release-bound change needs explicit async-risk disposition.

## Scope Boundaries

In scope:

- Async API contract correctness.
- Cancellation-token propagation checks.
- Exception-flow and failure-surface checks.
- Concurrency and fan-out risk checks.

Out of scope:

- Full performance benchmarking.
- Product feature implementation.
- Non-C# infrastructure workflow execution.

## Inputs

- Target modules and call paths.
- Expected async behavior and failure policy.
- Concurrency assumptions and limits.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Async behavior map for critical paths.
- Findings table with severity and remediation.
- Cancellation and exception-flow verdict.
- Final recommendation: pass, pass-with-conditions, or fail.

## Deterministic Workflow

1. Map async boundaries and identify call-chain fan-out points.
2. Verify cancellation token intake, propagation, and honoring behavior.
3. Verify exception propagation and translation behavior.
4. Evaluate Task vs ValueTask use by contract and call frequency.
5. Check async stream behavior for backpressure and cancellation handling.
6. Rank findings and publish one explicit recommendation.

## Decision Rules

- `pass`: no unresolved critical or high findings.
- `pass-with-conditions`: only medium or low findings remain with owner and due date.
- `fail`: any unresolved critical finding, or high finding in a production path.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert async review | Deterministic Workflow |
| Deterministic quality decision | Decision Rules |
| Auditable findings | Required Outputs |
| Cross-project reusability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Async defects are high-impact and often escape superficial review.
- Cancellation and exception behavior must be explicit to avoid production instability.

Trade-offs:

- Strict async checks increase pre-merge effort but reduce runtime defects.
- Minimal checks increase throughput but can hide failure-mode risk.

Open blockers:

- Missing traceability of async entry points can invalidate conclusions.
- Undefined cancellation policy creates ambiguous pass criteria.

Recommendation:

- Apply this gate to all async changes in shared libraries and production paths.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when async behavior, cancellation flow, and exception flow are explicitly mapped and one recommendation is published.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Decision mode is explicit.
- Source catalog is current for this evaluation cycle.
