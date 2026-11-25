---
name: "negative-test-designer"
pack: "verification-test-design-pack"
purpose: "Design invalid, unexpected, hostile, or malformed-input tests that pressure the system’s error handling and resilience."
inputs: ["input model", "validation rules", "error-handling expectations", "security concerns if relevant"]
outputs: ["negative tests", "malformed input cases", "error expectation matrix", "resilience notes"]
handoffs: ["boundary-value-generator", "test-oracle-writer", "fault-based-test-ideator"]
---
# negative-test-designer

## Purpose
Design invalid, unexpected, hostile, or malformed-input tests that pressure the system’s error handling and resilience.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- input model
- validation rules
- error-handling expectations
- security concerns if relevant

## Deliverables
- negative tests
- malformed input cases
- error expectation matrix
- resilience notes

## Operating procedure
1. Generate invalid, malformed, missing, hostile, or unexpected inputs.
2. Target validation, parsing, error handling, and recovery paths.
3. Define what safe failure looks like for each case.
4. Prioritize cases that are both realistic and risky.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- boundary-value-generator
- test-oracle-writer
- fault-based-test-ideator

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not only test happy-path validation.
- Do not define failure without defining safe expected behavior.
- Do not ignore malformed and missing data cases.

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
