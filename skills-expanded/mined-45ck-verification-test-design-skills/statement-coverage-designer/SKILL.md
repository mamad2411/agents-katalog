---
name: "statement-coverage-designer"
pack: "verification-test-design-pack"
purpose: "Design the smallest practical test set that executes every reachable statement at least once."
inputs: ["code or pseudo-code", "CFG if available", "coverage target"]
outputs: ["test paths", "statement map", "unreachable statement notes", "coverage rationale"]
handoffs: ["cfg-builder", "branch-coverage-designer", "basis-path-tester"]
---
# statement-coverage-designer

## Purpose
Design the smallest practical test set that executes every reachable statement at least once.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- code or pseudo-code
- CFG if available
- coverage target

## Deliverables
- test paths
- statement map
- unreachable statement notes
- coverage rationale

## Operating procedure
1. Break code into statements or basic blocks.
2. Select tests that execute every reachable statement at least once.
3. Call out unreachable or dead code instead of pretending to cover it.
4. Map tests back to statements explicitly.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- cfg-builder
- branch-coverage-designer
- basis-path-tester

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not equate statement coverage with branch or logic coverage.
- Do not fake coverage over unreachable code.
- Do not omit statement-to-test mapping.

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
