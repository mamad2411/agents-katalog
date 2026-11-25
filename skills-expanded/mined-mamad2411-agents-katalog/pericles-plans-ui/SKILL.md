---
name: pericles-plans-ui
version: 2026.05.0
description: >
  How to build Plans — the response-workflow module: a Plan Builder (form + drag-drop
  workflow graph), execution, a communications hub, reporting, and simulation. Use this
  WHENEVER you build or change Plan authoring, execution, comms, reporting, or
  simulation. Encodes the existing Workflow engine substrate (Workflow/Node/Edge/
  Execution + handlers + reactflow), trial-mode simulation, and that execution commits
  through deterministic node handlers.
doctrine_refs: [§3; Plans PRD]
depends_on: [pericles-frontend-foundations, pericles-execution-node, pericles-notifications, pericles-persona-layer]
last_reconciled: 2026-05-28
---

# Pericles Plans UI (build skill)

Plans turn a risk event into a coordinated response: build a Plan, execute it, coordinate
communications, report on it, and simulate before committing. **The engine already
exists** — `Workflow`/`WorkflowNode`/`WorkflowEdge`/`WorkflowExecution`, the
`workflow/handlers/`, `frontend/src/components/workflow`, **reactflow**, and
`.claude/plans/drag-drop-workflow-architecture.md`. Build the UX on top of it.

## When to use this skill

Building/changing the Plan Builder, execution, the comms hub, reporting, or simulation.

## Surfaces

- **Plan Builder** — two complementary modes: a **form** for quick authoring and a
  **drag-drop workflow graph** (reactflow over `WorkflowNode`/`WorkflowEdge`). Node types
  map to the engine's `NodeType`: TRIGGER, ACTION, CONDITION, NOTIFICATION, END
  (`pericles-execution-node`).
- **Execution** — runs a `WorkflowExecution` (status PENDING/RUNNING/COMPLETED/FAILED/
  CANCELLED) via the deterministic node handlers. `ExecutionMode` is MANUAL / AUTOMATIC /
  BOTH. Every node writes an `ExecutionLog` (lineage, `pericles-observability`).
- **Communications hub** — NOTIFICATION nodes deliver via the `NotificationHandler`
  (`pericles-notifications`); external comms pass the approval gate, never auto-send.
- **Reporting** — execution history, outcomes, and audit trail per Plan (read-only logs).
- **Simulation** — **trial mode**: run the Plan with handlers simulating side effects
  ("would send", "would commit") so the user can validate before a real run. Honor
  `isTrialMode` end to end.

## Templates & packs

Industry Packs ship `plan_templates` (e.g. Tier-1 Supplier Disruption, Port Strike
Response, Raw Material Shortage) the customer activates — they don't author from scratch
(`pericles-industry-pack`). A template instantiates a `Workflow`.

## Persona & tenant

Persona shapes the Plans surface (`pericles-persona-layer`); Plans and executions are
tenant-scoped (`organization_id` on `Workflow`/`WorkflowExecution`,
`pericles-tenant-isolation`).

## What this forbids

Executing consequential nodes outside the deterministic handlers; auto-sending external
comms without the approval gate; a Builder that bypasses the Workflow models or invents a
parallel engine; ignoring trial mode in simulation; editable execution logs; client-
trusted `organization_id`.

## Verification

The Builder produces valid `Workflow` graphs (typed nodes/edges); execution runs through
handlers with `ExecutionLog`s; simulation honors trial mode; comms route via the
NotificationHandler + approval; templates instantiate from packs; everything tenant-scoped.

## Existing standards (read alongside)

`.claude/plans/drag-drop-workflow-architecture.md`;
`.cursor/rules/001-application/006-pericles-plans-core-standards-auto.mdc`;
`backend/src/workflow/*`, `frontend/src/components/workflow`; Plans PRD.

## Open questions

- The form↔graph round-trip (does the form generate graph nodes, or are they separate
  authoring paths) — confirm with the drag-drop architecture plan.
- Where Plan templates are stored/versioned (registry vs pack) — reconcile with
  `pericles-industry-pack`.

## Changelog

- 2026.05.0 — Initial draft; built on the existing Workflow engine (models + handlers +
  reactflow) and trial-mode simulation.
