---
name: delivery-status-grid
description: Use when a user asks for delivery status, progress, completion state, or remaining scope and expects table-first reporting with explicit X of Y measures.
---

# Delivery Status Grid

## Overview

Provide delivery updates in grid-first format so progress is scannable, comparable, and measurable across projects.

This skill is generic and can be applied to any repository, stack, or delivery model.

## Trigger Conditions

Use this skill when the user asks for:
- Delivery status
- Progress update
- Completion state
- What is done vs what remains
- Any "where are we" checkpoint

Do not use this skill for deep defect analysis or code review findings; use review workflows for those.

## Required Output Contract

Always follow this contract:
- Put tables first.
- Include at least one explicit X of Y metric.
- Prefer separate Done and Remaining tables when scope is multi-part.
- Keep non-table narrative to 3 short lines maximum.
- If denominator Y is not obvious, define Y before reporting X of Y.

## X of Y Rules

Use these rules consistently:
- X = completed units.
- Y = total units in agreed scope.
- If useful, add percent as (X / Y) * 100.
- Never report X without naming Y.
- If scope changed, restate updated Y and note that progress was recalculated.

## Evidence Gathering (Generic)

Base status on verifiable signals, not assumptions:
- Build and test outcomes.
- Delivery docs, plans, and execution logs.
- CI status and quality gates.
- Completed vs pending milestones/tasks.
- Known blockers and dependencies.

If evidence is incomplete, state assumptions in one short line below tables.

## Table Templates

### Summary

Use template: `./references/summary-template.md`

### Done

Use template: `./references/done-template.md`

### Remaining

Use template: `./references/remaining-template.md`

### Risks and Blockers

Use template: `./references/risks-and-blockers-template.md`

## Response Flow

1. Confirm reporting scope.
2. Gather current evidence.
3. Define denominators (Y values).
4. Produce Summary, Done, Remaining tables.
5. Add risks/blockers table if relevant.
6. End with brief caveat lines only when necessary.

## Common Mistakes

Avoid these mistakes:
- Narrative-first responses.
- Missing denominator Y.
- Mixing done and remaining into a single unclear table.
- Reporting stale metrics after scope changes.
- Overloading the response with long prose.

## Done Criteria

A response is complete only if:
- It is grid-first.
- It contains at least one X of Y metric.
- Done and Remaining are clearly separated when applicable.
- Narrative is minimal and only adds context.

## Inputs

- User request context and target scope for this skill invocation.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.

## Workflow

1. Gather required context and constraints from the workspace and user request.
2. Execute the skill-specific steps and produce the required artifacts or decisions.
3. Validate outputs for completeness and consistency with active workspace instructions.

