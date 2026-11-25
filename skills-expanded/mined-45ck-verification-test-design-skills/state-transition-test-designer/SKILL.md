---
name: "state-transition-test-designer"
pack: "verification-test-design-pack"
purpose: "Create tests from states, events, guards, and transitions, including invalid or out-of-order sequences."
inputs: ["state model or workflow", "events/triggers", "transition rules", "guard conditions"]
outputs: ["transition tests", "invalid transition tests", "state coverage notes", "sequence scenarios"]
handoffs: ["negative-test-designer", "coverage-goal-planner", "test-oracle-writer"]
---
# state-transition-test-designer

## Purpose
Create tests from states, events, guards, and transitions, including invalid or out-of-order sequences.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- state model or workflow
- events/triggers
- transition rules
- guard conditions

## Deliverables
- transition tests
- invalid transition tests
- state coverage notes
- sequence scenarios

## Operating procedure
1. Identify states, allowed events, guard conditions, and resulting actions.
2. Create tests for normal transitions plus invalid or out-of-sequence actions.
3. Ensure initial, terminal, and recovery states are considered.
4. Document transition coverage and residual gaps.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- negative-test-designer
- coverage-goal-planner
- test-oracle-writer

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not ignore invalid transitions.
- Do not skip initial or terminal state behavior.
- Do not lose guard-condition reasoning.

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
