---
name: test-e2e
description: Execute the repository's TESTS_E2E.md plan as a complete, autonomous end-to-end integration test — every phase sequentially, failures investigated and fixed immediately, everything logged to a timestamped protocol file. Use when the user asks for an e2e test, a full integration run, acceptance testing, stack verification, a regression run, or to "run the test plan" — with optional scope arguments like quick, no-build, or keep-up.
---

# test-e2e — Execute the E2E plan

**Goal**: Run the plan in `TESTS_E2E.md` (repository root) from scratch:
every phase in order, every step verified against its `Expect:`, every
failure fixed before moving on, everything logged to
`<protocol dir>/<protocol prefix>-YYYYMMDD-HHMM.md` (UTC timestamp at
start; create the directory if missing).

## Pre-flight

1. Locate `TESTS_E2E.md` at the repo root (or nearest ancestor containing
   one). **Missing** → tell the user no plan exists and offer to run
   `test-init` to generate it. Do not improvise a plan.
2. Read the whole plan. Take Meta (protocol dir/prefix), Scopes, Facts,
   Fixtures, Phases, Wrap-up.
3. Resolve the user's arguments against `## Scopes`. Unknown scope word →
   ask once now; after launch there is no interaction. No arguments →
   full plan.
4. Create the protocol file with its header (see format below); record
   the Environment commands' results; initialize counters
   (passed / failed / fixed / blocked / skipped).

## Critical rules

1. **Run autonomously without user confirmation.** Execute ALL commands
   (bash, file reads, edits, writes, docker operations, curl calls,
   service restarts) immediately without pausing for approval. This is an
   automated test suite — treat every tool call as pre-approved. Do not
   ask "should I continue?" — just do it.
2. **Fix failures immediately.** When a step's result contradicts its
   `Expect:`, do NOT skip it. Investigate the root cause, apply a fix,
   re-run the failing check until it passes, then continue. Check the
   step's `On fail:` hint and the plan's `## Facts` first — a Fact that
   declares the behavior expected means it is NOT a failure; never "fix"
   documented caveats.
3. **Log everything, as you go.** Every result (pass or fail), issue,
   fix, and retry goes into the protocol file the moment it happens —
   timestamps, exact error messages, files changed, before/after of
   fixes. Never batch protocol writes for the end.
4. **Retry timing issues once.** Connection refused / service still
   initializing → wait 15–30 seconds, retry once, then investigate.
   Per-step `Retry:`/`Timeout:` lines override this default.
5. **Never skip a phase on your own.** A phase that cannot pass even
   after fixes is logged `BLOCKED` with the reason, and the run
   continues. The only legitimate skips: `SKIPPED (scope)` for
   phases/steps excluded by the resolved scopes, and `BLOCKED (prereq)`
   for `needs-<x>` tags whose prerequisite is absent on this host
   (record which). External-dependency steps that fail clearly upstream
   (per plan Facts/tags) are `SKIPPED-EXTERNAL`, never silent passes.
6. **Scratch, not repo.** Runtime state (configs, data dirs, logs) lives
   in a fresh temp dir per run. The only repo writes allowed: the
   protocol file, Fixtures the plan declares, and fixes for real
   failures. `Destructive:` steps must target scratch or a path the plan
   explicitly names.
7. **Minimize console output.** One line per phase; the protocol file is
   the detailed log.

## Execution

Walk phases in plan order. Per phase: append the phase header to the
protocol, run each step (`Run:` commands; honor `Verify:` lists and
`Cleanup:` lines), judge strictly against `Expect:`, log the row, keep
counters. Per step verdicts: `PASS`, `FIXED` (failed → fixed → re-run
passed), `FAIL` (only when a fix could not be found — rare; explain),
`BLOCKED`, `SKIPPED (scope)`, `SKIPPED-EXTERNAL`.

## Wrap-up (always runs)

1. Execute the plan's `Re-run:` phases (prove fixes made during the run
   didn't regress anything).
2. If any repo file was changed by fixes: list them in the protocol with
   summarized diffs; leave changes uncommitted; flag them in the console
   summary.
3. Scratch cleanup: temp dirs, containers/images/volumes created by this
   run (unless a `keep-up`-style scope says otherwise).
4. Fill the protocol Summary table and final verdict:
   `PASS` (no FAIL, no BLOCKED) / `PASS with BLOCKED` / `FAIL`.
5. Process the plan's `Remind:` bullets in the console summary.

## Protocol file format

```markdown
# E2E Test Protocol — <project>

**Date**: YYYY-MM-DD HH:MM UTC
**Branch**: <current git branch>
**Commit**: <HEAD short hash>
**Plan**: TESTS_E2E.md (format v1, generated <date>) · Scope: <scopes or full>
**Environment**: <results of the plan's Environment commands>

## Summary

| Phase | Result | Tests | Passed | Fixed | Failed | Blocked | Skipped |
|-------|--------|-------|--------|-------|--------|---------|---------|

## Phase N: <name>

### Results

| # | Step | Result | Details |
|---|------|--------|---------|

### Issues & Fixes

#### Issue N.1: <title>
- **Error**: <exact error message>
- **Root cause**: <analysis>
- **Fix**: <what was changed>
- **Files modified**: <list>
- **Verified**: Yes/No

Total: N passed, N fixed-then-passed, N blocked, N skipped.
Repo files changed: <list or none>.
```

## Console output

One line per phase (`Phase 4 — live daemon … PASS (2 fixed)`), then a
final block: overall verdict, counters, protocol file path, repo files
changed by fixes (if any), and the plan's Remind items.
