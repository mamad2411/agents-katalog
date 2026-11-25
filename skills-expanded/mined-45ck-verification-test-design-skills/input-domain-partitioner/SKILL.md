---
name: "input-domain-partitioner"
pack: "verification-test-design-pack"
purpose: "Create a clean domain model of input classes, relationships, and constraints before selecting detailed tests."
inputs: ["requirements", "field definitions", "range and format rules", "cross-field constraints"]
outputs: ["input domain model", "equivalence class candidates", "cross-field restrictions", "selection guidance"]
handoffs: ["equivalence-partitioning-generator", "pairwise-test-generator", "negative-test-designer"]
---
# input-domain-partitioner

## Purpose
Create a clean domain model of input classes, relationships, and constraints before selecting detailed tests.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- requirements
- field definitions
- range and format rules
- cross-field constraints

## Deliverables
- input domain model
- equivalence class candidates
- cross-field restrictions
- selection guidance

## Operating procedure
1. Catalog every input, field, and cross-field dependency.
2. Group values into meaningful classes before choosing exact cases.
3. Record restrictions such as formats, uniqueness, cardinality, and cross-field rules.
4. Produce a partition map that downstream test design can reuse.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- equivalence-partitioning-generator
- pairwise-test-generator
- negative-test-designer

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not jump straight to test values before modeling the domain.
- Do not miss cross-field constraints.
- Do not mix unrelated dimensions into one class.

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
