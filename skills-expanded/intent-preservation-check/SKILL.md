---
name: intent-preservation-check
description: Compare an AI-generated product revision with confirmed product intent, constraints, and prior decisions to detect drift. Use after substantial changes to a brief, flow, prototype, interface, or implementation. Do not use to block intentional changes that have explicit evidence and ownership.
---

# Intent Preservation Check

Detect whether a new artifact silently changed decisions that humans had already made.

## Establish the comparison

1. Identify the baseline artifact or decision record and the revised artifact.
2. Extract confirmed intent: target user and job, product promise, conceptual model, terminology, critical task, constraints, quality bar, permissions, edge states, non-goals, and explicit human decisions.
3. Keep assumptions and preferences separate from confirmed decisions; they may change without constituting a violation.
4. Compare observable behavior and meaning, not only words or visual similarity.

## Classify changes

For each meaningful difference, classify it as:

- `Preserved`: intent remains intact despite implementation differences.
- `Intentional change`: evidence, owner, and rationale are recorded.
- `Unresolved`: the change may be valid but lacks a decision.
- `Drift`: confirmed intent was removed, contradicted, or obscured without authorization.

Prioritize drift affecting user control, permissions, safety, trust, recovery, product meaning, or the primary task. Do not demand pixel-level sameness unless visual precision was an explicit constraint.

## Output

```markdown
## Baseline and revision
## Confirmed intent inspected
## Change table
| Element | Baseline | Revision | Classification | Impact | Evidence |
## Critical drift
## Human decisions required
## Safe corrections
## Context or decision-record updates
```

## Boundaries

- Do not invent baseline intent when no trustworthy source exists.
- Do not label every difference as drift; preserve room for implementation judgment and evidence-backed evolution.
- Do not silently revert, overwrite, publish, or deploy an artifact.
- When sources conflict, expose the conflict and identify the decision owner.
- A passing check means known intent was preserved, not that the product is usable or valuable.
