---
name: "cfg-builder"
pack: "verification-test-design-pack"
purpose: "Convert code or pseudo-code into a control-flow graph suitable for structural test design and reasoning."
inputs: ["code or pseudo-code", "basic block boundaries", "branching logic"]
outputs: ["basic blocks", "CFG description", "entry/exit notes", "graph-based observations"]
handoffs: ["basis-path-tester", "statement-coverage-designer", "branch-coverage-designer"]
---
# cfg-builder

## Purpose
Convert code or pseudo-code into a control-flow graph suitable for structural test design and reasoning.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- code or pseudo-code
- basic block boundaries
- branching logic

## Deliverables
- basic blocks
- CFG description
- entry/exit notes
- graph-based observations

## Operating procedure
1. Group statements into basic blocks.
2. Mark branch and merge points plus entry and exit.
3. Describe the graph in text or adjacency style if drawing is unavailable.
4. Use the CFG to support structural test reasoning.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- basis-path-tester
- statement-coverage-designer
- branch-coverage-designer

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not blur basic block boundaries.
- Do not omit entry/exit semantics.
- Do not produce a graph that cannot support later coverage analysis.

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
