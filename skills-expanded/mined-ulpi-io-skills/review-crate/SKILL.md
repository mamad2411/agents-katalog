---
name: review-crate
version: 2.0.0
description: |
  Deep-audit ONE Rust crate end to end — read every file, don't sample: enumerate and read the whole
  crate, run its `cargo test`, check the existing `.ulpi/issues/<crate>.md` to avoid duplicates, then
  write or append evidence-backed findings (correctness, panic, validation, race, data-corruption,
  coverage gaps) each with severity and exact file:line — runs as a forked analysis workflow with its
  own reasoning budget, isolated from the main flow. Only valid if it actually read the entire crate;
  grounds every finding in real file:line evidence, labels uncertain claims INFERENCE, and never invents
  issues from intuition or writes outside this repository's issue file. Use when the user asks for a deep
  review of a single Rust crate.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
context: fork
agent: general-purpose
effort: high
argument-hint: "[crate path]"
arguments:
  - crate_path
when_to_use: |
  Use when the user explicitly asks for a deep review of one Rust crate. Examples:
  "/review-crate crates/hgdb-storage", "audit this crate", "deep review of hgdb-common". Do NOT use
  for branch-diff review (that's find-bugs), to fix the findings it records (that's bugfix-crate), or
  to sweep many crates in one pass — this reads one crate whole and produces its issue file.
---

<EXTREMELY-IMPORTANT>
This skill is only valid if it actually reads the whole crate.

Non-negotiable rules:
1. Enumerate and read every file in the target crate.
2. Run the crate's tests unless there is a concrete blocker.
3. Ground every finding in exact `file:line` evidence.
4. Check the current repository's canonical issue file before writing new findings.
5. Write findings only to `.ulpi/issues/<crate-name>.md` in this repository.
</EXTREMELY-IMPORTANT>

# review-crate

## Inputs

- `$crate_path`: Path to the crate directory

## Goal

Perform a complete crate audit that:

- reads the entire crate
- runs tests
- reports real bugs and coverage gaps
- updates the canonical local issue file without duplicating prior findings

## Step 0: Resolve crate identity

Determine:

- crate path
- crate name from `Cargo.toml`
- canonical issue file path: `.ulpi/issues/<crate-name>.md`

If the crate path is invalid, stop and say so clearly.

**Success criteria**: The crate and issue-file target are explicit before review begins.

## Step 1: Enumerate and read the whole crate

Read every file in the crate, including:

- `Cargo.toml`
- source files
- test files
- crate-local docs such as `CLAUDE.md`
- supporting docs in the crate directory

Do not sample. Do not stop after "main files".

**Success criteria**: You can honestly state that the whole crate was read.

## Step 2: Run crate tests

Run the narrowest full-crate verification that makes sense, typically:

- `cargo test -p <crate-name> -- --nocapture`

If tests cannot run, report the exact blocker.

**Success criteria**: The review includes real crate-test signal or a concrete reason it is unavailable.

## Step 3: Check the existing issue file

If `.ulpi/issues/<crate-name>.md` already exists:

- read it first
- avoid duplicating existing findings
- append only genuinely new issues

If it does not exist:

- create it when there are findings worth recording

**Success criteria**: The issue file remains canonical and non-duplicative.

## Step 4: Analyze and write findings

Look for:

- correctness bugs
- panic or crash risks
- validation gaps
- race or state issues
- data corruption risks
- performance traps that are clearly real
- coverage gaps around risky behavior

For each finding include:

- severity
- category
- exact `file:line`
- why the issue is real
- suggested fix direction

Label uncertain claims as `INFERENCE` and explain why they are uncertain.

**Success criteria**: Findings are evidence-driven and actionable.

## Step 5: Finish with residual risk

Report:

- files read
- test results
- findings written or appended
- remaining uncertainty or coverage gaps

If there are no material findings, say so explicitly.

**Success criteria**: The user understands both what was reviewed and what risk remains.

## Guardrails

- Do not write findings to external absolute paths outside this repository.
- Do not claim full review if files were skipped.
- Do not invent issues from intuition alone.
- Do not add `disable-model-invocation`; this is a valid deep-audit workflow.
- Do not turn this into a multi-crate sweep.

## Output Contract

Report:

1. crate reviewed
2. file count and statement that the whole crate was read
3. test results
4. findings by severity
5. issue file written or appended
6. residual risk or clean result
