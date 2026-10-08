---
name: create-tests-extract
version: 2.0.0
description: |
  Move a bulky inline test block out of its source file WITHOUT weakening it — same coverage, same
  private access: read the source and its inline tests, pick the smallest safe extraction boundary
  (an adjacent `#[cfg(test)] mod`, not a top-level `tests/`, when private access matters), move tests
  and their helpers with names and attributes intact plus the minimal module wiring, then run the
  narrowest relevant tests. Preserves the original visibility model and touches production code only as
  far as wiring requires — never silently downgrades private unit tests into weaker public-API
  integration tests. Use when the user asks to split large inline tests out of a source file.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Skill
argument-hint: "[source file or module to clean up]"
arguments:
  - request
when_to_use: |
  Use when the user explicitly asks to slim a source file by moving its large inline tests out.
  Examples: "extract these Rust tests", "move this giant #[cfg(test)] block out", "clean up this file
  by moving tests next to it". Do NOT use to author new test cases or fix failing ones (that's bugfix),
  and do NOT broaden it into a general refactor — it relocates existing tests without changing what
  they cover.
effort: high
---

<EXTREMELY-IMPORTANT>
The point is readability without semantic drift.

Non-negotiable rules:
1. Read the source file and its inline tests fully before moving anything.
2. Preserve the original visibility and helper access model.
3. Prefer adjacent test modules over integration tests when private access matters.
4. Change production code only as much as module wiring requires.
5. Run the narrowest relevant tests after extraction.
</EXTREMELY-IMPORTANT>

# create-tests-extract

## Inputs

- `$request`: Source file, module, or cleanup goal

## Goal

Move bulky inline tests into adjacent files while keeping:

- the same effective test coverage
- the same access to private items where needed
- a clearer production file

## Step 0: Read and classify the test block

Inspect:

- the production file
- the inline test module
- helper functions or fixtures used only by tests
- whether the tests depend on `super::*` or private module items

If the file belongs to a Rust crate, use `rust` for conventions before changing the module layout.

**Success criteria**: The tests are classified as local-inline, adjacent-module, or true integration candidates.

## Step 1: Choose the smallest safe extraction boundary

Prefer:

- `foo.rs` + `#[cfg(test)] mod foo_tests;` + `foo_tests.rs`
- or `foo/mod.rs` + `tests.rs` for directory modules

Avoid pushing tests into top-level `tests/` unless they genuinely should become public-API integration tests.

**Success criteria**: The new layout preserves the intended visibility model.

## Step 2: Extract without semantic drift

When moving the tests:

- add the minimal `#[cfg(test)] mod ...;` wiring
- keep `use super::*;` or equivalent imports when needed
- preserve test names and attributes
- move test-only helpers with the suite that needs them

Do not rename tests or restructure production modules unless the extraction requires it.

**Success criteria**: The moved tests still compile in the same effective context.

## Step 3: Verify the moved suite

After extraction:

- run the narrowest relevant tests
- check for warnings or visibility regressions
- verify the production file is materially easier to scan

**Success criteria**: The new layout passes and preserves behavior.

## Guardrails

- Do not turn private unit tests into public-only integration tests by accident.
- Do not move tiny, explanatory inline tests that still improve readability where they are.
- Do not broaden the refactor beyond the requested extraction.
- Do not drop fixtures or helper coverage just to shorten the production file.

## Output Contract

Report:

1. files created or modified
2. extraction layout chosen
3. any tests intentionally left inline
4. validation run after the move
