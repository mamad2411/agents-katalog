---
name: implementation-standards
description: "Engineering criteria for implementation: SOLID, Clean Code, patterns, comment anchors, quality signals and simplification-first debt."
license: MIT
---

# Implementation standards

> Load this skill before writing or reviewing code. It is the **source of engineering criteria**;
> `.atlas/agents/engineer.md` is only a summary.

---

## SOLID

- **S** — one reason to change per class; one use case per application service.
- **O** — extend through composition, polymorphism and dependency injection before inheritance.
- **L** — subtypes must be substitutable without breaking invariants; prefer composition.
- **I** — keep interfaces small and specific to their consumer; no god interfaces.
- **D** — dependencies point toward the domain; high-level modules do not depend on low-level ones.
- Supporting concepts: cohesion, low coupling, encapsulation.

## Design patterns

- Apply them **only when the problem justifies it** and they reduce complexity.
- Premature abstraction is debt, just like duplication.
- Common: Factory, Strategy, Repository, Specification, Observer, Builder.

## Clean Code

- Meaningful names that reveal intent; no cryptic abbreviations.
- Small functions that do one thing.
- No dead, commented-out or unrefactored code.
- DRY with judgment: do not abstract for the sake of abstracting.

## Comment anchor (mandatory)

- Comments explain **why**, never what or how.
- Reference an **ADR** (`adr/NNNN-...`) or functional documentation.
- **Never** reference `openspec/specs/` (they are deltas that get archived).
- **Never** reference roadmaps, planning documents or other projects as the justification.
- If no ADR anchors the decision, the comment is **self-contained**: decision and reason, here and now.
- **Limits**: doc comment ≤ 3 lines; inline comment ≤ 2; decision block ≤ 6 and links to the ADR or
  document that holds the detail.
- **Do not repeat**: the same doc comment in N methods is duplication. Document it **once** on the class
  or the collaborator that owns the behavior.
- **Do not describe the "what"**: the name and types already say it. No signature or change history
  (git owns that).
- If it does not fit, the detail belongs in an ADR or functional documentation; the comment references it.
- A comment does **not** justify a lint threshold or a degraded design.

## Quality controls are signals, not goals

- Do not delete blank lines, split methods without cohesion or add trivial tests to pass a number.
- Do not raise the CRAP threshold so a change passes.
- Do not exclude files with real logic from coverage or CRAP.
- If a touched file has pre-existing lint violations, resolve them; do not leave debt "because it was
  not mine".
- If a limit is close, **refactor** or **document why** in the commit.

## Thresholds are analysis triggers, not a design excuse

- When a file/method size, complexity or CRAP threshold fires: **first remove duplication** (repeated
  boilerplate for logging, transactions or instrumentation is the usual cause), then extract
  **cohesive, typed collaborators**, and finally split responsibilities. A documented suppression is
  the **last** resort.
- **Do not** introduce bare strings, booleans or magic numbers to carry semantics (names, modes, kinds).
  Model them with an **enum, value object or interface** in its own file; that type also counts toward
  size.
- If the refactor was not planned in `design.md`, **declare it** in the change report (and in
  `design.md` if structural). No invisible refactors.

## Technical debt: simplification first

1. Extract Method / Extract Class.
2. Decompose Conditional / Replace Conditional with Polymorphism.
3. Introduce Parameter Object / Preserve Whole Object.

- Protected by the existing tests (green before and after).
- Additional tests are a **complement**, not a substitute for reducing complexity.
- Do not mask a complex method with tests that only cover the happy path.

## Tests

- Test behavior, not implementation details.
- No disabled tests, magic sleeps or trivial assertions.
- Cover error paths and business rules, not only the happy path.
