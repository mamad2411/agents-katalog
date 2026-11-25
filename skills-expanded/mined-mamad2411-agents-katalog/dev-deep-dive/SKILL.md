---
name: dev-deep-dive
description: Two-stage investigation — causal trace (via @trail-tracer) followed by requirements crystallization (via @echo-analyst + dev-deep-interview). Use when a problem is both unclear in cause AND unclear in scope.
---

# Dev Deep Dive

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

A two-stage investigation that combines causal tracing with requirements crystallization. Use when both the cause AND the scope of a problem are ambiguous.

## Use When
- Production issue with unclear cause AND unclear scope of fix
- Bug report that needs both root cause analysis and clarification of "what does fixed look like?"
- Strategic problem where you don't know what to build OR why the current state isn't working

## Workflow

### Stage 1 — Causal trace
Hand off to `@trail-tracer`:
- Generate competing hypotheses
- Collect evidence FOR and AGAINST each
- Apply lenses (systems / premortem / science)
- Identify the discriminating probe
- Save report to `workspace/development/debug/[C]trace-{topic}-{date}.md`

### Stage 2 — Requirements crystallization
Hand off to `@echo-analyst` + `dev-deep-interview`:
- Surface unstated assumptions
- Define scope boundaries
- Identify missing acceptance criteria
- Save spec to `workspace/development/specs/[C]spec-{topic}-{date}.md`

### Stage 3 — Synthesis
- Combine the trace report and the requirements spec
- Output: a unified understanding of "what's broken AND what done looks like"
- Hand off to `@compass-planner` to plan the actual fix

## Pairs With
- `@trail-tracer` (Stage 1)
- `@echo-analyst` (Stage 2)
- `dev-deep-interview` (Stage 2)
- `@compass-planner` (Stage 3 handoff)
