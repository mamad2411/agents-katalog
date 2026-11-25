---
name: "unit-test-writer"
pack: "automation-testing-pack"
purpose: "Design focused unit tests around single behaviors, branches, and contracts with clear setup, action, and assertion structure."
inputs: ["requirements or code under test", "function or class behavior", "edge cases", "dependencies or seams"]
outputs: ["unit test cases or skeletons", "assertion plan", "dependency strategy", "coverage notes"]
handoffs: ["mock-vs-stub-selector", "fixture-and-test-data-builder", "test-oracle-writer if present"]
---
# unit-test-writer

## Purpose
Design focused unit tests around single behaviors, branches, and contracts with clear setup, action, and assertion structure.

## Trigger this skill when
- You need automation work at this specific test level or concern rather than a vague “write some tests” request.
- You want explicit artifacts, assertions, and maintenance tradeoffs instead of brittle generated code.
- You need a reusable output that can hand off cleanly to the next testing skill.

## Expected inputs
- requirements or code under test
- function or class behavior
- edge cases
- dependencies or seams

## Deliverables
- unit test cases or skeletons
- assertion plan
- dependency strategy
- coverage notes

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
- mock-vs-stub-selector
- fixture-and-test-data-builder
- test-oracle-writer if present

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
