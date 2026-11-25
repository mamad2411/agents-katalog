---
name: "basis-path-tester"
pack: "verification-test-design-pack"
purpose: "Compute a basis set of independent execution paths from a control-flow graph and derive tests from them."
inputs: ["control-flow graph", "cyclomatic complexity if available", "code or pseudo-code"]
outputs: ["independent paths", "test set derived from basis paths", "complexity note", "residual risk note"]
handoffs: ["cfg-builder", "path-coverage-designer", "statement-coverage-designer"]
---
# basis-path-tester

## Purpose
Compute a basis set of independent execution paths from a control-flow graph and derive tests from them.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- control-flow graph
- cyclomatic complexity if available
- code or pseudo-code

## Deliverables
- independent paths
- test set derived from basis paths
- complexity note
- residual risk note

## Operating procedure
1. Build or use a CFG of the target logic.
2. Estimate cyclomatic complexity and identify independent basis paths.
3. Design tests that exercise each selected independent path.
4. State what complexity implies about residual risk.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- cfg-builder
- path-coverage-designer
- statement-coverage-designer

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not claim every path is covered just because basis paths are.
- Do not skip CFG quality.
- Do not ignore complexity warnings.

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
