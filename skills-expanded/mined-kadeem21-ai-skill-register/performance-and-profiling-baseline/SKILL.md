---
name: performance-and-profiling-baseline
description: Introduce lightweight profiling and performance hygiene in Python applications. Use when latency or throughput issues appear.
---

# Performance and Profiling Baseline

## Goal
Provide repeatable baseline before optimization changes.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Profiling plan (cProfile and/or py-spy), bottleneck report, and optimization guardrails.

## Verify Gate
Capture baseline metrics and demonstrate impact for at least one critical path.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
