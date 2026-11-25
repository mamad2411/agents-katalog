---
name: "equivalence-partitioning-generator"
pack: "verification-test-design-pack"
purpose: "Partition an input domain into valid and invalid equivalence classes and select representative tests from each class."
inputs: ["requirements or specification", "input fields or parameters", "business rules", "known constraints"]
outputs: ["equivalence partitions", "representative test set", "partition rationale", "coverage notes"]
handoffs: ["boundary-value-generator", "test-oracle-writer", "coverage-goal-planner"]
---
# equivalence-partitioning-generator

## Purpose
Partition an input domain into valid and invalid equivalence classes and select representative tests from each class.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- requirements or specification
- input fields or parameters
- business rules
- known constraints

## Deliverables
- equivalence partitions
- representative test set
- partition rationale
- coverage notes

## Operating procedure
1. Extract each input or parameter and the rules that constrain it.
2. Define valid and invalid equivalence classes that are disjoint and collectively useful.
3. Select one representative input from each class, then add extra cases only when justified.
4. Explain the rationale for each partition and test choice.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- boundary-value-generator
- test-oracle-writer
- coverage-goal-planner

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not create overlapping classes without explanation.
- Do not confuse representative tests with full coverage of a partition.
- Do not ignore invalid partitions.

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
