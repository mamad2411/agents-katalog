---
name: bugfix-crate
version: 3.0.0
description: |
  Work a Rust crate's recorded issue file to green — one finding at a time, disciplined and sequential:
  for each finding, write the failing regression test first, apply the smallest correct fix, run the full
  crate's `cargo test` and `cargo clippy -D warnings`, then mark the finding FIXED / Deferred / Not-a-bug
  in the issue file before moving on. Never marks a finding fixed without its verification pass, never
  batches findings, and never buries a warning under `#[allow]` or swaps a real fix for a comment — the
  issue file and crate state stay in sync after every fix. Use only when the user asks to fix findings
  from an existing crate issue file.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Skill
disable-model-invocation: true
user-invocable: true
argument-hint: "[path to .ulpi/issues/<crate>.md]"
arguments:
  - issues_file
when_to_use: |
  Use only when the user explicitly points at an existing crate issue file to repair. Examples:
  "/bugfix-crate .ulpi/issues/hgdb-storage.md", "fix the issues in this crate review", "work through
  the findings for hgdb-types". Do NOT use to produce that issue file in the first place (that's
  review-crate) or for broad multi-crate refactors — this skill is explicit-user-only and consumes
  findings that already exist.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill is a strict red-green-refactor repair loop.

Non-negotiable rules:
1. Fix one finding at a time.
2. For behavioral bugs, write the failing regression test before the fix.
3. Run crate tests and clippy after every fix.
4. Do not mark a finding fixed without the required verification.
5. Use the `rust` skill for crate-specific coding conventions before changing Rust code.
</EXTREMELY-IMPORTANT>

# bugfix-crate

## Inputs

- `$issues_file`: Path to the crate findings file

## Goal

Work through a crate issue file sequentially and leave behind:

- a verified fix for each resolved finding
- regression coverage for each behavioral fix
- a passing crate test suite
- an updated issue file showing what was fixed, deferred, or rejected as not-a-bug

## Step 0: Establish the baseline

Before editing:

- read the entire issue file
- determine the target crate name and path
- invoke `rust` for relevant conventions
- read crate-local `CLAUDE.md` or testing guidance if present
- run baseline `cargo test -p <crate>`
- run baseline `cargo clippy -p <crate> -- -D warnings`

**Success criteria**: The crate, issue file, and baseline state are explicit before the first fix.

## Step 1: Process one finding at a time

For each unresolved finding:

- read the cited file and surrounding context
- determine whether it is behavioral, API, dead-code, doc-only, deferred, or not-a-bug
- if it is a behavioral or API fix, write the failing test first
- verify the test fails before changing the implementation

Do not batch findings.

**Success criteria**: Each finding has a concrete resolution path before any fix lands.

## Step 2: Apply the smallest correct fix

Make the minimum code change that addresses the root cause.

Rules:

- do not batch adjacent refactors
- do not weaken existing tests
- do not hide warnings with `#[allow(...)]`
- if you uncover another real bug in the touched area, fix it in the same pass and add it to the issue file

**Success criteria**: The fix addresses the root cause without broad collateral edits.

## Step 3: Verify and mark status

After each fix:

- run `cargo test -p <crate>`
- run `cargo clippy -p <crate> -- -D warnings`
- update the issue file:
  - `**[FIXED]**` for verified fixes
  - `Deferred: <reason>` for real out-of-scope fixes
  - `Not a bug: <reason>` for invalid findings

Do not mark a finding fixed before the verification pass completes.

**Success criteria**: The issue file and crate state stay in sync after every finding.

## Step 4: Finish only when the issue file is resolved

At the end:

- confirm every finding has a terminal status
- confirm the crate still passes tests and clippy
- summarize resolved, deferred, and rejected findings

**Success criteria**: The issue file is fully triaged and the crate is green.

## Guardrails

- Do not use worktree agents for same-crate fixing.
- Do not run this skill proactively; it is explicit-user-only.
- Do not mark behavioral bugs fixed without regression coverage.
- Do not replace a real fix with comments, warnings, or documentation.
- Do not batch multiple findings in one verification loop.

## Output Contract

Report:

1. crate and issue file processed
2. baseline test and clippy state
3. per-finding outcome
4. final test and clippy state
5. any newly discovered findings added during repair
