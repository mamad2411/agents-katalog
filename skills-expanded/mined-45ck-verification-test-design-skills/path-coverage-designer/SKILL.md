---
name: "path-coverage-designer"
pack: "verification-test-design-pack"
purpose: "Identify meaningful execution paths and design tests while being explicit about infeasible or exploding path counts."
inputs: ["code or CFG", "path constraints", "loop handling assumptions"]
outputs: ["candidate paths", "selected paths", "infeasible path notes", "path-risk commentary"]
handoffs: ["basis-path-tester", "cfg-builder", "coverage-goal-planner"]
---
# path-coverage-designer

## Purpose
Identify meaningful execution paths and design tests while being explicit about infeasible or exploding path counts.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- code or CFG
- path constraints
- loop handling assumptions

## Deliverables
- candidate paths
- selected paths
- infeasible path notes
- path-risk commentary

## Operating procedure
1. Identify feasible paths through the control flow, accounting for loops carefully.
2. Avoid fake exhaustiveness when path counts explode.
3. Choose the most risk-relevant and independent paths.
4. Separate selected, infeasible, and omitted paths.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- basis-path-tester
- cfg-builder
- coverage-goal-planner

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not pretend all paths are feasible.
- Do not explode loops into nonsense path sets.
- Do not omit path-selection rationale.

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
