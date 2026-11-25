---
name: delivery-orchestration
description: Use when one deterministic intake must coordinate the full project-management and delivery lifecycle across intake, shaping, backlog, execution control, forecasting, release, change control, and outcome learning.
---

# Delivery Orchestration

## Specialization

Orchestrate the full PM and delivery lifecycle from one intake.

This skill is the umbrella entry point for agent-usable project management and delivery work. It owns lifecycle phasing, output ownership, handoff conditions, and completion logic across intake, planning, execution control, release, and post-ship learning.

## Objective

Produce one deterministic delivery orchestration contract that coordinates the entire lifecycle with explicit phases, required artifacts, cadence checkpoints, and decision gates.

## Trigger Conditions

- A project needs one top-level PM and delivery intake instead of separate disconnected workflows.
- Work spans request intake, planning, forecasting, scope control, release, and post-ship review.
- Agents need a single lifecycle contract before coordinating delivery across multiple artifacts and decisions.
- A reusable cross-project operating pattern is needed for full delivery governance.

## Scope Boundaries

In scope:

- Lifecycle intake and phase selection.
- Phase-output ownership.
- Handoff conditions and gating rules.
- Planning, execution-control, release, and learning checkpoints.
- Exception and recalculation triggers.

Out of scope:

- Product code implementation.
- Tool-specific administration.
- Team-org redesign beyond owner clarity.
- Specialist engineering execution details.

## Inputs

- Initiative objective, workstream ID, or delivery scope.
- Delivery horizon, release expectations, and review cadence.
- Known owners or owner roles.
- Constraints, dependencies, governance obligations, and risk signals.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Orchestration intake contract with objective, boundaries, success signals, and lifecycle scope.
- Phase-output ownership matrix with exactly one owner per required output.
- Delivery artifact map covering intake, planning, execution control, release, and learning.
- Cadence model for intake review, planning review, flow review, forecast review, release review, and outcome review.
- Exception and recalculation policy for blocked work, scope pressure, forecast drift, and release risk.
- Final orchestration recommendation with adoption order and residual risks.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Stand up one lifecycle contract | Core phases and required outputs are explicit |
| L2 Delivery | Coordinate one project end to end | The lifecycle contract supports live delivery decisions |
| L3 Hardening | Enforce release-grade orchestration | Exceptions, recalculation triggers, and review checkpoints are explicit |
| L4 Expert Standardization | Build a reusable umbrella delivery model | The orchestration contract is portable, auditable, and agent-usable across projects |

## Lifecycle Phases

- Intake Control
- Outcome and Opportunity Framing
- Scope and Backlog Structuring
- Acceptance and Readiness Hardening
- Flow and Forecast Control
- Delivery Coordination
- Scope Change Governance
- Release Control
- Outcome Review and Retrospective Learning

## Deterministic Workflow

1. Lock intake scope: objective, horizon, owners, governance obligations, and out-of-scope boundaries.
2. Select only the lifecycle phases that own necessary outputs for the work.
3. Build the phase-output ownership matrix so every required output has exactly one owning phase.
4. Publish the delivery artifact map before active work begins.
5. Define handoff conditions so downstream phases start only when upstream outputs are complete enough.
6. Set cadence checkpoints for intake review, planning review, flow review, forecast review, release review, and outcome review.
7. Define exception and recalculation rules for blocked work, scope change, weak forecast confidence, and release risk.
8. Run the lifecycle against the published contract and record deviations as explicit exceptions.
9. Close the loop with post-ship outcome review and retrospective adjustments.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Phase | Minimum Artifact |
|---|---|---|
| Admitted, deferred, rejected, or routed inbound work | Intake Control | Intake decision record |
| Target outcome and opportunity structure | Outcome and Opportunity Framing | Outcome framing record |
| Active backlog and release scope model | Scope and Backlog Structuring | Backlog schema and release scope map |
| Testable completion and readiness rules | Acceptance and Readiness Hardening | Acceptance pack and ready checklist |
| Workflow policy, metrics, and forecast view | Flow and Forecast Control | Workflow definition and forecast statement |
| Cross-owner coordination and delivery health | Delivery Coordination | Dependency map, RAID log, milestone view |
| Approved, rejected, deferred, or swapped scope changes | Scope Change Governance | Scope-change record |
| Promotion evidence and go or no-go decision | Release Control | Gate checklist and evidence bundle |
| Expected-versus-actual post-ship decision and learning actions | Outcome Review and Retrospective Learning | Outcome review and learning action list |

## Handoff Criteria

- Do not start backlog structuring until intake and outcome framing are explicit enough to justify active work.
- Do not call work ready for execution until completion and readiness rules are explicit.
- Do not use forecasts for commitment unless flow definitions and assumptions are current.
- Do not absorb scope change silently; every material change must pass the scope-governance phase.
- Do not promote a release when release evidence is incomplete.
- Do not close the lifecycle until post-ship outcome and learning actions are recorded.

## Decision Rules

- If a required output has no owner, orchestration is incomplete.
- If two phases claim the same output, simplify ownership before proceeding.
- If a phase adds no unique output, remove it from scope.
- If exceptions recur without altering the lifecycle contract, treat that as orchestration failure, not normal variance.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| One umbrella PM and delivery intake | Specialization + Deterministic Workflow |
| Explicit lifecycle phase ownership | Lifecycle Phases + Ownership Matrix Template |
| Gated handoffs across lifecycle | Handoff Criteria |
| Forecast, change, release, and learning control | Required Outputs + Decision Rules |
| Cross-project portability | Depth Modes L4 + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- A single lifecycle contract reduces coordination ambiguity better than disconnected local rituals.
- Artifact ownership is the primary control mechanism for agent-usable delivery.

Trade-offs:

- One umbrella model improves consistency but can feel heavier than local team habits.
- Strong gates and recalculation rules reduce drift but surface weak upstream work earlier.

Open blockers:

- Missing named owners weaken phase accountability.
- Existing local process conventions may conflict with explicit lifecycle gating.

Recommendation:

- Use this skill as the top-level delivery orchestration intake when the work spans more than one major delivery control area.

## Workspace Execution Contract

This workspace has a ratified delivery pattern that serves as the canonical phase sequence when this skill is invoked here. Agents must follow it in preference to deriving their own sequence.

**Ratified plan:** [`.docs/plans/delivery/pattern/delivery-pattern-plan.md`](../../../.docs/plans/delivery/pattern/delivery-pattern-plan.md)  
**Status:** APPROVED 2026-05-06  
**Phases:** P1 Intake → P2 Research → P3 Plan (`G-PLAN`) → P4 Acceptance Criteria ‖ P5 ADRs → P6 TDD (`G-TDD`) → P7 Implementation → P7a Security ‖ P7b Performance ‖ P7c Governance Audit → P8 Quality Gate (`G-REVIEW`) → P9 Test Orchestration → P10 Release Readiness (`G-RELEASE`) → P11 Sync/Promotion → P12 Retrospective

Key constraints from the ratified plan:
- Full pattern applies to all deliveries — no abridged variant
- `release-simulation` is mandatory when >3 asset files are changed
- Full PRD for new assets; one-page plan for updates
- Retrospective due within 5 business days or on-demand
- `G-TDD` may be satisfied by `code-reviewer` agent; human oversight required for high-risk or cross-cutting changes

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Default freshness threshold is 30 days.

## Pragmatic Stop Rule

Stop when every selected phase owns one output set, cadence and exception rules are explicit, and lifecycle closure includes both release control and post-ship learning.

## Anti-Patterns

- Running delivery through meetings with no durable lifecycle artifacts.
- Treating forecast, release, and outcome review as optional side activities.
- Allowing scope changes without explicit ownership and impact analysis.
- Ending the lifecycle at deployment instead of at learning closure.

## Done Criteria

- Intake contract, ownership matrix, artifact map, cadence, and exception policy all exist.
- Selected phases have no unowned or multiply owned outputs.
- Handoff criteria and recalculation triggers are explicit.
- Final recommendation states adoption order and residual risk.
- Source catalog entries are current for this evaluation cycle.