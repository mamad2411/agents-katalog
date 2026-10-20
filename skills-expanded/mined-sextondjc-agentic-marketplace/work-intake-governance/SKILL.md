---
name: work-intake-governance
description: Use when raw requests, ideas, incidents, or stakeholder asks must be classified, bounded, and admitted, deferred, rejected, or routed before they enter planning or delivery.
---

# Work Intake Governance

## Specialization

Classify inbound work before it pollutes the backlog.

This skill turns raw demand into an explicit intake decision with evidence requirements, ownership, urgency, and routing. It is the pre-backlog control point for agent-usable delivery systems.

## Objective

Produce a governed intake record that decides whether a request should be accepted, deferred, rejected, or routed elsewhere, with enough structure for downstream planning to proceed without re-triaging the same input.

## Trigger Conditions

- New requests arrive from stakeholders, support, leadership, or discovery work.
- A backlog is accumulating poorly formed items with unclear ownership or urgency.
- A project needs a consistent gate before requests become active planning candidates.
- Agents need a deterministic intake rule set before deciding what enters planning or delivery.

## Scope Boundaries

In scope:

- Intake classification.
- Urgency and impact scoring.
- Evidence sufficiency checks.
- Admission, deferral, rejection, and routing decisions.
- Intake ownership and follow-up trigger definition.

Out of scope:

- Detailed backlog decomposition.
- Experiment execution.
- Implementation planning.
- Root-cause investigation beyond intake requirements.

## Inputs

- Raw request or request set.
- Source channel and requester context.
- Known business, operational, or user impact.
- Available evidence and supporting artifacts.
- Constraints: timelines, compliance, capacity, and dependencies.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Intake record with request ID, source, summary, owner, and classification.
- Admission decision: accept, defer, reject, or route.
- Evidence sufficiency note listing what exists and what is missing.
- Urgency and impact assessment with rationale.
- Next-action trigger with named owner and decision horizon.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Classify one inbound request | One intake record and one decision exist |
| L2 Delivery | Govern a batch of requests | All items have explicit intake disposition |
| L3 Hardening | Establish admission discipline | Evidence and urgency rules are enforced consistently |
| L4 Expert Standardization | Build reusable intake operating model | Intake schema and admission rules are portable across projects |

## Deterministic Workflow

1. Normalize the request into one concise problem or ask statement.
2. Record source, requester, and any time or governance constraint.
3. Check evidence sufficiency: problem proof, impact proof, and urgency proof.
4. Score urgency and impact using explicit decision rules.
5. Choose disposition: accept, defer, reject, or route.
6. Record the reason for the decision and the conditions that would change it.
7. Assign an owner and next trigger so the intake does not go stale.
8. Publish the intake record in a durable format suitable for backlog or planning handoff.

## Intake Decision Rules

- Accept when the request has enough evidence, a real owner, and a credible path to action.
- Defer when the request matters but lacks timing, evidence, or capacity fit.
- Reject when the request conflicts with strategy, duplicates an existing item, or lacks durable value.
- Route when the request belongs to a different delivery stream, owner, or specialist process.

## Artifact Contract

| Artifact | Minimum Fields |
|---|---|
| Intake record | Request ID, summary, source, owner, disposition, rationale |
| Evidence note | Existing evidence, missing evidence, confidence level |
| Urgency-impact assessment | Urgency, impact, risk note, rationale |
| Next-action trigger | Trigger date or event, owner, review condition |

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Pre-backlog admission gate | Objective + Deterministic Workflow |
| Explicit intake decisions | Required Outputs + Intake Decision Rules |
| Evidence-based intake quality | Deterministic Workflow step 3 + Artifact Contract |
| Durable routing and follow-up | Required Outputs + Deterministic Workflow steps 6 to 8 |
| Portable cross-project intake model | Depth Modes L4 + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Not every inbound ask deserves backlog space.
- Intake quality improves downstream planning more than ad hoc clarification later.

Trade-offs:

- Strong intake control reduces churn but can feel slower to requesters.
- High evidence expectations improve signal quality but may defer some valuable work.

Open blockers:

- Weak ownership prevents durable intake decisions.
- Missing evidence can force defer decisions even when intuition says the work matters.

Recommendation:

- Use this skill wherever multiple sources can create work. It is the cleanest way to stop backlog pollution before it starts.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Default freshness threshold is 30 days.

## Pragmatic Stop Rule

Stop when each inbound item has one explicit disposition, one owner, and one next trigger, and no item remains in an ambiguous intake state.

## Anti-Patterns

- Treating every inbound request as a backlog item.
- Accepting requests with no owner.
- Hiding missing evidence inside vague urgency language.
- Letting deferred requests decay without a review trigger.

## Done Criteria

- All required outputs exist.
- Each item has exactly one disposition.
- Evidence sufficiency is explicit.
- Ownership and next trigger are recorded.
- Source catalog entries are current for this evaluation cycle.