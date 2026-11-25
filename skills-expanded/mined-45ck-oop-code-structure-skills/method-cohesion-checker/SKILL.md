---
name: "method-cohesion-checker"
pack: "oop-code-structure-pack"
purpose: "Check whether methods are doing one coherent job, expose the right abstraction, and avoid mixed responsibility."
inputs: ["method bodies or summaries", "class role", "call graph hints", "side effects", "API intent"]
outputs: ["cohesion findings", "mixed-responsibility warnings", "split candidates", "abstraction notes", "recommended changes"]
handoffs: ["extract-method-refactor if present", "class-responsibility-checker", "naming-and-abstraction-reviewer"]
---
# method-cohesion-checker

## Purpose
Check whether methods are doing one coherent job, expose the right abstraction, and avoid mixed responsibility.

## Trigger this skill when
- Methods are long or mix orchestration with domain logic.
- A method appears to do several conceptual jobs.
- You need split candidates before refactoring.

## Expected inputs
- method bodies or summaries
- class role
- call graph hints
- side effects
- API intent

## Deliverables
- cohesion findings
- mixed-responsibility warnings
- split candidates
- abstraction notes
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
- extract-method-refactor if present
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
