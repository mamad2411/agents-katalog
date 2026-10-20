---
name: mobile-orchestrator
description: Use when one MAUI mobile request spanning Android and iOS includes UX design, prototyping, implementation, accessibility, offline resilience, performance, and release hardening and needs one deterministic intake.
---

# Mobile Orchestrator

## Specialization

Use this skill to coordinate multi-surface MAUI mobile work from one intake when the request spans discovery, design, prototyping, implementation, hardening, or release readiness.

This skill is specialized for intake, phase ownership, and unified synthesis. It is not a replacement for deeper single-objective execution guidance inside any one mobile discipline.

## Objective

Produce one deterministic MAUI mobile execution contract for Android and iOS from a single intake, with explicit phase ownership, evidence expectations, and completion checks.

## Trigger Conditions

- A mobile request spans more than one capability area.
- Teams want one mobile intake instead of disconnected design and engineering workflows.
- Cross-project reuse matters more than one-off local optimization.
- A MAUI mobile change needs explicit ownership across UX, prototyping, implementation, accessibility, offline resilience, performance, and release hardening.
- The request must deliver for both Android and iOS unless an explicit exception is stated.

## Scope Boundaries

In scope:

- Deterministic mobile intake and phased execution planning.
- Phase-output ownership with exactly one owner per required output.
- Unified execution recommendation for mixed mobile design and delivery work.

Out of scope:

- Deep execution of any one specialized phase.
- Non-mobile product areas unless they materially constrain the mobile slice.
- Generic project governance unrelated to the mobile objective.

## Inputs

- User objective and target MAUI mobile surface.
- Scope boundaries, environments, platforms (Android and iOS), and risk level.
- Required outputs, known evidence, and time sensitivity.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Intake contract with objective, boundaries, and required outputs.
- Phase-output ownership matrix.
- Unified mobile execution recommendation.
- Rejected-candidate table with deterministic reason codes.
- Closure check stating whether all required outputs are owned.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Route one mixed mobile request | One intake and one phase contract exist |
| L2 Delivery | Coordinate one cross-surface mobile effort | Every required output has one owning phase |
| L3 Hardening | Support release-grade mobile work coordination | Risks, evidence expectations, and blockers are explicit |
| L4 Expert Standardization | Establish reusable mobile operating model | Reusable intake, ownership, and routing rubric are documented |

## Capability Catalog

Use one or more phases based on request shape:

- Experience Framing and UX Risks
- Platform Conventions and Adaptive Layouts
- High-Fidelity Prototype and Handoff Assets
- MAUI-Specific Implementation and Hardening
- Accessibility Quality Gate
- Offline Resilience and Recovery
- Performance Quality Gate
- Release Readiness and Promotion Evidence

## Deterministic Workflow

1. Lock the mobile objective, risk boundary, Android and iOS target platforms, and required outputs.
2. Classify the request into one or more capability phases from the catalog.
3. Assign exactly one owner per required output.
4. Reject any phase plan with unowned or multiply owned outputs.
5. Define evidence expectations and handoff criteria between phases.
6. Produce one unified execution recommendation: narrow execution, phased execution, or stop pending blockers.
7. Publish closure status with residual risks and unresolved blockers.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Phase | Evidence Expectation |
|---|---|---|
| User goals, key journeys, and ranked UX risks | Experience Framing and UX Risks | Journey map, assumptions, and severity-ranked risks |
| Platform-pattern and adaptive-layout decision | Platform Conventions and Adaptive Layouts | Platform conventions summary and layout constraints |
| Prototype or annotated handoff package | High-Fidelity Prototype and Handoff Assets | Tokens, states, annotations, and component mapping |
| MAUI-specific implementation path | MAUI-Specific Implementation and Hardening | Navigation, DI, storage, testing, and trimming notes |
| Accessibility findings and remediation path | Accessibility Quality Gate | Labels, focus order, touch-target, dynamic-type, and state-a11y evidence |
| Offline continuity and recovery decision | Offline Resilience and Recovery | Retry, stale-data, interruption, and recovery evidence |
| Performance findings and threshold decision | Performance Quality Gate | Startup, navigation, scroll, memory, and residual-risk notes |
| Release recommendation and promotion evidence | Release Readiness and Promotion Evidence | Signing, smoke, rollback, approvals, and store-readiness evidence |

## Unified Decision Rules

- `narrow-execution`: one phase owns the meaningful work and adjacent phases are only informational.
- `phased-execution`: two or more phases are required and ownership is unambiguous.
- `stop-pending-blockers`: required outputs are unowned, evidence is materially missing, or risk cannot be bounded.

## Rejected Candidate Reasons

- `R1`: Outside the mobile slice.
- `R2`: Adds overlap without adding required output coverage.
- `R3`: Expands scope beyond the bounded objective.
- `R4`: Requires evidence, platform access, or environment setup that is not currently available.
- `R5`: Better handled by a narrower single-phase workflow.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| One mobile intake | Objective + Deterministic Workflow |
| Phase ownership clarity | Phase-Output Ownership Matrix Template |
| Deterministic orchestration | Unified Decision Rules |
| Rejected-scope record | Rejected Candidate Reasons |
| Cross-project reusable contract | Capability Catalog + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Mixed mobile requests benefit from one intake and explicit output ownership.
- Most mobile work can be reduced to a small number of bounded capability phases.

Trade-offs:

- Strong orchestration reduces drift and duplicate work but adds upfront routing overhead.
- Over-bundling slows narrow requests that should stay inside one phase.

Open blockers:

- Missing platform constraints or release targets can invalidate a phased plan.
- Weakly bounded objectives create overlapping phase ownership.

Recommendation:

- Default to `narrow-execution` for one-surface mobile tasks and use `phased-execution` only when more than one phase clearly owns a required output.

## Source Governance Summary

- Active sources, evaluation date, and guidance deltas are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active source checks.

## Pragmatic Stop Rule

Stop when every required output has exactly one owner, the execution mode is explicit, and no blocker remains hidden behind ambiguous mobile scope.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Ownership matrix has no unowned or multiply owned outputs.
- Decision mode is explicit.
- Source catalog is current for this evaluation cycle.

