---
name: thermo-nuclear-code-quality-review
description: Extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. Use only when explicitly asked for a thermo-nuclear or thermonuclear code quality review, a deep code quality audit, or an especially harsh maintainability review.
user-invocable: false
---
## Overview

An unusually strict review of implementation quality, maintainability, abstraction quality, and codebase health. Above all, be ambitious about structure: do not stop at local cleanup. Actively hunt for the code judo move, a restructuring that preserves behavior while making the implementation dramatically simpler, smaller, more direct, and more elegant. Prefer deleting complexity over rearranging it.

Run this skill only on explicit request. The repo command schema has no `disable-model-invocation` field, so explicit-only is carried by the description wording and the slash command, not by auto-suggestion.

## Steps

1. **Read** `SKILL.md` (this file) and scope the diff: read the current branch's changes against its merge base, then list the files touched and the concepts each change introduces.
2. **Model the ideal shape first.** Before judging the diff, ask what the simplest behavior-preserving implementation would look like. That target is the bar.
3. **Hunt for the code judo move.** For every meaningful change, look for a reframing that makes whole branches, helpers, modes, conditionals, or layers disappear. Prefer the solution that feels inevitable in hindsight.
4. **Check structural health** against the Standards below: file size, spaghetti growth, directness, type and boundary cleanliness, canonical-layer ownership, and orchestration or atomicity.
5. **Prioritize and report.** Lead with structural regressions and missed simplifications, keep behavior identical, and prefer a few high-conviction findings over a long list of nits.

## Standards

Apply every standard. Treat each as a presumptive blocker unless the author justifies it clearly.

- **Be ambitious about simplification.** Look for the reframing that deletes categories of complexity, not the version that spreads the same complexity around. If a path deletes complexity, push hard for it.
- **Guard the 1000-line threshold.** Do not let a change push a file from under 1000 lines to over 1000 lines without a very strong reason. Prefer extracting helpers, subcomponents, or modules. If the diff crosses that line, ask whether to decompose first.
- **Block spaghetti growth.** Be highly suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches bolted onto unrelated flows. Push the logic into a dedicated abstraction, helper, state machine, or policy object instead of tangling an existing path.
- **Clean the design, do not just accept working code.** If behavior can stay the same while the structure gets meaningfully cleaner, push for the cleaner version. Do not rubber-stamp "it works" code that leaves the codebase messier.
- **Prefer direct, boring code over magic.** Treat brittle, ad-hoc, or magical behavior as a quality problem. Flag thin wrappers, identity abstractions, and pass-through helpers that add indirection without buying clarity.
- **Keep type and boundary contracts clean.** Question unnecessary optionality, `unknown`, `any`, or cast-heavy code when a clearer boundary could exist. If a branch leans on a silent fallback to paper over an unclear invariant, ask to make the boundary explicit.
- **Keep logic in its canonical layer.** Call out feature logic leaking into shared paths or implementation details leaking through an API. Reuse the existing canonical helper instead of a near-duplicate, and move logic to the package or module that already owns the concept.
- **Treat needless sequential orchestration and non-atomic updates as smells** when the cleaner structure is obvious: parallelize independent work, and restructure related updates so state cannot land half-applied.

## Primary review questions

- Is there a code judo move that makes this dramatically simpler?
- Can the change be reframed so fewer concepts, branches, or helper layers are needed?
- Did the diff add branching where a better abstraction should exist?
- Did a cohesive module become more coupled, more stateful, or harder to scan?
- Is this logic in the right file, layer, and package?
- Did the change enlarge a file or component past a healthy size boundary?
- Is the abstraction earning its keep, or is it just a wrapper?
- Did the diff add casts, optionality, or ad-hoc shapes that hide the real invariant?

## Preferred remedies

Prefer remedies that remove moving pieces over remedies that relocate them:

- Delete a layer of indirection rather than polishing it.
- Reframe the state model so conditionals disappear instead of getting centralized.
- Turn special-case logic into a simpler default flow with fewer exceptions.
- Extract a pure helper, or split a large file into focused modules.
- Replace condition chains with a typed model or an explicit dispatcher.
- Reuse the canonical helper; move logic to the module that owns the concept.
- Parallelize independent work, or make related updates atomic, when that also simplifies the flow.

Do not settle for "maybe rename this" when the issue is structural, and do not settle for a cleaner version of the same messy idea when a much simpler idea is plausible.

## Approval bar

Do not approve merely because behavior looks correct. Block, with explicit and actionable feedback, when any of these holds:

- a plausible code judo move would delete complexity the change instead preserves
- the change pushes a file from under 1000 lines to over 1000 lines without a strong reason
- the change adds ad-hoc branching that tangles an existing flow
- the change scatters feature checks across shared code
- the change adds an unnecessary wrapper, cast, or optionality that makes the design more indirect
- the change duplicates a canonical helper or puts logic in the wrong layer

## Guardrails

- This is a review: do not commit, push, merge, or run production scripts without consent; wait for an explicit request before any destructive git action.
- Flag exposed secrets or credentials; never print or commit a secret while reviewing.
- Keep behavior identical: propose restructuring, do not change what the code does.
- Be direct and demanding about structure, but raise pure cosmetic nits as non-blocking so they do not crowd out the structural findings.
