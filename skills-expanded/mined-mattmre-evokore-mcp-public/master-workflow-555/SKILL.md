---
name: master-workflow-555
description: Use when orchestrating a non-trivial coding task end-to-end and you want disciplined phase/panel/gate structure without giving up autonomous-loop continuity. Drives the 5/5/5 master workflow (5 phases, 5 panels, 5 gates).
aliases:
  - master-555
  - 5-5-5
  - master-workflow
category: EVOKORE Extensions
tags:
  - orchestration
  - workflow
  - master
  - phases
  - panels
  - gates
metadata:
  version: "1.0.0"
  source: "EVOKORE"
---

# Master Workflow 5/5/5

The **5/5/5 master workflow** is the highest-level coding-task template in EVOKORE. It walks one task through **5 phases**, with **5 panel reviews** invoked at the critical decision points, and **5 quality gates** that must pass before the next phase starts.

## When to use it

Reach for this workflow when:

- The task is non-trivial (would benefit from explicit planning + verification rather than ad-hoc edits).
- You want panel-of-experts review at the critical decision points.
- You need a single, auditable trail of phases → panels → gates → deliver.
- You want a structured DAG without losing autonomous-loop continuity (no new blocking surfaces — gates are conditional, not interactive).

Do **not** use it for trivial single-edit tasks; the overhead is wasted there.

## The 5/5/5 structure

| # | Phase | Panel | Gate |
|---|-------|-------|------|
| 1 | **Plan**       — produce an implementation plan      | Architecture Planning   | Plan approved        |
| 2 | **Explore**    — survey the relevant codebase         | Feasibility Research    | Exploration complete |
| 3 | **Implement**  — apply the plan                       | Code Refinement         | Implementation complete |
| 4 | **Verify**     — run tests, fill coverage gaps        | Testing Quality         | Tests green          |
| 5 | **Handoff**    — emit PR body + session-log update    | Documentation Quality   | Handoff ready        |

Each gate is a `conditional` step that evaluates a simple expression on the outputs of its phase (and, where applicable, its panel). A gate that does not pass short-circuits the rest of the DAG — but the workflow still runs `deliver` so the operator gets a partial report instead of a black box.

## Inputs

| Input | Type | Required | Default | Notes |
|---|---|---|---|---|
| `task_title`        | string  | yes |   | Short imperative title |
| `task_brief`        | string  | yes |   | Self-contained task brief |
| `artifacts`         | array   | no  | `[]` | Initial known files / URLs |
| `skip_panels`       | array   | no  | `[]` | Panel IDs to skip (e.g. `["architecture"]`) |
| `max_phase_seconds` | number  | no  | `1800` | Per-phase timeout |

## Outputs

A single `task_report` object with three keys:

- `phases` — output of each of the 5 phases.
- `panels` — output of each of the 5 panel reviews.
- `gates` — boolean approval state for each of the 5 gates.

## Skipping panels

Pass `skip_panels` to bypass any subset of the 5 panels for fast-track tasks. Valid panel IDs:

- `architecture`
- `feasibility`
- `code-refinement`
- `testing-quality`
- `documentation-quality`

Skipping a panel does **not** skip the corresponding gate — gates evaluate phase outputs, so they remain in force.

## Relationship to other skills / workflows

- `panel-review-generic` — invoked under the hood for each of the 5 panels.
- `release-readiness-gate` — narrower workflow for release decisions only. The 5/5/5 master workflow can call it as part of the Verify phase.
- `orch-plan`, `orch-review`, `orch-refactor` — sub-orchestration skills that map to individual phases.

## Why 5 / 5 / 5?

- **5 phases** is the minimum count that distinguishes planning from exploration and verification from handoff. Fewer phases collapse meaningful boundaries; more become bookkeeping.
- **5 panels** maps cleanly onto the 5 phases — one expert review at each critical decision point.
- **5 gates** keeps the failure surface explicit: every phase has a single, named, boolean checkpoint.

## Invocation example

```json
{
  "workflow": "master-workflow-555",
  "inputs": {
    "task_title": "Add evokore:init repo bootstrap",
    "task_brief": "Add a first-run bootstrap command that reports and (with --apply) materializes runtime state. Must be idempotent and dry-run by default.",
    "artifacts": ["scripts/", "package.json", "tests/integration/"],
    "skip_panels": []
  }
}
```

## Non-goals

- Not a replacement for ad-hoc editing on trivial tasks.
- Not a CI workflow — runs inside an MCP orchestration session, not GitHub Actions.
- Does not commit, push, or open PRs by itself. The Handoff phase only emits the PR body markdown; the operator decides whether to land it.
