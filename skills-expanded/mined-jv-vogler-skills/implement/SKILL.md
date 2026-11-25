---
name: implement
description: The standard for writing and landing code — naming, control flow, comments, constants, purity — plus verifying the change, choosing a branch, and splitting the work into atomic commits with a message that matches the repository. Use whenever writing or modifying code: implementing a feature, fixing a bug, refactoring, migrating, or working through a task list; whenever reviewing your own diff before committing; and whenever deciding how to split changes into commits or what a commit message should say.
---

# Implement

How code gets written and landed, independent of where the work came from. A ticket, a bug
report, a plan phase, or a one-line request all end the same way: code that meets the standards
below, verified, and committed as reviewable units.

## Workflow

### 1. Choose the branch

Before touching code, ask the user whether to create a new branch or continue on the current one,
suggesting a name derived from the work (`feature-cart-discounts`, `fix-session-expiry`). Ask
once for the whole task, not per file or per commit. When running unattended with no stated
preference, stay on the current branch and say so in the report.

If the working tree already holds unrelated uncommitted changes, surface them before starting —
the commits should contain only this task's work.

### 2. Write the code

Follow the Code Writing Standards below on every line written. Match the surrounding code where
it already has a convention: its naming, module layout, error handling, and test style. A change
that reads as though it was always there is worth more than one that is locally cleaner but
foreign to the file.

Stay inside the requested scope. Fixing something adjacent that you noticed is a separate change
— mention it, don't fold it in.

### 3. Verify before calling it done

Run the project's tests, type checker, and linter for the code touched, and any acceptance
criteria the task defines. "It compiles" is not verification. If something fails and the fix is
outside the task's scope, stop and report it rather than working around it.

### 4. Commit

Commit in atomic commits: each one is a single logical change that builds and passes tests on its
own. A small, cohesive task is usually one commit; a task that mixes concerns — a refactor
enabling a feature, code plus docs — gets one commit per concern. Never bundle unrelated changes
into one commit, and never split one logical change across several.

Match the repository's existing commit message convention (check `git log`); absent one, default
to Conventional Commits — `type(scope): summary` — choosing the type that matches the change:
`feat`, `fix`, `refactor`, `test`, `docs`, `chore`. The summary says what the change does, not
which files moved.

### 5. Report

State what changed, the tests run and their results, and the branch and commits produced. Name
anything left undone and why. Keep it short enough to skim.

## Code Writing Standards

Apply these to every line of code written. To extend this list, add a new `###` subsection: a
named rule, the instruction, and a one-line reason.

### Names spell out meaning

No abbreviations or single-letter names — `qty`, `amt`, `cfg` make the reader decode instead of
read. The only exceptions are near-universal conventions: loop indices `i`/`j`, comparators
`a`/`b`, math `x`/`y`, caught errors `e`/`err`, event `e`, and infra names `id`, `db`, `ctx`.

### Return early

Prefer guard clauses over nested conditionals and keep cyclomatic complexity low — the happy path
should read top-to-bottom without indentation debt. Never nest ternaries; a ternary that needs
another ternary needs a function.

### Comments explain why, never what

Make code self-explanatory by extracting well-named functions and variables instead of annotating
opaque blocks. Reserve comments for context the code cannot carry: a constraint, a workaround, a
non-obvious "why".

### No magic numbers

Move literal values and configuration into named constants, enums, or config objects. A name
documents intent; a bare number forces every reader to reverse-engineer it.

### Pure by default

Favor pure functions and determinism; avoid mutating values and hidden side effects. When side
effects are necessary, isolate them in the layer that owns them (IO, infrastructure) so core logic
stays predictable and testable.
