---
name: "inheritance-vs-composition-advisor"
pack: "oop-code-structure-pack"
purpose: "Decide whether a relationship should be modeled through inheritance, composition, aggregation, or delegation."
inputs: ["class relationships", "reuse goal", "behavioral variance", "state ownership", "extensibility needs"]
outputs: ["relationship decision", "rationale", "tradeoff summary", "alternative structure proposal", "recommended next step"]
handoffs: ["class-responsibility-checker", "overloading-overriding-reviewer", "object-lifecycle-reviewer"]
---
# inheritance-vs-composition-advisor

## Purpose
Decide whether a relationship should be modeled through inheritance, composition, aggregation, or delegation.

## Trigger this skill when
- A base class feels forced.
- Reuse is being modeled structurally rather than behaviorally.
- You need to choose between subclassing and containment/delegation.

## Expected inputs
- class relationships
- reuse goal
- behavioral variance
- state ownership
- extensibility needs

## Deliverables
- relationship decision
- rationale
- tradeoff summary
- alternative structure proposal
- recommended next step

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
- class-responsibility-checker
- overloading-overriding-reviewer
- object-lifecycle-reviewer

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
