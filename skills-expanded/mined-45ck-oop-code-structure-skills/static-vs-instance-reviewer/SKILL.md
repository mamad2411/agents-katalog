---
name: "static-vs-instance-reviewer"
pack: "oop-code-structure-pack"
purpose: "Decide whether data or behavior belongs on the class, the instance, or neither."
inputs: ["class members", "access patterns", "state ownership", "call sites", "concurrency concerns if any"]
outputs: ["placement recommendations", "ownership rationale", "API design notes", "testability consequences", "recommended changes"]
handoffs: ["class-responsibility-checker", "visibility-modifier-reviewer", "object-lifecycle-reviewer"]
---
# static-vs-instance-reviewer

## Purpose
Decide whether data or behavior belongs on the class, the instance, or neither.

## Trigger this skill when
- There is debate over helper methods vs instance behavior.
- Shared state or utility classes are growing.
- Ownership of behavior is unclear.

## Expected inputs
- class members
- access patterns
- state ownership
- call sites
- concurrency concerns if any

## Deliverables
- placement recommendations
- ownership rationale
- API design notes
- testability consequences
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
- class-responsibility-checker
- visibility-modifier-reviewer
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
