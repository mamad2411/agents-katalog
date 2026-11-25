---
name: code-quality
description: Writing and reviewing maintainable, correct code in any language. Use when writing new modules, reviewing code, refactoring, naming things, handling errors, or when the user says "clean this up", "code quality", "review this", "refactor", "is this good code", or "best practices".
---

# Code Quality

Code quality is not aesthetics. It is one measurable thing: **how fast can the next person (human or AI) change this code without breaking it?** Every rule below serves that.

## The hierarchy — when rules conflict, higher wins

1. **Correct** — handles the real input space, including the ugly parts (empty, null, duplicate, concurrent, huge, malformed).
2. **Honest** — the code's names, types, and structure tell the truth about what it does. No function named `validate` that also saves.
3. **Changeable** — the next likely change touches one place.
4. **Consistent** — matches the codebase around it. A "better" pattern that fights the codebase is worse.
5. **Small/clever/fast** — last, and only with evidence it matters.

## Writing rules

### Shape
- Functions do one thing at one level of abstraction. The test: can you name it accurately without "and"? Length is a symptom, not the rule — a 40-line straight-line function beats 5 fragmented ones you must chase.
- Depth over surface: prefer few functions with real behavior over layers of one-line delegation. Every hop a reader must follow is a cost; charge it against real value.
- Data shapes beat control flow: replacing an if/else ladder with a lookup table, an enum with exhaustive matching, or a well-typed state object usually deletes bugs. Make illegal states unrepresentable where the type system allows.

### Names
- Names carry the spec: `retry_delay_seconds` not `delay`; `is_eligible_for_credit` not `check`. If a good name is impossible, the abstraction is wrong.
- Booleans read as assertions (`is_`, `has_`, `can_`); functions as verbs; avoid negated booleans (`not_disabled`) that force double negation.

### Errors — where most "quality" issues actually live
- Handle or propagate, never swallow. An empty catch block is a bug with extra steps; catching broad `Exception` to log-and-continue hides corruption.
- Fail fast at boundaries: validate inputs where they enter (API edge, file load, config boot), then the interior trusts its inputs. Validation sprinkled everywhere means it's guaranteed nowhere.
- Error messages state what failed, with what input, and what the caller can do — written for the debugging session at 2 a.m.
- Distinguish expected failures (user error → typed error/result, clean message) from bugs (invariant broken → crash loudly). Converting bugs into handled errors hides them.

### State & dependencies
- Minimize mutable state; minimize its scope; make mutation obvious. Global mutable state is guilty until proven innocent.
- Side effects live at the edges; the core computes. A function that computes AND writes AND notifies is three functions wearing a trenchcoat.
- Take dependencies explicitly (parameters/constructor), not by reaching into globals — this is what makes code testable without patching.

### Comments
- Comment *why*, never *what*: constraints, non-obvious reasons, links to the decision. If the code needs a what-comment, rewrite the code.
- Delete commented-out code on sight; git remembers.

## Duplication — the nuanced rule

Duplication is cheaper than the wrong abstraction. Extract when the copies must change together *for the same reason* (shared business rule); keep copies when they merely look alike today (two forms with similar fields). Rule of three: tolerate two, refactor at three — and when you extract, extract the concept, not the coincidence.

## Refactoring discipline

- Never mix refactoring and behavior change in one commit; reviewers can verify "no behavior change" or "this specific change", not both at once.
- Refactor with a safety net (tests or at least a manual golden-path check), in steps that each keep the build green.
- Leave the campsite cleaner, but stay in the campsite: fixing everything you touch turns a 10-line PR into a 500-line hostage situation.

## Reviewing code (yours or others')

1. First pass — intent: does this change do what was asked, and only that? Flag scope creep and silent behavior changes.
2. Second pass — the input space: walk empty/null/zero/negative/duplicate/huge/concurrent/unauthorized through every new path.
3. Third pass — the seams: every external call (time, network, disk, DB) — what happens when it's slow, fails, or returns garbage?
4. Report defects as: input → wrong behavior → consequence. Rank by severity. Style nits go last, batched, and never block correctness discussion.
