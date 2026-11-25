---
name: "constructor-simplifier"
pack: "design-for-testability-pack"
purpose: "Simplify constructors and object creation paths so units can be instantiated in tests with minimal setup and fewer hidden dependencies."
inputs: ["constructors", "factory/builders", "required collaborators", "default configuration"]
outputs: ["constructor simplification plan", "dependency reductions", "safe defaults", "test setup improvements"]
handoffs: ["dependency-injection-advisor", "pure-function-opportunity-finder", "api-contract-testability-checker"]
---
# constructor-simplifier

## Purpose
Simplify constructors and object creation paths so units can be instantiated in tests with minimal setup and fewer hidden dependencies.

## Trigger this skill when
- The current artifact is difficult to test directly or reliably.
- You suspect hidden dependencies, side effects, non-determinism, or awkward setup are harming test quality.
- You want design changes that improve testability before adding more tests.

## Expected inputs
- constructors
- factory/builders
- required collaborators
- default configuration

## Deliverables
- constructor simplification plan
- dependency reductions
- safe defaults
- test setup improvements

## Operating procedure
1. Read the code or design with a testability lens rather than a feature lens.
2. Identify collaborators, side effects, state transitions, environment assumptions, and setup cost.
3. Separate core logic from orchestration, effects, and framework concerns.
4. Surface the concrete causes of poor testability, not just the symptoms.
5. Recommend low-risk refactors or abstractions that improve controllability and observability.
6. Prioritize changes that reduce flakiness, setup burden, and mocking complexity.

## Quality gates
- Findings are specific to the artifact, not generic testing advice.
- Recommendations reduce coupling or non-determinism in a concrete way.
- Hidden I/O, time, randomness, or state dependencies are called out when present.
- Output separates findings, refactor options, tradeoffs, and next actions.

## Handoff targets
- dependency-injection-advisor
- pure-function-opportunity-finder
- api-contract-testability-checker

## Output style
- Be explicit about uncertainty.
- Prefer concrete examples over abstract advice.
- Separate facts, risks, refactor options, and recommended next step.
- Flag where a simpler design change beats a heavier testing workaround.

## Failure modes to avoid
- Do not prescribe mocks as the first answer to every problem.
- Do not hide framework coupling or hidden I/O behind euphemistic wording.
- Do not recommend invasive redesign when a small seam or abstraction is enough.
- Do not confuse code coverage with testability.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks
## Refactor options
## Recommended next skill
```
