---
name: itsol-subagent-workflow
description: "Delegate authorized work with bounded packets, ownership, verification, and review when required."
---
# ITSOL Subagent Workflow

Validate `itsol-workflow-mode` before delegation. Every packet includes `workflow_mode`, `mode_source`, `decision_authority`, `scope`, `artifact_state`, `execution_mode`, and `protected_constraints`; invalid or restriction-conflicting state is `blocked`.

Validate `itsol-execution-policy` too: propagate execution state, observable `done_when`, child `stop_after` no later than the parent, remaining identity/parallel/review ceilings, and escalation behavior. Missing or expanded state is `blocked`.

Accept `approved` only for genuinely approved `governed` artifacts, `ready-for-execution` for reviewed `autonomous-planned`, and `not-required` for `direct`; `Draft` never authorizes execution. Direct needs no plan path.

## Packet and graph

State outcome, authority/constraints, `done_when`, focused evidence, bounded read/write scope, dependencies, ownership, and stable `work_item_id`. Build a graph only when multiple packets/dependencies need one; otherwise stay inline or use one packet. Identity reuse counts once against `max_subagents`; each running packet counts against `max_parallel`. Keep one writer per file/contract, require proportionate verification evidence, and use independent review only when policy, user request, or material risk warrants it. TDD/RED-GREEN evidence is required only for an explicitly requested test-first task.

Initiative phase packets additionally carry `initiative_id`, `phase_id`, requirement IDs, canonical artifact paths, decisions, and phase evidence obligations. Child completion does not update initiative/phase state until the main agent validates and records it.

## Boundary and response

Only the main agent delegates. Children do not spawn agents or invoke external agent CLIs. Never set `maxTurns`. Each response reports `completed`, `partial`, `blocked`, or `failed`, achieved evidence, unverified gaps, blockers, and next action; the main agent accepts `completed` only after validating every `done_when`. Commit only when separately authorized, using Angular convention and one coherent verified slice.

Load `itsol-execution-policy` after workflow mode and preserve both contracts through plans, context, compaction, packets, continuations, review, and handoff. Resource policy never changes workflow authority.

## Focused references

- [01-planning-and-delegation.md](./references/01-planning-and-delegation.md) — packet planning and delegation.
- [02-review-commit-validation.md](./references/02-review-commit-validation.md) — review, commit, and validation.
