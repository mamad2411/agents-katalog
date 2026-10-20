---
name: web-ux-visual-consistency
description: Use when implementing or reviewing web UX visual consistency outcomes with deterministic design-token conformance checks and evidence-backed release recommendations.
---

# Web UX Visual Consistency

## Specialization

Use this skill to produce expert-level, agent-usable visual consistency outcomes for web UX surfaces.

## Objective

Reduce visual drift by validating design-token conformance, component state consistency, and predictable visual hierarchy.

## Trigger Conditions

- A release updates component styles, tokens, or visual hierarchy.
- Teams need objective visual consistency evidence for sign-off.
- Design system conformance is required before promotion.

## Scope Boundaries

In scope:

- Token usage, spacing rhythm, typography scale, and state styling consistency.
- Component visual state behavior across key journeys.

Out of scope:

- Brand strategy definition and creative concept work.

## Inputs

- In-scope journeys and components.
- Design token policy and component standards.
- Visual acceptance thresholds.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Visual consistency findings with severity and user-impact rationale.
- Token conformance matrix for in-scope components.
- Prioritized remediation backlog for visual drift.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope components and visual states.
2. Define conformance checks for token usage and state consistency.
3. Validate spacing, typography, and state treatments against policy.
4. Record drift findings and classify severity.
5. Assign remediation disposition with owner and due date.
6. Re-check high-impact drift after remediation.
7. Publish evidence artifacts and final recommendation.

## Visual Consistency Gate Checklist

- [ ] In-scope components use approved tokens.
- [ ] Typography and spacing follow policy scales.
- [ ] Default, hover, focus, disabled, and error states are consistent.
- [ ] No undocumented visual divergence in shared components.
- [ ] High and critical drift findings are resolved or deferred with owner and due date.

## Severity Model

- Critical: visual inconsistency blocks or misleads core user tasks.
- High: major inconsistency degrades trust and completion quality.
- Medium: clear drift with moderate impact.
- Low: minor style divergence.

## Evidence Contract

- `.docs/changes/<workstream-id>/visual-consistency-findings.md`
- `.docs/changes/<workstream-id>/token-conformance-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when token conformance checks are complete, high and critical issues are resolved or dispositioned, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

