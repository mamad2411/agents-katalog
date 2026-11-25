---
name: "coverage-goal-planner"
pack: "verification-test-design-pack"
purpose: "Choose an appropriate coverage target for the situation and define what evidence is needed to claim it."
inputs: ["risk level", "code or model under test", "time budget", "quality expectations"]
outputs: ["coverage objective", "selected criteria", "evidence plan", "stop conditions"]
handoffs: ["statement-coverage-designer", "branch-coverage-designer", "path-coverage-designer"]
---
# coverage-goal-planner

## Purpose
Choose an appropriate coverage target for the situation and define what evidence is needed to claim it.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- risk level
- code or model under test
- time budget
- quality expectations

## Deliverables
- coverage objective
- selected criteria
- evidence plan
- stop conditions

## Operating procedure
1. Assess risk, criticality, complexity, and available time.
2. Choose suitable criteria such as EP/BVA, statement, branch, path, or MC/DC.
3. Define what evidence is needed to claim the chosen coverage.
4. Set stop conditions and residual-risk notes.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- statement-coverage-designer
- branch-coverage-designer
- path-coverage-designer

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not choose coverage criteria without context.
- Do not confuse measured coverage with product correctness.
- Do not set unattainable goals without noting cost.

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
