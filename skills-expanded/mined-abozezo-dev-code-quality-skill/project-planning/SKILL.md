---
name: project-planning
description: |
  Turns a requested change into an implementation-ready plan by clarifying requirements,
  documenting assumptions, assessing risks and dependencies, sequencing milestones, and
  defining verifiable acceptance criteria. Use before implementation when scope, behavior,
  constraints, or delivery steps need to be agreed.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Project Planning Skill

Create a shared, implementation-ready plan before changing application code. This skill is
planning-only: gather evidence, clarify the requested outcome, and obtain agreement (or enough
specificity to proceed) before handing work to an implementation workflow.

## When to Use This Skill

- A request has unclear scope, users, behavior, success measures, or constraints.
- A feature, migration, integration, refactor, or rollout needs coordinated execution.
- A team needs an ordered plan that another agent can implement without rediscovering decisions.
- Risks, dependencies, trade-offs, or acceptance criteria need explicit treatment.

## Planning Boundary

- **Do not modify application code, configuration, infrastructure, tests, or production data.**
- Do not start implementation, run destructive migrations, or make speculative fixes while planning.
- Read-only repository inspection and non-mutating discovery commands are allowed when they reduce
  uncertainty.
- Planning artifacts may be drafted only when requested or when the surrounding workflow permits
  them; they must describe proposed work, not implement it.
- If requirements remain material and unresolved, ask targeted questions and clearly mark the plan
  as pending agreement rather than guessing.

## Workflow

### 1. Establish the Planning Context

1. Restate the requested outcome in one or two sentences.
2. Inspect relevant existing documentation, architecture, interfaces, and conventions using
   read-only methods.
3. Record the current state, the desired state, affected users or systems, and explicit
   out-of-scope items.
4. Separate known facts from assumptions and open questions.

### 2. Ask Targeted Questions

Ask only questions whose answers change scope, design, sequencing, cost, risk, or acceptance.
Prefer a short, prioritized set over a broad questionnaire. Cover gaps such as:

- **Outcome:** What user or business problem must be solved, and how will success be measured?
- **Behavior:** What are the primary flows, edge cases, failure behavior, and non-goals?
- **Constraints:** What compatibility, performance, accessibility, security, privacy, budget, or
  deadline constraints apply?
- **Ownership:** Who approves decisions, supplies content or credentials, and operates the result?
- **Delivery:** Is there a required rollout, migration, feature flag, monitoring, or rollback plan?

For each question, state why it matters. If an answer is unavailable, propose a bounded default
assumption and label it for confirmation.

### 3. Record Assumptions and Decisions

Maintain an assumptions and decisions log with:

| Item | Type | Rationale | Owner / source | Status |
| --- | --- | --- | --- | --- |
| Example: existing authentication is reused | Assumption | avoids a new identity flow | requester | needs confirmation |

Mark every item as **confirmed**, **proposed**, or **open**. Never present a proposed assumption
as an agreed requirement. Identify which open items block planning or implementation.

### 4. Identify Dependencies and Risks

List dependencies that affect sequencing or delivery, including external services, APIs, data,
teams, approvals, environments, licenses, and release windows. For each material risk, capture:

| Risk | Likelihood | Impact | Early signal | Mitigation | Contingency | Owner |
| --- | --- | --- | --- | --- | --- | --- |

Prioritize risks that could invalidate the approach, delay a milestone, compromise safety, or
require a decision before implementation. Convert unresolved high-impact risks into explicit
decision gates.

### 5. Break Work into Ordered Milestones

Create small, outcome-oriented milestones in dependency order. Each milestone must state:

1. **Goal and scope** — the observable outcome and included/excluded work.
2. **Prerequisites** — decisions, inputs, or prior milestones required to begin.
3. **Implementation approach** — the proposed components, interfaces, data changes, and validation
   strategy at a level sufficient for an implementer to act.
4. **Deliverables and owner** — concrete outputs and responsible party.
5. **Acceptance criteria** — objective conditions proving the milestone is complete.
6. **Risks and rollback considerations** — relevant mitigations, release safeguards, and recovery
   needs.

Sequence discovery and decision gates before dependent build work. Call out parallelizable work
only when dependencies genuinely permit it.

### 6. Produce the Implementation-Ready Plan

Deliver a plan with the following structure:

```markdown
# <Initiative> Plan

## Objective
## Scope and Non-Goals
## Current-State Findings
## Requirements
## Open Questions and Assumptions
## Dependencies
## Risks and Mitigations
## Milestones
### Milestone 1 — <name>
- Goal and scope:
- Prerequisites:
- Proposed approach:
- Deliverables and owner:
- Acceptance criteria:
- Risks / rollback:

## Validation and Release Approach
## Decision Gates and Approval Needed
```

Make acceptance criteria observable and testable. Prefer statements such as “an authorized user
can complete X and receives Y,” “the migration can be rolled back without data loss,” or “the
defined latency target is met under the agreed workload,” rather than “works correctly.”

### 7. Confirm Readiness Before Handoff

Before implementation, verify that:

- Requirements and non-goals are sufficiently specific.
- Material assumptions are confirmed or explicitly approved as defaults.
- Dependencies have owners and a feasible order.
- High-impact risks have mitigations or decision gates.
- Every milestone has measurable acceptance criteria.
- The requester has agreed to the plan, or the documented evidence establishes that the plan is
  sufficiently specified for implementation under the applicable workflow.

If any condition fails, keep the work in planning, state the blocker, and ask the next targeted
question. Hand off only the agreed or sufficiently specified plan; implementation belongs to a
separate workflow.
