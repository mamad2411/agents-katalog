---
name: observability-baseline
description: Set minimum observability with structured logs, correlation IDs, and baseline metrics for latency/errors/throughput. Use when adding services or stabilizing operations.
---

# Observability Baseline

## Goal
Enable debugging without ad-hoc prints.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Logging fields standard, level usage, and metric shortlist.

## Verify Gate
Trace one request path and confirm correlation ID continuity.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
