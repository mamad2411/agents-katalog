---
name: pericles-execution-node
version: 2026.05.0
description: >
  How to build deterministic Execution Nodes that commit consequential actions — the
  §3 "supervisors propose, executors commit" boundary. Use this WHENEVER an LLM-driven
  Skill would otherwise send a notification, commit freight, contact a supplier,
  message a customer, or write an audit record. Encodes the deterministic-commit rule,
  per-commit logging, trial vs run mode, and how this maps onto the existing Workflow
  node-handler engine (BaseNodeHandler + TRIGGER/ACTION/CONDITION/NOTIFICATION/END).
doctrine_refs: [§3]
depends_on: [pericles-doctrine, pericles-functional-agent, pericles-postgres-queue]
last_reconciled: 2026-05-28
---

# Pericles Execution Node (build skill)

Consequential actions must be **deterministic and auditable**, never a raw LLM call
(§3). A supervisor (Functional Agent) reasons and **proposes**; a deterministic
**Execution Node** validates the proposal against rules and **commits**. The repo
already has the substrate: the Workflow node-handler engine.

## When to use this skill

Any time a Skill's output would cause a real-world effect: sending a
notification/alert, committing freight or a re-route, contacting a supplier, messaging
a customer, or writing an audit/history record. Also when building Plan execution.

## The existing substrate: Workflow node handlers

`backend/src/workflow/handlers/` is the deterministic execution layer (the Plans
engine). Build Execution Nodes as node handlers:

- **`BaseNodeHandler`** (abstract): `supportedTypes: NodeType[]`, `canHandle(nodeType)`,
  `execute(node, context): NodeExecutionResult`, and logging helpers
  (`createLogEntry` / `startExecution` / `completeExecution`).
- **`NodeType`** ∈ `TRIGGER | ACTION | CONDITION | NOTIFICATION | END`; concrete
  handlers: `trigger-handler`, `action-handler`, `condition-handler`,
  `notification-handler`, `end-handler`.
- **Trial vs run mode** — handlers check `isTrialMode(context)`. In trial mode the
  `NotificationHandler` *simulates* ("would send"); in run mode it actually sends. This
  is the dry-run safety the doctrine wants; honor it in every new handler.
- **`ExecutionMode`** ∈ `MANUAL | AUTOMATIC | BOTH`; **`ExecutionStatus`** ∈
  `PENDING | RUNNING | COMPLETED | FAILED | CANCELLED` (on `WorkflowExecution`).

A consequential action = a node handler whose `execute` performs the commit
deterministically and writes an `ExecutionLog`.

## The commit rule (§3)

1. The supervisor (agent) produces a **proposal** as schema-validated structured data
   (`pericles-prompts`) — what to do, to whom, why.
2. The Execution Node **re-validates** the proposal against deterministic rules (tenant
   scope, thresholds, allow-lists), independent of the LLM.
3. It **commits** — and only the Execution Node commits.
4. It **logs** the commit: the proposing Skill ID + version, the inputs, and the rule
   path taken (the §3 per-commit record; maps to `ExecutionLog` + the per-invocation
   lineage in `pericles-observability`).

External-facing commits (customer/supplier messages) additionally require the human/
approval gate per deployment shape (`pericles-deployment-shapes`); Execution Nodes
never auto-send external comms without it (`pericles-notifications`).

## Dispatch via the queue

The queue **dispatches**; the Execution Node **commits**. A proposal becomes a
`MessageQueue` message (`message_type: notification | incident | event`), a worker
hands it to the handler, the handler commits with retries/backoff
(`pericles-postgres-queue`). Publishing never blocks the proposing path.

## What this forbids

Committing a consequential action from an agent/prompt or a tool's `execute()`; an
Execution Node that trusts the proposal without independent rule validation; sending
external comms without the approval gate; a handler that ignores trial mode; a commit
without an `ExecutionLog` recording proposing Skill version + inputs + rule path.

## Verification

Every consequential action is a node handler extending `BaseNodeHandler`; trial mode
simulates and run mode commits; each commit writes an `ExecutionLog` with proposing
Skill version + inputs + rule path; external comms gated by approval; rule validation
is independent of the LLM proposal. Add a test that a malformed/forged proposal is
rejected deterministically.

## Existing standards (read alongside)

Doctrine §3 (Notion); `backend/src/workflow/handlers/*` and `backend/src/workflow/types.ts`;
`.claude/plans/drag-drop-workflow-architecture.md`; `.cursor/rules/001-application/006-pericles-plans-core-standards-auto.mdc`.

## Open questions

- Whether non-Plan consequential actions (e.g. Co-Pilot-proposed supplier outreach)
  reuse the Workflow handler engine or a lighter Execution Node abstraction — decide
  before the first non-Plan committer ships.
- The exact approval-gate mechanism per deployment shape — define with
  `pericles-deployment-shapes`.

## Changelog

- 2026.05.0 — Initial draft. §3 commit rule mapped onto the real Workflow node-handler
  engine (BaseNodeHandler, NodeType, trial/run mode, ExecutionLog) and the MessageQueue
  dispatch path.
