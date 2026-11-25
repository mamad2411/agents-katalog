---
name: "constructor-sanity-checker"
pack: "oop-code-structure-pack"
purpose: "Review constructors for clarity, invariant establishment, dependency sanity, and avoidance of hidden complexity."
inputs: ["constructor definitions", "dependencies", "defaults", "invariants", "usage examples"]
outputs: ["constructor findings", "invariant issues", "dependency concerns", "simplification options", "recommended changes"]
handoffs: ["object-lifecycle-reviewer", "encapsulation-reviewer", "immutability-opportunity-finder"]
---
# constructor-sanity-checker

## Purpose
Review constructors for clarity, invariant establishment, dependency sanity, and avoidance of hidden complexity.

## Trigger this skill when
- Constructors are long, surprising, or hard to call correctly.
- It is unclear where invariants are established.
- Object creation seems coupled to hidden behavior.

## Expected inputs
- constructor definitions
- dependencies
- defaults
- invariants
- usage examples

## Deliverables
- constructor findings
- invariant issues
- dependency concerns
- simplification options
- recommended changes

## Operating procedure
1. Identify the object-oriented concern this skill is meant to assess.
2. Separate facts from inferred design intent.
3. Review the current structure against OOP fundamentals: responsibility, invariants, ownership, exposure, abstraction, and lifecycle where relevant.
4. Surface concrete risks, tradeoffs, and improvement options.
5. Prefer minimal structural change that materially improves clarity or safety.
6. Hand off to the next most relevant skill if the issue is broader than this skill alone can resolve.

## Quality gates
- Findings are tied to concrete code structure or stated design intent.
- Recommendations explain *why*, not just *what*.
- Tradeoffs are stated when multiple designs could work.
- Output avoids style nitpicks unless they affect abstraction or maintainability.

## Handoff targets
- object-lifecycle-reviewer
- encapsulation-reviewer
- immutability-opportunity-finder

## Output style
- Be explicit about uncertainty.
- Prefer short, evidence-based findings over long vague critique.
- Distinguish design defects from mere preference.
- End with recommended next actions.

## Failure modes to avoid
- Do not invent framework constraints without evidence.
- Do not recommend sweeping refactors without naming the benefit.
- Do not confuse naming/style issues with true design problems unless they affect abstraction.
- Do not force inheritance, immutability, or statics as ideology.

## Minimum output skeleton
```md
## Summary
## Findings
## Risks
## Recommendations
## Tradeoffs
## Recommended next skill
```
