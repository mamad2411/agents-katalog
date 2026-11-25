---
name: operations-process-improvement
description: Use when analyzing, documenting, improving, or standardizing an operational process, SOP, workflow, handoff, bottleneck, quality issue, incident pattern, service process, or back-office routine. Prefer this Skill when the task needs process mapping, root-cause thinking, waste reduction, controls, owner clarity, SOP updates, or measurement. Do not use for system changes, compliance approval, or unverified automation claims.
meta:
  version: 1
  display_name: 运营流程优化
---

# Operations Process Improvement

## Purpose

Improve repeatable work by mapping the current process, identifying bottlenecks and failure modes, and designing a simpler, measurable target process.

## Use When

Use for:

- SOP creation or cleanup
- process mapping
- bottleneck analysis
- handoff improvement
- quality issue review
- operational risk reduction
- service process redesign
- back-office routine improvement

## Material Gate

Identify:

- process trigger, owner, participants, inputs, outputs, tools, and frequency
- current steps, pain points, defects, cycle time, and rework
- constraints, controls, and customer/internal impact
- desired level: quick fix, SOP, automation candidate, or redesign

If current process evidence is missing, create a discovery checklist first.

## Workflow

1. Map current state from trigger to done.
2. Identify bottlenecks, rework, unclear owners, missing controls, and avoidable handoffs.
3. Separate root causes from symptoms.
4. Design target state with fewer steps, clearer owners, and measurable checks.
5. Define SOP updates, training needs, and control points.
6. Suggest automation only after process clarity.
7. Use `html-report-builder` for process maps, SOP packs, or improvement reports.

## Checks

- Current and target process are not mixed.
- Each step has owner, input, output, and decision point when relevant.
- Improvement includes metric and review cadence.
- Automation does not mask unclear process ownership.
- Controls are maintained or improved.

## Outputs

- process map
- SOP draft
- root-cause summary
- improvement plan
- handoff checklist
- control matrix
- operations report

## Boundary

This Skill owns operational process analysis, SOP structure, improvement reasoning, and measurement framing. It does not own system configuration, staffing authority, compliance approval, automation implementation, or external system writes.

It must not run shell, Python, Node, npm, curl, MCP, workflow engine, RPA, ticketing, ERP, CRM, email, package install, deploy, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
