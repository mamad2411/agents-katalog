---
name: "test-oracle-writer"
pack: "verification-test-design-pack"
purpose: "Define what counts as a correct result for each test so outcomes are observable, comparable, and not left to intuition."
inputs: ["requirements", "test cases", "business rules", "data expectations"]
outputs: ["test oracles", "expected outputs", "observable checks", "oracle assumptions"]
handoffs: ["negative-test-designer", "traceability packs later", "automation-testing packs later"]
---
# test-oracle-writer

## Purpose
Define what counts as a correct result for each test so outcomes are observable, comparable, and not left to intuition.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- requirements
- test cases
- business rules
- data expectations

## Deliverables
- test oracles
- expected outputs
- observable checks
- oracle assumptions

## Operating procedure
1. For each test, define the observable correct outcome.
2. Specify exact values, state changes, error messages, side effects, or invariants as relevant.
3. Avoid vague expectations like “works” or “should be okay.”
4. Record any assumptions where the spec is silent.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- negative-test-designer
- traceability packs later
- automation-testing packs later

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not leave expected results implicit.
- Do not use subjective pass/fail language.
- Do not ignore side effects or persistent-state changes.

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
