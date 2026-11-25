---
name: "architecture-pass"
description: Run a local Architecture pass on the code that just changed — read the diff as a design, decide which concerns deserve their own module, who owns each piece of state, and which way data flows, then restructure the changed code to match without changing behavior, verify it, and record the result. Use whenever the user says architecture pass, structure the diff, clean up the structure of this change, make the changed code well-structured, tidy the shape of this feature, or has just finished a feature or fix and wants structural hygiene before review — even if they don't say "architecture".
---

# Role

You are running an **Architecture pass** on the code that just changed.

Step back from the diff and design the structure the changed code actually needs. Then restructure the code to match. This pass changes shape, not features: the program should do exactly what it did before, organized so that each concern can be understood on its own.

Three things keep this honest:

- **Proportionality.** Most passes are small. Do the small, local moves without ceremony; pause and show the design before anything that crosses a module boundary or leaves the diff.
- **Verified means you ran it.** "Behavior preserved" is a claim you demonstrate — with checks that passed before and after, and a real run of the changed behavior. Where you couldn't demonstrate it, say so in those words.
- **Doing nothing is a valid outcome.** If the diff is already well-structured, say so and stop. Restructuring for symmetry or taste is a cost with no return.

# Scope

## What counts as "the diff"

Decide this first and state it in your report. In order of preference:

1. Uncommitted changes (`git status`, `git diff`), if any.
2. The current branch against its base (`git diff <base>...HEAD`), if the user is on a feature branch.
3. The most recent commit(s) the user points to.

If it is ambiguous which the user means — uncommitted work on top of a multi-commit branch, say — ask one short question rather than guessing.

## What you may touch

- **The diff's files** — freely, within the rules below.
- **Immediate seams** — callers, imports, and tests that must change for the diff's files to keep working. These are consequences of the restructure, not expansions of scope.
- **Everything else** — out of scope. If restructuring the diff properly would require restructuring code around it, say so in the design note and let the user decide. Don't quietly widen the pass because the surrounding code "also needed it."

# Phase 1 — Read the diff as a design

Before moving anything, understand what the change does and how it is currently shaped. Read the diff and the files it lives in, not just the hunks. Then decide:

- **Concerns.** Which distinct responsibilities does this change carry (core logic vs. rendering, engine vs. interface, data vs. presentation, policy vs. mechanism, I/O vs. computation)? Which of them deserve their own module, and which are small enough to stay together? A concern earns a boundary when it would be understood, tested, or changed independently — not because a boundary would look tidy.
- **State ownership.** For each piece of state the diff introduces or touches: who creates it, who is allowed to mutate it, who reads it, and how long it lives. "Single owner" means one place creates and mutates; everyone else reads or asks. Distinguish source-of-truth state from derived state — derived state should be computed from its source, not kept in sync by hand.
- **Data flow.** Which direction does data move, and does anything flow backwards (a lower layer reaching up, a callback that mutates its caller's state, rendering code that imports the engine *and* the engine importing rendering)? Decide where the direction is, and where any cycle breaks.

Favor the simplest structure that keeps each concern understandable on its own. Boundaries exist for clarity, not ceremony; one more module is only an improvement if the thing it isolates is worth isolating.

## Write the design note

Three to six lines, in plain language: the concerns and where each lives, who owns each piece of state, which way data flows, and what you will **not** change and why. This is the thing you are about to make the code match, and the thing the user will check your work against.

## Proportionality gate

**Proceed without waiting** when every planned change is one of:
- moving code between the diff's own files, or within a file
- extracting or inlining a function or class inside one module
- renaming a symbol that is private to the diff's files
- deleting indirection you have confirmed unused (grep for every reference, including tests and dynamic lookups)

**Show the design note and wait for a yes** when any planned change:
- creates a new module or file
- moves code across an existing module boundary
- changes a public, exported, or externally-consumed signature
- touches files outside the diff for anything beyond import fixes
- changes who owns a piece of state in a way callers could observe (initialization order, lifetime, when a value becomes available)
- is something you cannot verify with the project's own checks

When in doubt, it's the second list.

# Phase 2 — Restructure

Make the code match the design note. Work in small mechanical steps and keep the checks green between them where the project's checks are fast enough to allow it.

- **Move logic to where it belongs.** Each concern lives in the module the design note gave it. Leave a thin call at the old location only if the old location is a seam other code depends on.
- **Give every piece of state a single owner.** When ownership moves, trace the lifecycle: where it is created now, where it was created before, and whether anything read it in between. This is the most common place a "shape-only" change alters behavior.
- **Collapse duplicated policy — carefully.** Collapse duplication when the copies exist for the same reason and would change together. Leave it when two pieces of code happen to look alike but answer to different concerns; merging those couples things that should drift apart. Two copies is often fine. Three that must change together is a signal.
- **Delete indirection the new structure no longer needs.** Before deleting an interface, adapter, or wrapper, confirm nothing else uses it: other callers, tests, reflection or string-based lookups, configuration, serialization. "I didn't see a use" is not "there is no use."

## What "preserve behavior" covers

Observable outputs, the order and presence of side effects, error types and messages, persistence and wire formats, public signatures, and timing-sensitive behavior where the project cares about it. If the restructure would change any of these — even for the better — stop and surface it as a separate decision. A behavior fix hidden inside a structural pass is the thing reviewers trust least.

## Keep the restructure separable

If the feature work is already committed, put the architecture pass in its own commit (or commits) so a reviewer can read behavior changes and shape changes separately. If everything is still uncommitted and the user has committed nothing yet, suggest the split rather than imposing it.

# Phase 3 — Verify

**Baseline first.** Before you move anything, run the project's own checks (tests, type-check, lint, build — whatever it has) and record the result. A failure that appears after restructuring is only attributable if you know it wasn't there before.

After restructuring:

- **Run the project's own checks again.** Report pass/fail per check, not a summary.
- **Do a real run of the changed behavior.** Exercise the actual feature or fix through its real entry point — the command, the endpoint, the UI flow, the script. Compare against the baseline where output is comparable. A passing test suite is not a real run unless the suite actually covers the changed behavior.
- **Say what the checks cover and don't.** If the changed behavior has no tests and you could not run it, the honest status is *unverified*, and the report says that. Do not describe a lint pass as verification of behavior.
- **If you cannot run the project** (missing environment, credentials, fixtures, hardware), say so plainly, say what you did instead (reading, tracing, type-checking), and leave the behavior status as unverified.

# Phase 4 — Record and report

## Record the structure

Briefly record the resulting structure — concerns and their homes, state owners, data-flow direction, and the reason for any non-obvious choice — so later work builds with it rather than against it. Put it where the project already keeps this kind of thing: `CONTEXT.md`, `ARCHITECTURE.md`, a module-level docstring, a `README` in the directory, or the PR description. Do not create a new documentation file without asking. If there is nothing non-obvious to record, say so rather than writing something decorative.

## Report

Use this shape:

```
## Architecture pass — <what was passed over>

**Treated as the diff:** <uncommitted / branch vs base / commits>

**Design:**
- Concerns: …
- State owners: …
- Data flow: …

**Changed:** <moves, merges, deletions — by file>
**Left alone, and why:** <things you considered and didn't do>

**Verified:**
- <check>: pass / fail (before: …, after: …)
- Real run: <what you exercised, how, result>
**Not verified:** <what, and why>

**Recorded at:** <path> / nothing worth recording / proposed, awaiting a yes
```

Keep "Verified" and "Not verified" as separate lists. Never fold an unrun check into a passing summary.

# When to do nothing

Stop after Phase 1 and say so when:

- the diff already has one concern per module, clear state ownership, and one-way flow
- the only improvements you can find are renames for taste or boundaries for symmetry
- the structure the diff "needs" is really a restructure of the surrounding application, which is out of scope

Report what you looked at and why you left it. That is a complete pass.

# Anti-patterns

- Restructuring for symmetry, taste, or because a pattern exists for it.
- Introducing an abstraction with one implementation to make the diff look "extensible."
- Collapsing duplication that is coincidental, coupling concerns that should drift apart.
- Deleting indirection on the strength of "I didn't see a use."
- Moving state ownership without tracing initialization order and lifetime.
- Quietly fixing a bug or changing an error message mid-restructure and calling it shape.
- Widening the pass into surrounding code without a yes.
- Reporting "tests pass" when only lint ran, or "behavior preserved" when nothing exercised the behavior.
- Writing a new ARCHITECTURE.md nobody asked for.
