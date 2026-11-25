---
name: "boundary-value-generator"
pack: "verification-test-design-pack"
purpose: "Design tests around lower, upper, just-inside, and just-outside boundaries for numeric, ordered, sized, and count-based inputs."
inputs: ["requirements or constraints", "ranges or thresholds", "partition model if available"]
outputs: ["boundary cases", "off-by-one checks", "invalid edge tests", "boundary rationale"]
handoffs: ["equivalence-partitioning-generator", "negative-test-designer", "test-oracle-writer"]
---
# boundary-value-generator

## Purpose
Design tests around lower, upper, just-inside, and just-outside boundaries for numeric, ordered, sized, and count-based inputs.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- requirements or constraints
- ranges or thresholds
- partition model if available

## Deliverables
- boundary cases
- off-by-one checks
- invalid edge tests
- boundary rationale

## Operating procedure
1. Identify ranges, thresholds, counts, lengths, dates, or ordered values.
2. Generate cases at min, min+1, typical, max-1, max, and just-outside where relevant.
3. Include invalid and off-by-one probes, not just valid boundaries.
4. State why the chosen boundaries matter operationally.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- equivalence-partitioning-generator
- negative-test-designer
- test-oracle-writer

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not only test the boundary itself.
- Do not miss just-outside invalid cases.
- Do not assume all boundaries are numeric.

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
