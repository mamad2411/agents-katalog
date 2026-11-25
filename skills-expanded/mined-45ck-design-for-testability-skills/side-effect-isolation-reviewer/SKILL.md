---
name: "side-effect-isolation-reviewer"
pack: "design-for-testability-pack"
purpose: "Review how well side effects are isolated from core logic so tests can focus on behavior without fragile environment setup."
inputs: ["code/design", "I/O boundaries", "state mutation points", "external integrations"]
outputs: ["side-effect map", "logic-vs-effect split", "isolation recommendations", "test strategy notes"]
handoffs: ["hidden-io-detector", "pure-function-opportunity-finder", "seam-finder"]
---
# side-effect-isolation-reviewer

## Purpose
Review how well side effects are isolated from core logic so tests can focus on behavior without fragile environment setup.

## Trigger this skill when
- The current artifact is difficult to test directly or reliably.
- You suspect hidden dependencies, side effects, non-determinism, or awkward setup are harming test quality.
- You want design changes that improve testability before adding more tests.

## Expected inputs
- code/design
- I/O boundaries
- state mutation points
- external integrations

## Deliverables
- side-effect map
- logic-vs-effect split
- isolation recommendations
- test strategy notes

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
- hidden-io-detector
- pure-function-opportunity-finder
- seam-finder

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
