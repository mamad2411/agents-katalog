---
name: "branch-coverage-designer"
pack: "verification-test-design-pack"
purpose: "Design tests that execute each decision outcome, including true and false branches and equivalent multi-way alternatives."
inputs: ["code or pseudo-code", "CFG if available", "branch conditions"]
outputs: ["branch coverage tests", "branch map", "missed-branch notes", "coverage rationale"]
handoffs: ["statement-coverage-designer", "path-coverage-designer", "mc-dc-test-designer"]
---
# branch-coverage-designer

## Purpose
Design tests that execute each decision outcome, including true and false branches and equivalent multi-way alternatives.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- code or pseudo-code
- CFG if available
- branch conditions

## Deliverables
- branch coverage tests
- branch map
- missed-branch notes
- coverage rationale

## Operating procedure
1. Identify every decision point and each possible outcome.
2. Design tests that force each branch outcome.
3. Distinguish branch coverage from statement coverage when branches share statements.
4. Document branches that cannot be forced and why.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- statement-coverage-designer
- path-coverage-designer
- mc-dc-test-designer

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not miss false branches.
- Do not assume branch coverage proves condition independence.
- Do not ignore exception or default paths where relevant.

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
