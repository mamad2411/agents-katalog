---
name: "fault-based-test-ideator"
pack: "verification-test-design-pack"
purpose: "Generate tests based on likely developer mistakes, common defect patterns, and known fragility in the design or code."
inputs: ["requirements or code", "defect history if available", "risk hotspots", "common bug patterns"]
outputs: ["fault hypotheses", "targeted tests", "bug pattern mapping", "risk-ranked defect probes"]
handoffs: ["negative-test-designer", "coverage-goal-planner", "review or inspection packs later"]
---
# fault-based-test-ideator

## Purpose
Generate tests based on likely developer mistakes, common defect patterns, and known fragility in the design or code.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- requirements or code
- defect history if available
- risk hotspots
- common bug patterns

## Deliverables
- fault hypotheses
- targeted tests
- bug pattern mapping
- risk-ranked defect probes

## Operating procedure
1. Identify likely mistake patterns such as off-by-one, null handling, logic inversion, stale state, and incorrect defaults.
2. Map each fault hypothesis to a focused test or probe.
3. Rank hypotheses by plausibility and impact.
4. Prefer defect-seeking tests over generic repetition.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- negative-test-designer
- coverage-goal-planner
- review or inspection packs later

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not invent exotic faults while ignoring common ones.
- Do not produce unranked lists with no rationale.
- Do not omit the link from fault hypothesis to concrete test.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Coverage / rationale
## Assumptions
## Open questions
## Recommended next skill
```
