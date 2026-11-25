---
name: safe-refactoring
description: Restructures code in small steps that each keep behavior identical and tests green. Use it for renames, extractions, moves and cleanup of messy modules.
---

# Safe refactoring

A refactor changes structure, never behavior. If behavior must change, stop and say so.

## Steps

1. Run the existing tests and note the result. If the target code is not covered, write characterization tests first: call it with real inputs and assert today's outputs, even odd ones. Commit these separately.
2. State the goal in one line, for example "extract the pricing rules from OrderService". List the steps, each small enough to finish in minutes.
3. For each step: make one mechanical change, run the tests and the type checker, then commit. Use the editor or language tooling for renames and moves (`tsc`, `ruff`, `gofmt`, IDE rename) instead of search and replace.
4. Prefer these moves in order: rename, extract function, inline, move, introduce a parameter object, replace conditional with polymorphism. Keep old and new code side by side until callers are switched, then delete the old.
5. Search for every caller with grep, including strings, config, docs and tests, before changing a public signature.

## Rules

- Never mix a refactor with a bug fix or feature in one commit. If you find a bug, write it down and keep going.
- Do not change a test to make it pass. A failing test means the step changed behavior: revert it.
- Stop and ask if no test can reach the code and it cannot be exercised by hand.

## Report

The steps taken, the commits, test results before and after, bugs spotted but left alone.
