---
name: "fixture-and-test-data-builder"
pack: "automation-testing-pack"
purpose: "Design fixtures and test data that make scenarios reproducible, minimal, realistic enough, and easy to maintain."
inputs: ["data model", "scenario list", "boundary values", "cleanup rules"]
outputs: ["fixture plan", "data sets", "cleanup/reset notes", "reuse opportunities"]
handoffs: ["unit-test-writer", "integration-test-writer", "api-test-suite-builder"]
---
# fixture-and-test-data-builder

## Purpose
Design fixtures and test data that make scenarios reproducible, minimal, realistic enough, and easy to maintain.

## Trigger this skill when
- You need automation work at this specific test level or concern rather than a vague “write some tests” request.
- You want explicit artifacts, assertions, and maintenance tradeoffs instead of brittle generated code.
- You need a reusable output that can hand off cleanly to the next testing skill.

## Expected inputs
- data model
- scenario list
- boundary values
- cleanup rules

## Deliverables
- fixture plan
- data sets
- cleanup/reset notes
- reuse opportunities

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
- unit-test-writer
- integration-test-writer
- api-test-suite-builder

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
