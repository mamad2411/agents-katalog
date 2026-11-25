---
name: code-review
description: >
  Two-axis review of the diff since a fixed point: Standards (maintainability,
  structure, Fowler smell baseline) and Spec (faithful implementation of the
  originating spec). The Standards axis is an extremely strict maintainability
  audit that pushes for "code judo" moves that delete complexity. Use when asked
  to "code review", "maintainability review", "code quality audit", "/code-review",
  or "/review-quality".
disable-model-invocation: true
metadata:
  short-description: "Strict two-axis review: Standards & Spec"
provenance:
  origin: mattpocock-skills (fusion: two-axis review absorbed into strict maintainability review)
  license: MIT
  upstream_url: https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review
  maintained_by: my-skills
---

# Two-Axis Code Review

Review the diff since a fixed point along **two independent axes**:

- **Standards** — does the code follow the repo's documented coding standards and the strict maintainability bar below (structural simplification, abstraction quality, no spaghetti growth)?
- **Spec** — does the code faithfully implement the originating spec (`.plan/spec.md`, a commit-referenced task, or the user's described requirement)?

Report the two axes **separately** — do not merge or rerank findings. A change can pass one axis and fail the other: code that follows every standard but implements the wrong thing (Standards pass, Spec fail); code that does exactly what was asked but breaks the project's conventions (Spec pass, Standards fail). Keeping them separate stops one axis from masking the other.

## 1. Pin the fixed point and find the spec

1. **Fixed point**: the user supplies a commit SHA, branch, tag, `main`, `HEAD~5`, or you ask. Diff command: `git diff <fixed-point>...HEAD` (three-dot, merge-base comparison). Confirm it resolves (`git rev-parse`) and the diff is non-empty.
2. **Spec source**, in this order:
   1. `.plan/spec.md` in the repo (output of `sdd-spec`)
   2. Issue / task references in commit messages (`#123`, `Closes #45`, ticket ids)
   3. A path the user passes as an argument
   4. If nothing is found, ask the user. If they say there isn't one, the **Spec** axis is skipped and reports "no spec available".

## Standards Axis — Strict Code Quality Review

An unusually strict review focused on implementation quality, maintainability,
abstraction quality, and codebase health. Push the reviewer to be **ambitious**
about code structure -- not just local cleanup, but structural restructurings
that preserve behavior while making the implementation dramatically simpler.

### Core Prompt

> Perform a deep code quality audit of the current branch's changes.
> Rethink how to structure / implement the changes to meaningfully improve
> code quality without impacting behavior.
> Work to improve abstractions, modularity, reduce spaghetti code, improve
> succinctness and legibility.
> Be ambitious -- if there is a clear path to improving the implementation
> that involves restructuring some of the codebase, go for it.
> Be extremely thorough and rigorous. Measure twice, cut once.

### Non-Negotiable Standards

0. **Be ambitious about structural simplification.**
   - Do not stop at "this could be a bit cleaner."
   - Look for opportunities to reframe the change so that whole branches,
     helpers, modes, conditionals, or layers disappear entirely.
   - Prefer the solution that makes the code feel inevitable in hindsight.
   - Assume there is often a "code judo" move available: a re-organization
     that uses the existing architecture more effectively and makes the change
     dramatically simpler and more elegant.
   - If you see a path to delete complexity rather than rearrange it, push
     hard for that path.

1. **Do not let a PR push a file from under 1k lines to over 1k lines
   without a very strong reason.**
   - Treat this as a strong code-quality smell by default.
   - Prefer extracting helpers, subcomponents, modules, or local abstractions.
   - Only waive if there is a compelling structural reason.

2. **Do not allow random spaghetti growth in existing code.**
   - Be highly suspicious of new ad-hoc conditionals, scattered special cases,
     or one-off branches inserted into unrelated flows.
   - Prefer pushing logic into a dedicated abstraction, helper, state machine,
     policy object, or separate module.

3. **Bias toward cleaning the design, not just accepting working code.**
   - If behavior can stay the same while the structure becomes meaningfully
     cleaner, push for the cleaner version.
   - Strongly prefer simplifications that remove moving pieces altogether
     over refactors that merely spread the same complexity around.

4. **Prefer direct, boring, maintainable code over hacky or magical code.**
   - Treat brittle, ad-hoc, or "magic" behavior as a code-quality problem.
   - Flag thin abstractions, identity wrappers, or pass-through helpers that
     add indirection without buying clarity.

5. **Push hard on type and boundary cleanliness.**
   - Question unnecessary optionality, `unknown`, `any`, or cast-heavy code
     when a clearer type boundary could exist.
   - Prefer explicit typed models or shared contracts over loosely-shaped
     ad-hoc objects.

6. **Keep logic in the canonical layer and reuse existing helpers.**
   - Call out feature logic leaking into shared paths.
   - Prefer existing canonical utilities/helpers over bespoke one-offs.

7. **Treat unnecessary sequential orchestration as a design smell.**
   - If independent work is serialized for no good reason, ask whether it
     should run in parallel.
   - If related updates can leave state half-applied, push for atomicity.

### Primary Review Questions

For every meaningful change, ask:

- Is there a "code judo" move that would make this dramatically simpler?
- Can this change be reframed so fewer concepts, branches, or helper layers
  are needed?
- Does this improve or worsen the local architecture?
- Did the diff add branching complexity where a better abstraction should
  exist?
- Is this logic living in the right file and layer?
- Did this change enlarge a file or component past a healthy size boundary?
- Are there repeated conditionals that signal a missing model or helper?
- Is this abstraction actually earning its keep, or is it just a wrapper?

### Fowler Smell Baseline

On top of the repo's documented standards (a documented repo standard always wins — where it endorses something the baseline would flag, suppress the smell), always carry this fixed baseline of Fowler code smells (_Refactoring_, ch.3). Each smell is a labelled heuristic, never a hard violation; skip anything tooling already enforces. Each reads *what it is* → *how to fix*:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### What to Flag Aggressively

- A complicated implementation where a cleaner reframing could delete whole
  categories of complexity.
- Refactors that move code around but fail to reduce the number of concepts
  a reader must hold.
- A file crossing 1000 lines due to the PR.
- New conditionals bolted onto unrelated code paths.
- One-off booleans, nullable modes, or flags that complicate existing control flow.
- Feature-specific logic leaking into general-purpose modules.
- Thin wrappers or identity abstractions that add indirection without
  simplifying anything.
- Copy-pasted logic instead of extracted helpers.
- Bespoke helpers where the codebase already has a canonical utility.

### Preferred Remedies

- Delete a whole layer of indirection rather than polishing it.
- Reframe the state model so conditionals disappear.
- Change the ownership boundary so the feature becomes a natural extension
  of an existing abstraction.
- Turn special-case logic into a simpler default flow with fewer exceptions.
- Extract a helper or pure function.
- Split a large file into smaller focused modules.
- Replace condition chains with a typed model or explicit dispatcher.
- Delete wrappers that do not meaningfully clarify the API.

Do not be satisfied with "maybe rename this" feedback when the real issue
is structural.

### Review Tone

Be direct, serious, and demanding about quality. Do not be rude, but do not
soften major maintainability issues into mild suggestions.

Good phrases:

- `this pushes the file past 1k lines. can we decompose this first?`
- `this adds another special-case branch into an already busy flow. can we
  move this behind its own abstraction?`
- `this works, but it makes the surrounding code more spaghetti. let's keep
  the behavior and restructure the implementation.`
- `i think there's a code-judo move here that makes this much simpler. can
  we reframe this so these branches disappear?`
- `this refactor moves complexity around, but doesn't really delete it. is
  there a way to make the model itself simpler?`

## Spec Axis — Faithful Implementation

Check the diff against the originating spec. Report:

- **(a) Missing or partial** — requirements the spec asked for that are absent or only half-implemented.
- **(b) Scope creep** — behaviour in the diff that wasn't asked for.
- **(c) Wrong-looking implementations** — requirements that look implemented but where the implementation doesn't match what the spec described.

Quote the spec line for each finding. If no spec is available, report "no spec available" and skip this axis.

## Execution

Run both axes. For large diffs, run them as **parallel sub-agents** so their contexts don't pollute each other, then aggregate. For small diffs, a single pass covering both axes is fine — but always keep the findings under their own `## Standards` / `## Spec` headings, and never merge or rerank across axes.

### Output Structure

Prioritize findings within each axis:

**Standards axis** — in this order:
1. Structural code-quality regressions
2. Missed opportunities for dramatic simplification / code-judo restructuring
3. Spaghetti / branching complexity increases
4. Boundary / abstraction / type-contract problems
5. File-size and decomposition concerns
6. Modularity and abstraction issues
7. Legibility and maintainability concerns

Do not flood the review with low-value nits if there are larger structural
issues. Prefer a smaller number of high-conviction comments over a long list
of cosmetic notes.

**Approval bar (Standards)** — do not approve merely because behavior seems correct:

- No clear structural regression
- No obvious missed opportunity to make the implementation dramatically simpler
- No unjustified file-size explosion
- No obvious spaghetti-growth from special-case branching
- No unnecessary wrapper/cast/optionality churn
- No architecture-boundary leak or canonical-helper duplication

Presumptive blockers (unless the author can justify clearly):

- The PR preserves incidental complexity when a plausible code-judo move exists
- The PR pushes a file from below 1000 lines to above 1000 lines
- The PR adds ad-hoc branching that makes an existing flow more tangled
- The PR duplicates an existing helper or puts logic in the wrong layer

**Spec axis** — findings ordered by severity within each category (missing / creep / wrong).

End with a one-line summary: total findings per axis, and the worst issue *within each axis* (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent.
