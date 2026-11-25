---
name: "encapsulation-reviewer"
pack: "oop-code-structure-pack"
purpose: "Review fields, methods, and object interactions for information hiding, invariant protection, and leakage of internal state."
inputs: ["class definitions", "fields and methods", "mutation paths", "public API surface", "invariants if known"]
outputs: ["exposure findings", "invariant risks", "API surface recommendations", "state-protection suggestions", "follow-up actions"]
handoffs: ["visibility-modifier-reviewer", "immutability-opportunity-finder", "constructor-sanity-checker"]
---
# encapsulation-reviewer

## Purpose
Review fields, methods, and object interactions for information hiding, invariant protection, and leakage of internal state.

## Trigger this skill when
- Objects expose too much mutable state.
- Invariants can be broken from outside the class.
- APIs feel leaky or too permissive.

## Expected inputs
- class definitions
- fields and methods
- mutation paths
- public API surface
- invariants if known

## Deliverables
- exposure findings
- invariant risks
- API surface recommendations
- state-protection suggestions
- follow-up actions

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
- visibility-modifier-reviewer
- immutability-opportunity-finder
- constructor-sanity-checker

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
