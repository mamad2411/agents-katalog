---
name: "invariant-finder"
pack: "data-structures-algorithmic-reasoning-pack"
purpose: "Identify invariants, preservation conditions, and breakpoints that should hold across operations or iterations."
inputs: ["algorithm or data structure operations", "state transitions", "correctness goals", "loop/recursion points", "failure examples if any"]
outputs: ["candidate invariants", "where they are established", "where they are preserved or broken", "correctness notes", "test/proof prompts"]
handoffs: ["algorithm-trace-checker", "complexity-red-flag-detector", "data-structure-selector"]
---
# invariant-finder

## Purpose
Identify invariants, preservation conditions, and breakpoints that should hold across operations or iterations.

## Trigger this skill when
- You need a structure or algorithm recommendation grounded in the real workload.
- A current implementation choice feels arbitrary, costly, or hard to justify.
- You want to reason about correctness or performance before writing more code.

## Expected inputs
- algorithm or data structure operations
- state transitions
- correctness goals
- loop/recursion points
- failure examples if any

## Deliverables
- candidate invariants
- where they are established
- where they are preserved or broken
- correctness notes
- test/proof prompts

## Operating procedure
1. Identify the data or algorithmic concern this skill is meant to assess.
2. Separate facts about operations, sizes, ordering, and mutation from assumptions.
3. Review the current or proposed approach against the workload, invariants, complexity, and representation constraints.
4. Surface concrete risks, tradeoffs, and improvement options.
5. Prefer the least complex structure or algorithm that meets the stated needs.
6. Hand off to the next most relevant skill if the issue is broader than this skill alone can resolve.

## Quality gates
- Findings are tied to the stated workload or concrete algorithm steps.
- Recommendations explain why the choice fits the context.
- Tradeoffs are stated when multiple options are viable.
- Output distinguishes asymptotic concerns from practical implementation risks.

## Handoff targets
- algorithm-trace-checker
- complexity-red-flag-detector
- data-structure-selector

## Output style
- Be explicit about uncertainty.
- Prefer short, evidence-based findings over generic claims of efficiency.
- Call out hidden assumptions such as sorted input, bounded size, or low mutation.
- End with recommended next actions.

## Failure modes to avoid
- Do not recommend advanced structures without a workload that justifies them.
- Do not rely on Big-O alone when locality or constant factors dominate.
- Do not conflate proof of correctness with a single successful example.
- Do not ignore edge cases, degenerate inputs, or mutation semantics.

## Minimum output skeleton
```md
## Summary
## Findings
## Risks
## Recommendations
## Tradeoffs
## Recommended next skill
```
