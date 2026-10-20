---
name: delivery-operating-system
description: Use when a project needs one expert-level, agent-usable project management and delivery operating model spanning discovery, shaping, backlog structure, flow control, release control, and learning loops.
---

# Delivery Operating System

## Specialization

Orchestrate a complete project-management and delivery operating model that agents can use across many projects without relying on implicit team habits.

This skill is the multi-capability entry point for agent-usable delivery work. It owns intake, phase sequencing, artifact ownership, and closure rules across the delivery lifecycle.

## Objective

Produce one reusable operating system for delivery: from outcome framing through retrospective improvement, with explicit artifacts, ownership, cadence, and decision gates.

## Trigger Conditions

- A project needs a full delivery operating model, not just one local skill.
- Teams want one expert-level intake that coordinates discovery, planning, flow, release, and learning.
- A compendium needs portable PM and delivery guidance that can be applied across many repositories.
- Agents are expected to participate in planning and delivery without relying on tacit human process knowledge.

## Scope Boundaries

In scope:

- Delivery-lifecycle intake.
- Phase sequencing and artifact ownership.
- Cross-phase handoff criteria.
- Review cadence and escalation model.
- Release and retrospective checkpoints.

Out of scope:

- Tool-specific board setup.
- Application implementation.
- Team-org redesign beyond handoff clarity.
- Domain-specific engineering standards.

## Inputs

- Project objective, workstream ID, or initiative name.
- Time horizon and release expectations.
- Participating owners or owner roles.
- Known constraints, dependencies, and governance obligations.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Intake contract with objective, boundaries, success signals, and lifecycle scope.
- Phase-output ownership matrix with exactly one owning phase per required output.
- Core artifact set for discovery, planning, execution, release, and learning.
- Cadence model for planning, flow review, go/no-go, and retrospective checkpoints.
- Escalation and exception policy for blocked, aging, or high-risk work.
- Final operating-model recommendation with residual risks and adoption order.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Stand up a lightweight delivery system | Core phases and artifact owners are defined |
| L2 Delivery | Enable one project end to end | Artifact set and cadence support active delivery |
| L3 Hardening | Establish release-grade governance | Exception handling and release checkpoints are explicit |
| L4 Expert Standardization | Build a reusable cross-project delivery model | The operating system is portable, auditable, and agent-usable by default |

## Capability Phases

- Outcome Framing
- Opportunity Mapping
- Scope and Release Slicing
- Backlog Structuring
- Acceptance Hardening
- Flow Governance
- Delivery Coordination
- Release Control
- Retrospective Learning

## Deterministic Workflow

1. Lock intake scope: objective, timeline, owners, governance obligations, and out-of-scope boundaries.
2. Select the phases required for the project. Keep only phases that own real outputs.
3. Build the phase-output ownership matrix. Every required artifact must have exactly one owning phase.
4. Publish the artifact contract for the chosen phases before execution begins.
5. Define handoff criteria between phases so downstream work starts only when upstream artifacts are complete enough.
6. Set cadence checkpoints: planning review, flow review, release review, and retrospective review.
7. Add escalation rules for blocked work, aging work, missing evidence, and release risk.
8. Run the lifecycle using the defined artifacts and checkpoints, recording exceptions instead of bypassing them.
9. Close the loop with retrospective learning and operating-model adjustments.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Phase | Minimum Artifact |
|---|---|---|
| Outcome definition and success signal | Outcome Framing | Outcome framing record |
| Opportunity structure and hypothesis tests | Opportunity Mapping | Opportunity map and assumption-test matrix |
| Release candidate decomposition | Scope and Release Slicing | Slice registry and release candidate map |
| Active backlog hierarchy and ready-state contract | Backlog Structuring | Backlog schema and ready checklist |
| Testable completion rules | Acceptance Hardening | Acceptance criteria pack and done gate |
| Active work policy and delivery signals | Flow Governance | Workflow definition and metrics contract |
| RAID and cross-owner coordination | Delivery Coordination | RAID log, dependency map, milestone list |
| Promotion and rollback decision evidence | Release Control | Gate checklist and evidence bundle |
| Learning and follow-up actions | Retrospective Learning | Retrospective summary and improvement actions |

## Handoff Criteria

- Do not start backlog structuring until the selected outcomes or opportunities are explicit enough to trace work upward.
- Do not start execution planning until acceptance hardening is sufficient for done to be checked without guesswork.
- Do not treat work as in flow until workflow state rules and ownership are explicit.
- Do not promote a release when release-control evidence is incomplete.
- Do not call the operating model stable until retrospective actions are recorded.

## Decision Rules

- If a required output has no owner, the operating system is incomplete.
- If multiple phases claim the same required output, ownership must be simplified before execution continues.
- If a phase has no artifact, remove the phase or define the artifact.
- If exceptions recur without changing the model, treat that as a design failure, not a one-off issue.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| One reusable PM/delivery entry point | Specialization + Deterministic Workflow |
| Explicit phase orchestration | Capability Phases + Handoff Criteria |
| Owned artifacts across lifecycle | Required Outputs + Ownership Matrix Template |
| Agent-usable delivery gates | Decision Rules + Cadence model in workflow |
| Cross-project portability | Depth Modes L4 + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- The project benefits from one explicit operating model instead of ad hoc local process.
- Artifact ownership is a stronger control than meeting-heavy coordination.

Trade-offs:

- One lifecycle model improves consistency but can feel heavier than informal team habits.
- Strong handoff criteria reduce ambiguity but can expose missing upstream work earlier.

Open blockers:

- Missing named owners weaken phase accountability.
- Existing local rituals may conflict with explicit artifact ownership.

Recommendation:

- Use this skill as the default project-management and delivery entry point for agent-heavy work. Then instantiate only the phases that materially add value for the project.

## Workspace Execution Contract

This workspace has a ratified delivery pattern that serves as the canonical operating model when this skill is invoked here. Agents must follow it in preference to constructing a model from scratch.

**Ratified plan:** [`.docs/plans/delivery/pattern/delivery-pattern-plan.md`](../../../.docs/plans/delivery/pattern/delivery-pattern-plan.md)  
**Status:** APPROVED 2026-05-06  
**Phase flow:** P1 Intake → P2 Research → P3 Plan (`G-PLAN`) → P4 Acceptance Criteria ‖ P5 ADRs → P6 TDD (`G-TDD`) → P7 Implementation → P7a Security ‖ P7b Performance ‖ P7c Governance Audit → P8 Quality Gate (`G-REVIEW`) → P9 Test Orchestration → P10 Release Readiness (`G-RELEASE`) → P11 Sync/Promotion → P12 Retrospective

Key constraints from the ratified plan:
- Full pattern applies to all deliveries — no abridged variant
- `release-simulation` mandatory when >3 asset files are changed
- Full PRD for new assets; one-page plan for updates
- Retrospective due within 5 business days or on-demand
- `G-TDD` may be satisfied by `code-reviewer` agent; human oversight required for high-risk or cross-cutting changes

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Default freshness threshold is 30 days.

## Pragmatic Stop Rule

Stop when each selected phase owns one output set, handoff rules are explicit, cadence is defined, and exception handling is auditable.

## Anti-Patterns

- Running delivery from ceremonies with no durable artifacts.
- Starting execution before ownership and done rules are explicit.
- Mixing release decisions into ordinary status updates.
- Treating retrospective findings as optional notes instead of operating-model inputs.

## Done Criteria

- Intake contract, ownership matrix, artifact set, cadence, and exception policy all exist.
- Selected phases have no unowned or multiply owned outputs.
- Handoff criteria and escalation rules are explicit.
- Final recommendation states adoption order and residual risk.
- Source catalog entries are current for this evaluation cycle.