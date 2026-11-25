---
name: "equals-hashcode-reviewer"
pack: "oop-code-structure-pack"
purpose: "Review equality, identity, hashing, and value-object semantics so objects behave predictably in collections and comparisons."
inputs: ["class definitions", "equality semantics", "collection usage", "mutability characteristics", "language/runtime constraints"]
outputs: ["equality model summary", "risk findings", "contract issues", "collection-behavior warnings", "recommended changes"]
handoffs: ["immutability-opportunity-finder", "class-responsibility-checker", "naming-and-abstraction-reviewer"]
---
# equals-hashcode-reviewer

## Purpose
Review equality, identity, hashing, and value-object semantics so objects behave predictably in collections and comparisons.

## Trigger this skill when
- Objects are compared inconsistently.
- Types are used in sets/maps or caching.
- Value-object semantics are unclear.

## Expected inputs
- class definitions
- equality semantics
- collection usage
- mutability characteristics
- language/runtime constraints

## Deliverables
- equality model summary
- risk findings
- contract issues
- collection-behavior warnings
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
- immutability-opportunity-finder
- class-responsibility-checker
- naming-and-abstraction-reviewer

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
