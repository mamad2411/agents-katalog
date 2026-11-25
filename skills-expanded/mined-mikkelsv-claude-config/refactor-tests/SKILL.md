---
name: refactor-tests
description: "Audit test coverage after a code change and apply trivial test additions directly, deferring heavier gaps to a plan. Use whenever the user asks \"are we covered?\", \"do we need tests?\", adds a new command/handler/type, or after /audit-branch flags a test gap."
disable-model-invocation: true
---

# Test Coverage Review

Check if the test suite covers touched functionality. Trivial additions (adding a check to an existing test, one small new test) are applied directly inline. Heavier gaps — new test files, significant scaffolding, or coverage that requires design decisions — are deferred to a plan.

## Step 1: Load test framework

Discover the project's test setup at runtime rather than assuming one: read any test-pattern rules in the project's `.claude/rules/`, then locate the test projects or directories. `.claude/skill-config/test.md` — if present — already names the tiers and their commands; reuse it rather than re-deriving. Say what you found.

## Step 2: Scope

If orchestrator provided scope, skip to Step 3.

**Mode A** (no args): run `pwsh -NoProfile -File ".claude/scripts/git-diff-scope.ps1"` if that file exists, else `pwsh -NoProfile -File "$HOME/.claude/scripts/git-diff-scope.ps1"`. Abort if `MODE: none`.
**Mode B** (path/area): Glob relevant files, map to testable behavior.
**Mode C** (`all`): review full test suite vs full codebase.

## Step 3: Map changes to testable behavior

For each changed file, ask: Are there new public APIs, handlers, or commands? Did existing API behavior change? Are there new types or components? Were state transitions added or modified? Did any removed functionality leave existing tests referencing dead code? These are thinking prompts, not a fixed checklist — let what's actually in the diff shape the questions.

## Step 4: Cross-reference tests

Read the test sources for the current inventory. Categorize tests by concern (state roundtrips, serialization, UI interaction, domain logic) — derive the categories from what's actually in the test files; don't rely on a hardcoded list.

Look for:

- New functionality without tests.
- Stale tests referencing removed/renamed APIs.
- Partial coverage (only happy-path tested; edge cases missing).
- **"Verified live: N/N" standing in for coverage.** A live-verification note in a plan or commit records that someone watched it work once; it is a checklist for the permanent test, not a filled-in box. Diff those notes against the committed tests and either write the missing test or record the gap explicitly — an unrecorded one reads as covered forever, and the next reader has no way to tell the difference.
- **A "can't unit test this" note being inherited by proximity.** Such a note is scoped to the function it sits on, not its neighbours or the rest of the file. Re-check it per function — a file-level or nearby disclaimer is how a genuinely testable pure helper ends up permanently uncovered, because every later reviewer reads the note and moves on.

## Step 5: Report

**Coverage Summary** — per area: covered, partial, or uncovered.
**Gaps** — what's untested, severity (high/med/low), suggested test, effort (trivial/small/significant).
**Stale Tests** — tests referencing removed/renamed APIs.
**Verdict**: **Covered** / **Minor gaps** / **Needs new tests**. For trivial gaps (adding a check to an existing test), apply directly.

Adding a new test is always fair game here — a failure cannot supply the content of a test that did not exist. But changing an existing assertion *in response to a failing test* belongs to `/verify` (Phase D), which records the ordering; defer that one case rather than applying it inline.
