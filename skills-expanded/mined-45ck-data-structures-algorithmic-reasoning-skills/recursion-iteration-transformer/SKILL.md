---
name: "recursion-iteration-transformer"
pack: "data-structures-algorithmic-reasoning-pack"
purpose: "Convert between recursive and iterative formulations while preserving correctness, complexity, and readability."
inputs: ["current formulation", "base/termination conditions", "state carried across calls/loops", "space constraints", "readability goals"]
outputs: ["transformed formulation", "state mapping", "correctness cautions", "space/runtime notes", "preferred final form"]
handoffs: ["algorithm-trace-checker", "invariant-finder", "complexity-red-flag-detector"]
---
# recursion-iteration-transformer

## Purpose
Convert between recursive and iterative formulations while preserving correctness, complexity, and readability.

## Trigger this skill when
- You need a structure or algorithm recommendation grounded in the real workload.
- A current implementation choice feels arbitrary, costly, or hard to justify.
- You want to reason about correctness or performance before writing more code.

## Expected inputs
- current formulation
- base/termination conditions
- state carried across calls/loops
- space constraints
- readability goals

## Deliverables
- transformed formulation
- state mapping
- correctness cautions
- space/runtime notes
- preferred final form

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
- invariant-finder
- complexity-red-flag-detector

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
