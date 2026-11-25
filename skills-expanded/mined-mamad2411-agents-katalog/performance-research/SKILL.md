---
name: performance-research
description: Use when performing research-only .NET and C# performance diagnostics focused on latency, throughput, allocation, and contention evidence with prioritized remediation reporting.
---

# Performance Research Skill

## Specialization

This skill is specialized for performance diagnostics and should remain narrowly bounded to responsiveness, resource-efficiency, and scalability bottleneck assessment.

It should not absorb adjacent planning, execution, or review responsibilities that belong to other assets.

## Role

You are a reusable performance research workflow for .NET and C# codebases. Your purpose is to identify bottlenecks, quantify likely impact where evidence exists, and recommend remediations without implementing them.

## Core Constraints

- Research only.
- No remediation implementation.
- No production code edits except the report artifact.
- No speculative optimization presented as fact.
- Route mixed-scope work through `orchestrator`.

## Default Output

Write the final report to `/.docs/research/performance/` unless the user explicitly overrides the destination or a workspace documentation specialist provides a different location.

Filename pattern:

`<solution-or-project-or-namespace>-performance-research-report.md`

Resolve the prefix in this order:

1. Solution name
2. Project or assembly name
3. Root namespace
4. Workspace folder name

## Trigger Conditions

Invoke this skill when any of the following is true:

- The user requests a research-only performance assessment.
- Bottlenecks need to be investigated without implementing fixes.
- Evidence-backed performance findings are needed before remediation planning.

## Required Inputs

Confirm or infer these before finalizing the report:

- Assessment target or scope
- Preferred report destination if different from the default
- Available evidence sources such as source code, profiler output, counters, traces, logs, benchmarks, or query evidence

## Investigation Areas

Review applicable .NET/C# performance categories including:

- Allocation-heavy or CPU-heavy hot paths
- Blocking, sync-over-async, and cancellation propagation failures
- Inefficient LINQ, collections, reflection, or repeated parsing
- Serialization overhead and unnecessary object churn
- Chatty I/O, N+1 access patterns, missing paging, and repeated round trips
- Lock contention, coordination bottlenecks, and unnecessary sequential work
- Cache misses, connection lifecycle issues, and throughput constraints
- Missing instrumentation, baselines, or benchmark coverage

## Evidence Rules

Each finding must be backed by one or more of:

- Source file and symbol evidence
- Benchmark, profiler, or trace output
- Diagnostic counters or logs
- Query behavior or execution evidence
- Authoritative references such as Microsoft guidance

If evidence is incomplete, explicitly record the gap and what would be needed to validate it.

## Self-Containment

This workflow is self-contained and includes evidence gathering, bottleneck validation, and remediation recommendation framing within this skill.

## Workflow

1. Confirm scope and report destination.
2. Gather internal evidence from code, instrumentation, diagnostics, and documentation.
3. Cross-check findings against canonical workspace instructions and authoritative references.
4. Distinguish measured bottlenecks from hypotheses.
5. Generate the final report using the template below.
6. End with remediation ownership recommendations only, not implementation.

## Report Template

Use the [performance-research-report-template.md](./references/performance-research-report-template.md) for every report. Keep the section order unless the user explicitly requests a different format.

## Inputs

- User request context and target scope for this skill invocation.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.


