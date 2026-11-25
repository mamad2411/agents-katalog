---
name: "pairwise-test-generator"
pack: "verification-test-design-pack"
purpose: "Reduce combinatorial explosion by selecting a compact set of tests that covers all parameter pairs."
inputs: ["input parameters", "discrete value sets", "forbidden combinations if known"]
outputs: ["pairwise matrix", "reduced test set", "excluded combos", "coverage explanation"]
handoffs: ["decision-table-builder", "test-oracle-writer", "coverage-goal-planner"]
---
# pairwise-test-generator

## Purpose
Reduce combinatorial explosion by selecting a compact set of tests that covers all parameter pairs.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- input parameters
- discrete value sets
- forbidden combinations if known

## Deliverables
- pairwise matrix
- reduced test set
- excluded combos
- coverage explanation

## Operating procedure
1. List discrete parameters and their candidate values.
2. Note forbidden combinations or dependencies before generating pairs.
3. Construct a compact test set that covers every value pair at least once.
4. Explain what pairwise covers and what it does not.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- decision-table-builder
- test-oracle-writer
- coverage-goal-planner

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not use pairwise where sequence or higher-order interactions dominate.
- Do not include forbidden combinations as valid tests.
- Do not claim exhaustive interaction coverage.

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
