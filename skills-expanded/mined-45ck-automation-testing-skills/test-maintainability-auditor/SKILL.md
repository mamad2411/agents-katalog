---
name: "test-maintainability-auditor"
pack: "automation-testing-pack"
purpose: "Audit the long-term maintainability of a test suite, including duplication, brittleness, overcoupling, and poor abstractions."
inputs: ["test suite structure", "common helpers", "duplication patterns", "history of test churn"]
outputs: ["maintainability findings", "refactor suggestions", "brittleness hotspots", "suite health notes"]
handoffs: ["regression-suite-curator", "test-readability-reviewer", "mock-vs-stub-selector"]
---
# test-maintainability-auditor

## Purpose
Audit the long-term maintainability of a test suite, including duplication, brittleness, overcoupling, and poor abstractions.

## Trigger this skill when
- You need automation work at this specific test level or concern rather than a vague “write some tests” request.
- You want explicit artifacts, assertions, and maintenance tradeoffs instead of brittle generated code.
- You need a reusable output that can hand off cleanly to the next testing skill.

## Expected inputs
- test suite structure
- common helpers
- duplication patterns
- history of test churn

## Deliverables
- maintainability findings
- refactor suggestions
- brittleness hotspots
- suite health notes

## Operating procedure
1. Clarify the target behavior, boundary, or automation goal and what would count as evidence.
2. Structure the test asset so setup, action, and assertions are observable and separated.
3. Minimize hidden assumptions around data, timing, environment, and ordering.
4. Produce lean outputs with enough rationale that another agent or developer can continue the work safely.

## Quality gates
- Prefer stable, explainable automation over superficially broad coverage.
- Keep assertions tied to observable outcomes, not vague expectations.
- Be explicit about flake risks, environmental dependencies, and setup or cleanup needs.
- Do not hide uncertainty; name assumptions and residual risk.

## Handoff targets
- regression-suite-curator
- test-readability-reviewer
- mock-vs-stub-selector

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to behaviors, contracts, or flows.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not over-automate unstable or poorly specified behavior without naming the risk.
- Do not create tests whose assertions are weaker than the stated goal.
- Do not bury fixture, selector, timing, or dependency assumptions.

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
