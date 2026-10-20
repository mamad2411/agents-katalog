---
name: design-mobile-ux
description: Use when defining or improving mobile UX for iOS and Android and you need an expert, source-backed workflow from research through wireframes, validation, and engineering handoff.
---

# Design Mobile UX

## Specialization

Provide an expert-level, source-backed workflow for designing and validating mobile UX across iOS and Android, with explicit platform-fit, accessibility, and handoff quality gates.

## Objective

Produce mobile UX artifacts that reduce implementation ambiguity, preserve platform conventions, and make success criteria measurable before engineering begins.

## Scope Boundaries

In scope:

- User-goal framing, journey design, and risk prioritization.
- Low-fidelity to mid-fidelity mobile wireframes.
- Platform-aware interaction decisions for iOS and Android.
- Accessibility, adaptive-layout, and validation planning.
- Implementation-ready UX handoff notes.

Out of scope:

- High-fidelity prototype production.
- Production code implementation.
- Release governance unrelated to the UX slice.

## Trigger Conditions

- A mobile feature needs research-backed UX direction before implementation.
- A current mobile flow has usability, accessibility, or drop-off problems.
- A team needs explicit mobile handoff artifacts instead of ad hoc design notes.

## Inputs

- User request context and target journeys.
- Platforms, device classes, and orientation constraints.
- Known analytics, support signals, app reviews, or research inputs.
- Business goal, success criteria, and evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Problem statement with target users, goals, and ranked UX risks.
- Task-flow and wireframe set covering primary, edge, and recovery states.
- Platform conventions summary for iOS and Android differences that matter.
- Accessibility and usability findings with severity and remediation cues.
- Engineering handoff package with behaviors, instrumentation, and validation loop.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Frame one mobile UX problem | One journey map and one wireframe set exist |
| L2 Delivery | Prepare one feature for implementation | Core flows, states, and handoff notes are complete |
| L3 Hardening | De-risk a release-bound mobile journey | Accessibility, adaptive layout, and validation evidence are explicit |
| L4 Expert Standardization | Define reusable mobile UX operating model | Reusable decision rubric, handoff package, and validation loop are documented |

## Deterministic Workflow

1. Lock target users, business goal, success criteria, and bounded journey scope.
2. Gather evidence from analytics, support signals, app reviews, prior tests, and interviews or session reviews.
3. Map top tasks, failure points, and journey assumptions that must be tested.
4. Produce task flows and wireframes for primary, empty, loading, success, error, and recovery states.
5. Apply platform conventions intentionally for navigation, back behavior, actions, gestures, and content hierarchy.
6. Validate adaptive layouts across phone and tablet classes in portrait and landscape where relevant.
7. Run quick usability checks, capture severity-ranked issues, and iterate on the wireframes.
8. Produce a handoff package with behavior rules, accessibility notes, event instrumentation, and open risks.
9. Define post-implementation validation metrics and a follow-up test loop.

## Platform and Interaction Heuristics

- Preserve native navigation expectations and system gestures.
- Keep one dominant action per screen and avoid competing calls to action.
- Show state transitions clearly for loading, success, warning, failure, and retry.
- Use content hierarchy and spacing to lower cognitive load on small screens.
- Keep adaptive behavior intentional instead of allowing uncontrolled stretch or collapse.

## Accessibility and Usability Heuristics

- Maintain readable typography, contrast, and focus order.
- Keep touch targets comfortably tappable with safe spacing.
- Provide meaningful labels and announced state changes for assistive technologies.
- Avoid gesture-only actions without visible or accessible alternatives.
- Make recovery paths explicit when a user fails or abandons a step.

## Validation Loop

Track these metrics per key journey:

- Task completion rate.
- Time to complete task.
- Error and recovery rate.
- Drop-off by step.
- Accessibility issue count.
- Repeat usage or feature adoption when relevant.

Validation loop:

1. Capture baseline metrics before the UX change.
2. Tie instrumentation to the critical journey steps.
3. Compare post-change behavior against success criteria.
4. Re-test the weakest steps with targeted usability sessions.
5. Feed findings into the next wireframe revision.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Research-backed mobile UX scope | Objective + Deterministic Workflow steps 1 to 3 |
| Platform-aware wireframes | Workflow steps 4 to 6 + Platform and Interaction Heuristics |
| Accessibility-aware design | Accessibility and Usability Heuristics |
| Implementation-ready handoff | Required Outputs + Workflow step 8 |
| Reusable mobile UX standard | Depth Modes + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Mobile UX quality depends on platform-fit and accessibility, not just visual polish.
- Teams benefit from wireframes that encode behavior and validation expectations.

Trade-offs:

- Strong platform-fit improves usability but can reduce cross-platform visual uniformity.
- Heavier upfront UX definition lowers engineering ambiguity but adds planning time.

Open blockers:

- Missing analytics or real user evidence weakens prioritization.
- Undefined device or orientation scope can invalidate adaptive-layout decisions.

Recommendation:

- Use L2 for bounded feature work and L4 when a team needs reusable mobile UX rules across projects.

## Source Governance Summary

- Active sources, evaluation date, and guidance deltas are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active source checks.

## Pragmatic Stop Rule

Stop when the target journeys, states, platform conventions, accessibility requirements, and handoff notes are explicit enough that engineering can implement without guessing core UX behavior.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Platform, accessibility, and adaptive-layout decisions are explicit.
- Validation loop is defined.
- Source catalog is current for this evaluation cycle.
