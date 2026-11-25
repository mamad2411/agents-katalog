---
name: simplify
description: Review recent code changes for duplication, design quality, and runtime efficiency, then apply cleanup fixes directly. Use when the user asks to simplify code, clean up a patch, reduce duplication, improve maintainability, or run a post-implementation cleanup pass on changed files.
---

# Simplify

## Overview

Review the current diff or the most recent relevant edits with three lenses: reuse, code quality, and efficiency. Fix the worthwhile issues directly instead of only reporting them.

## Gather Review Scope

- Run `git diff` first.
- Run `git diff HEAD` if the current diff is empty or staged changes may be relevant.
- Fall back to the files the user named or the files edited most recently in the current session if git shows nothing useful.
- Use one shared patch or file set for every review pass so the findings stay comparable.

## Run Review Passes

Launch three independent review passes in parallel when agent delegation is available.
Perform the same passes locally when delegation is unavailable.
Wait for every pass to finish before deciding which edits to make.

### Reuse Pass

- Search for existing helpers, utilities, shared abstractions, and adjacent patterns before accepting new code as necessary.
- Flag newly added logic that duplicates an existing function, type guard, parser, formatter, or environment check.
- Replace hand-rolled code with existing utilities when the abstraction already exists and the behavior matches.

### Code Quality Pass

- Remove redundant state and cached values that can be derived cheaply.
- Collapse copy-paste variants into a shared helper when the differences are minor.
- Reduce parameter sprawl by restructuring call sites or lifting configuration into an existing abstraction.
- Tighten abstraction boundaries when a change leaks internal details across modules.
- Replace raw string switches or magic literals with existing constants, unions, enums, or branded types when available.
- Remove wrappers, nesting, and comments that do not add real value.
- Keep comments only when they explain a non-obvious constraint, invariant, or workaround.

### Efficiency Pass

- Remove repeated computation, duplicate I/O, redundant API calls, and unnecessary full-file reads.
- Parallelize independent work when the code currently performs it serially.
- Avoid adding blocking work to startup paths, hot request paths, or frequent render loops.
- Guard recurring updates so polling loops, listeners, and timers do not emit no-op changes.
- Verify that wrapper update helpers preserve a real no-change signal when callers return the same value or reference.
- Prefer direct operations with error handling over preflight existence checks that add race-prone churn.
- Check for memory growth, missing cleanup, and listeners or observers that can outlive their owner.

## Apply Fixes

- Fix the issues that clearly improve the code without changing intended behavior.
- Skip false positives or low-value churn quietly after checking them.
- Preserve unrelated user changes and avoid opportunistic refactors outside the reviewed scope.
- Re-run focused verification after edits when the project has relevant tests or linters.

## Close Out

- Summarize what was simplified and why.
- State clearly when the reviewed code was already clean enough that no changes were warranted.
