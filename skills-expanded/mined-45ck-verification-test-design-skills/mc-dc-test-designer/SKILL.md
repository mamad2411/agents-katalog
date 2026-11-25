---
name: "mc-dc-test-designer"
pack: "verification-test-design-pack"
purpose: "Design tests showing that each atomic condition can independently affect the overall decision outcome."
inputs: ["compound Boolean decisions", "logic expression", "safety or rigor needs"]
outputs: ["MC/DC test set", "condition toggling evidence", "independence rationale", "coverage notes"]
handoffs: ["branch-coverage-designer", "test-oracle-writer", "coverage-goal-planner"]
---
# mc-dc-test-designer

## Purpose
Design tests showing that each atomic condition can independently affect the overall decision outcome.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- compound Boolean decisions
- logic expression
- safety or rigor needs

## Deliverables
- MC/DC test set
- condition toggling evidence
- independence rationale
- coverage notes

## Operating procedure
1. Decompose compound Boolean decisions into atomic conditions.
2. Find test pairs showing each condition independently affects the result.
3. Minimize redundant cases while preserving independence evidence.
4. Show the decision truth change for each condition.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- branch-coverage-designer
- test-oracle-writer
- coverage-goal-planner

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not toggle multiple conditions when demonstrating one condition’s independent effect.
- Do not confuse condition coverage with MC/DC.
- Do not skip logic expression decomposition.

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
