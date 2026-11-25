---
name: "class-responsibility-checker"
pack: "oop-code-structure-pack"
purpose: "Check whether each class has a clear, coherent reason to change and a sensible responsibility boundary."
inputs: ["class/interface definitions", "method list", "field list", "usage context", "domain intent"]
outputs: ["responsibility assessment", "boundary problems", "split/merge suggestions", "reason-to-change analysis", "next refactor targets"]
handoffs: ["encapsulation-reviewer", "method-cohesion-checker", "inheritance-vs-composition-advisor"]
---
# class-responsibility-checker

## Purpose
Check whether each class has a clear, coherent reason to change and a sensible responsibility boundary.

## Trigger this skill when
- A class appears to do too many unrelated jobs.
- A service, entity, or controller has many reasons to change.
- You need to decide whether to split, merge, or redraw boundaries.

## Expected inputs
- class/interface definitions
- method list
- field list
- usage context
- domain intent

## Deliverables
- responsibility assessment
- boundary problems
- split/merge suggestions
- reason-to-change analysis
- next refactor targets

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
- encapsulation-reviewer
- method-cohesion-checker
- inheritance-vs-composition-advisor

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
