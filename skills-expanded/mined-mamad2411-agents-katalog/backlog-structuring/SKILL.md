---
name: backlog-structuring
description: Use when converting goals or validated opportunities into an explicit backlog hierarchy, ordering model, and item schema that agents can plan, execute, and report against.
---

# Backlog Structuring

## Specialization

Transform validated work into an explicit backlog operating model with clear hierarchy, ordering rules, and item fields.

This skill is for backlog architecture, not backlog tool administration. It produces the structure an agent or team needs to manage work consistently across projects.

## Objective

Produce a backlog system that preserves user value, implementation boundaries, and reporting clarity from goal level down to execution-ready items.

## Trigger Conditions

- A project has work items, but hierarchy and scope boundaries are inconsistent.
- Teams are mixing initiatives, features, stories, and tasks without stable rules.
- Backlog grooming is consuming time because the item schema is vague.
- An agent needs a portable backlog model before planning or execution can be reliable.

## Scope Boundaries

In scope:

- Goal and backlog hierarchy design.
- Item schema and status model.
- Ordering and deferral rules.
- Definition of Ready inputs.
- Release grouping fields.

Out of scope:

- Kanban flow policy and metrics tuning.
- Acceptance test writing.
- Release approval governance.
- Vendor-specific board configuration.

## Inputs

- Outcome framing or validated opportunities.
- Known initiative boundaries and release horizons.
- Existing backlog items or seed list.
- Capacity or sequencing constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Goal stack naming the portfolio or product goal and the work hierarchy beneath it.
- Backlog schema for each item level with required fields.
- Ordering policy defining priority, dependency, and deferral behavior.
- Ready-state checklist for execution-ready items.
- Deferral register for items held out of the active backlog.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Clarify hierarchy and item naming | One stable hierarchy and item template exist |
| L2 Delivery | Enable backlog shaping for active work | Active items have required fields and ordering logic |
| L3 Hardening | Standardize team-ready backlog behavior | Ready-state and deferral rules are enforced consistently |
| L4 Expert Standardization | Establish reusable cross-project backlog architecture | Hierarchy, item schema, and ordering policy are portable and auditable |

## Deterministic Workflow

1. Define the top-level goal and the delivery horizon the backlog must serve.
2. Select the hierarchy levels needed for the project. Only keep levels that drive real decisions.
3. Write the required field schema for each level. Distinguish why a user-facing item exists from how it will be implemented.
4. Normalize existing items into that schema. Merge duplicates, split overloaded items, and reject unlabeled work.
5. Set ordering rules using value, urgency, dependency, and risk reduction.
6. Define the Ready checklist for the lowest planning level that can enter execution.
7. Create deferral rules so rejected, parked, or later work is not silently mixed into active scope.
8. Publish the backlog contract with examples for each item level.

## Hierarchy Rules

- Every level must answer a distinct question.
- If two adjacent levels use the same decision criteria, collapse one of them.
- User-facing items must preserve user or business value, not only technical implementation intent.
- Execution tasks must inherit from one parent planning item; orphan tasks are invalid.

## Artifact Contract

| Artifact | Minimum Fields |
|---|---|
| Goal stack | Goal ID, description, time horizon, success signal |
| Backlog item schema | Item level, ID pattern, title format, purpose, required fields |
| Ordering policy | Priority signals, dependency rules, tie-break logic, escalation rule |
| Ready checklist | Required context, acceptance input, owner, dependency status |
| Deferral register | Item ID, reason, review trigger, owner |

## Decision Rules

- If an item cannot state its parent outcome or parent work item, do not keep it in the active backlog.
- If an item mixes multiple independently shippable outcomes, split it.
- If a task contains user-value language, it probably belongs one level higher.
- If a deferral reason is missing, the item is not deferred; it is unmanaged.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Clear hierarchy | Deterministic Workflow steps 1 to 3 |
| Reusable item schema | Required Outputs + Artifact Contract |
| Ordering and deferral discipline | Deterministic Workflow steps 5 to 7 |
| Agent-usable ready state | Ready-state checklist + Decision Rules |
| Cross-project portability | Depth Modes L4 + Hierarchy Rules |

## Reasoning Package

Assumptions:

- The project benefits from explicit hierarchy rather than a flat list.
- The lowest planning level is not the same as the execution-task level.

Trade-offs:

- More hierarchy improves traceability but increases maintenance cost.
- Strict schema rules reduce ambiguity but require disciplined backlog curation.

Open blockers:

- Legacy backlogs may contain unlabeled items that need manual normalization.
- Tool limits can pressure teams into bad hierarchy compromises.

Recommendation:

- Use this skill whenever delivery work spans more than one release candidate or more than one planning level. It provides the durable structure agents need for planning, execution, and reporting.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Default freshness threshold is 30 days.

## Pragmatic Stop Rule

Stop when every active item fits one level, required fields are explicit, and the execution-ready level has an enforceable Ready checklist.

## Anti-Patterns

- Treating the backlog as a dumping ground.
- Using hierarchy labels without distinct decision meaning.
- Letting technical tasks float without a parent user or business outcome.
- Leaving deferred work in the active queue.

## Done Criteria

- Goal stack and backlog schema are complete.
- Ready-state and deferral rules are explicit.
- Active items can be normalized into one consistent hierarchy.
- Source catalog entries are current for this evaluation cycle.