---
name: flow-metrics
description: Use when defining workflow states, WIP policy, delivery metrics, and improvement rules so agents and teams can manage flow with explicit signals instead of intuition.
---

# Flow Metrics

## Specialization

Define the delivery-flow operating model: workflow states, WIP limits, service expectations, and measurement rules.

This skill turns work execution into an observable system. It is not for backlog design or release approval; it is for managing flow quality once work is in motion.

## Objective

Produce an explicit workflow and measurement contract that supports daily execution decisions, escalation, and continuous improvement.

## Trigger Conditions

- Work is moving, but bottlenecks and aging items are hard to reason about.
- Teams want Kanban discipline or DORA-style measurement without vague metric theater.
- An agent needs explicit workflow policies before it can report or optimize delivery reliably.
- Throughput, WIP, and lead time are being discussed without stable definitions.

## Scope Boundaries

In scope:

- Workflow state definition.
- Started and finished rules.
- WIP policy.
- Service level expectations.
- Flow and delivery metrics.
- Improvement review cadence.

Out of scope:

- Backlog hierarchy design.
- Acceptance-criteria authoring.
- Release evidence collation.
- Team-structure redesign beyond necessary ownership signals.

## Inputs

- Current workflow or board states.
- Item types and service classes.
- Historical delivery data if available.
- Operational constraints and escalation expectations.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Workflow definition including each state, entry rule, and exit rule.
- WIP and service policy table.
- Metrics contract covering flow metrics and delivery outcome metrics.
- Breach and escalation playbook for aging, blocked, or failing work.
- Improvement review template with metric interpretation guardrails.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Make workflow observable | States and started/finished rules are explicit |
| L2 Delivery | Control active work with policy | WIP and SLE rules are published |
| L3 Hardening | Use metrics for operational decisions | Breach playbook and review cadence are active |
| L4 Expert Standardization | Establish portable flow governance model | Workflow, metrics, and guardrails are reusable across projects |

## Deterministic Workflow

1. Define the workflow states and remove duplicate or ambiguous labels.
2. Set explicit entry and exit rules for each state, including what counts as started and finished.
3. Assign service classes or item types only when they change workflow policy.
4. Set WIP limits and service level expectations that reflect real operating capacity.
5. Define the metrics contract: WIP, throughput, work item age, cycle time, lead time, change failure rate, deployment frequency, and recovery signal where relevant.
6. Add metric guardrails so no single proxy is used as the whole story.
7. Publish the breach playbook for blocked items, aged items, and SLE misses.
8. Run the review cadence with one action-focused improvement decision per cycle.

## Metrics Rules

- Do not track a metric unless it drives a decision.
- Use flow metrics for local execution control and delivery metrics for system improvement; do not confuse them.
- If a metric can be gamed easily, pair it with a balancing signal.
- Do not change state definitions midstream without recording the date of change.

## Artifact Contract

| Artifact | Minimum Fields |
|---|---|
| Workflow definition | State, purpose, entry rule, exit rule, owner |
| Policy table | Item class, WIP limit, SLE, escalation trigger |
| Metrics contract | Metric, definition, purpose, review cadence, balancing signal |
| Breach playbook | Trigger, owner, action, escalation path |
| Improvement review template | Review date, signals observed, change proposed, next checkpoint |

## Decision Rules

- If a state has no distinct entry or exit rule, remove or merge it.
- If a WIP limit is never acted on, it is decoration, not policy.
- If a metric lacks a balancing signal and can distort behavior, downgrade its use.
- If a breach trigger has no owner, it is not an escalation path.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Explicit workflow model | Deterministic Workflow steps 1 to 4 |
| Delivery measurement contract | Deterministic Workflow step 5 + Artifact Contract |
| Anti-metric-theater safeguards | Metrics Rules + Deterministic Workflow step 6 |
| Operational escalation rules | Breach playbook + Decision Rules |
| Reusable cross-project flow system | Depth Modes L4 + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Work can be represented as items moving through a defined workflow.
- Policy is only useful if it changes behavior when breached.

Trade-offs:

- More explicit flow control improves predictability but can expose uncomfortable capacity limits.
- Richer measurement improves learning but increases instrumentation and review overhead.

Open blockers:

- Missing historical data may delay baseline setting.
- Inconsistent state usage can make early metrics noisy.

Recommendation:

- Use this skill as soon as a team wants trustworthy delivery signals. It prevents the common failure mode where agents and humans report motion instead of flow health.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Default freshness threshold is 30 days.

## Pragmatic Stop Rule

Stop when the workflow states are enforceable, metrics definitions are decision-linked, and breach handling has named owners and actions.

## Anti-Patterns

- Collecting dashboards with no decision usage.
- Treating throughput as the only success metric.
- Running WIP limits with no escalation behavior.
- Redefining states after misses to hide flow problems.

## Done Criteria

- Workflow definition, policy table, metrics contract, and breach playbook all exist.
- Each metric has a purpose and review cadence.
- Escalation ownership is explicit.
- Source catalog entries are current for this evaluation cycle.