---
name: "decision-table-builder"
pack: "verification-test-design-pack"
purpose: "Translate combinational business logic into a structured decision table and derive lean but sufficient tests."
inputs: ["business rules", "conditions", "actions or outcomes", "policy exceptions"]
outputs: ["decision table", "collapsed rule set", "test scenarios", "rule completeness notes"]
handoffs: ["pairwise-test-generator", "test-oracle-writer", "requirements-conflict-checker if present"]
---
# decision-table-builder

## Purpose
Translate combinational business logic into a structured decision table and derive lean but sufficient tests.

## Trigger this skill when
- You need disciplined test design rather than ad hoc case generation.
- You need to justify why a test set is sufficient.
- You want a reusable artifact that can feed automation later.

## Expected inputs
- business rules
- conditions
- actions or outcomes
- policy exceptions

## Deliverables
- decision table
- collapsed rule set
- test scenarios
- rule completeness notes

## Operating procedure
1. List the conditions and possible values that drive outcomes.
2. Enumerate or collapse rules into a clean decision table.
3. Mark impossible or forbidden combinations explicitly.
4. Derive a lean test set that covers each meaningful rule.

## Quality gates
- Be explicit about infeasible, unreachable, or assumption-heavy cases.
- Prefer lean, justified test sets over exhaustive-looking noise.
- Keep expected outcomes observable and tied back to rules or logic.
- Show why each test exists, not just the test data.

## Handoff targets
- pairwise-test-generator
- test-oracle-writer
- requirements-conflict-checker if present

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated lists.
- Tie tests back to rules, logic, or structure.
- Make expected outcomes observable.

## Failure modes to avoid
- Do not hide contradictory rules.
- Do not leave impossible combinations unmarked.
- Do not produce a giant table without pruning or explanation.

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
