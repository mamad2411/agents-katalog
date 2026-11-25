---
name: xunit-orchestrator
description: Use when one xUnit request spans multiple capability areas and needs deterministic intake, explicit phase ownership, and a unified execution contract.
---

# xUnit Orchestrator

## Specialization

Use this skill to coordinate cross-project xUnit requests from one intake when work spans source curation, test design, fixture lifecycle, async behavior, Moq collaboration design, and quality-gate review.

This skill is specialized for intake, phase ownership, and unified synthesis. It does not replace deep execution guidance for any single phase.

## Objective

Produce one deterministic xUnit execution contract from a single intake, with explicit phase ownership, evidence expectations, and completion checks.

## Trigger Conditions

- A testing request spans multiple xUnit capability areas.
- Teams need one intake instead of disconnected test guidance.
- Cross-project reuse matters more than local one-off optimization.
- A change requires explicit ownership across test design, fixtures, async behavior, mocks, and release confidence.

## Scope Boundaries

In scope:

- Deterministic xUnit intake and phased execution planning.
- Phase-output ownership with exactly one owner per required output.
- Unified execution recommendation for mixed xUnit requests.

Out of scope:

- Product-specific implementation details unrelated to reusable testing patterns.
- Non-xUnit testing frameworks unless required for migration context.
- Generic project governance unrelated to the request objective.

## Inputs

- User objective and target test surface.
- Scope boundaries, environments, and risk level.
- Required outputs, known evidence, and delivery constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Intake contract with objective, boundaries, and required outputs.
- Phase-output ownership matrix.
- Unified xUnit execution recommendation.
- Rejected-candidate table with deterministic reason codes.
- Closure check stating whether all required outputs are owned.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Route one mixed xUnit request | One intake and one phase contract exist |
| L2 Delivery | Coordinate one cross-capability xUnit effort | Every required output has one owning phase |
| L3 Hardening | Support release-grade test behavior confidence | Risks, evidence expectations, and blockers are explicit |
| L4 Expert Standardization | Establish reusable xUnit operating model | Reusable intake, ownership, and routing rubric are documented |

## Capability Catalog

Use one or more phases based on request shape:

- Source Curation and Baseline Selection
- Test Design and Data Strategy
- Fixture Lifecycle and Context Isolation
- Async and Concurrency Test Behavior
- Collaboration Boundaries with Moq
- Evidence and Quality-Gate Decision

## Deterministic Workflow

1. Lock objective, risk boundary, target runtime, and required outputs.
2. Classify the request into one or more capability phases from the catalog.
3. Assign exactly one owner per required output.
4. Reject any phase plan with unowned or multiply owned outputs.
5. Define evidence expectations and handoff criteria between phases.
6. Produce one unified execution recommendation: narrow-execution, phased-execution, or stop-pending-blockers.
7. Publish closure status with residual risks and unresolved blockers.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Phase | Evidence Expectation |
|---|---|---|
| xUnit source baseline and version posture | Source Curation and Baseline Selection | Source catalog and rationale |
| Test shape decision (Fact vs Theory, data strategy) | Test Design and Data Strategy | Test matrix and data contract |
| Fixture scope and lifecycle decision | Fixture Lifecycle and Context Isolation | Fixture map and cleanup strategy |
| Async behavior and cancellation decision | Async and Concurrency Test Behavior | Await/cancellation assertion evidence |
| Moq usage boundary decision | Collaboration Boundaries with Moq | Mock seam map and interaction policy |
| Final confidence decision | Evidence and Quality-Gate Decision | Severity-ranked findings and verdict |

## Unified Decision Rules

- `narrow-execution`: one phase owns the meaningful work and adjacent phases are informational.
- `phased-execution`: two or more phases are required and ownership is unambiguous.
- `stop-pending-blockers`: required outputs are unowned, evidence is materially missing, or risk cannot be bounded.

## Rejected Candidate Reasons

- `R1`: Outside the xUnit testing slice.
- `R2`: Adds overlap without adding required-output coverage.
- `R3`: Expands scope beyond the bounded objective.
- `R4`: Requires evidence or environment access that is not available.
- `R5`: Better handled by a narrower single-phase workflow.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| One xUnit intake | Objective + Deterministic Workflow |
| Phase ownership clarity | Phase-Output Ownership Matrix Template |
| Deterministic orchestration | Unified Decision Rules |
| Rejected-scope record | Rejected Candidate Reasons |
| Cross-project reusable contract | Capability Catalog + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Mixed xUnit requests are higher quality when routed through one intake with explicit ownership.
- Most requests can be reduced to a small number of bounded capability phases.

Trade-offs:

- Strong orchestration reduces drift and duplicate work but adds upfront routing overhead.
- Over-bundling can slow narrow requests that should remain in one phase.

Open blockers:

- Missing runtime constraints or release criteria can invalidate the phase plan.
- Weakly bounded objectives create overlapping ownership.

Recommendation:

- Default to narrow-execution for localized requests and use phased-execution only when more than one phase clearly owns a required output.

## Source Governance Summary

- Active sources, evaluation date, and guidance deltas are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active source checks.

## Reference Assets

- Use [xunit-execution-contract-template.md](./references/xunit-execution-contract-template.md) when one xUnit request needs a reusable intake and ownership contract.

## Pragmatic Stop Rule

Stop when every required output has exactly one owner, the execution mode is explicit, and no blocker remains hidden behind ambiguous xUnit scope.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Ownership matrix has no unowned or multiply owned outputs.
- Decision mode is explicit.
- Source catalog is current for this evaluation cycle.


