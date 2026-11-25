---
name: test-manual
description: Conduct the repository's TESTS_MANUAL.md plan as a guided manual test — the USER runs every command and GUI action while Claude presents one step at a time, evaluates reported results, proposes (never applies unasked) fixes, and keeps the protocol file. Use when the user wants to test by hand, run commands themselves, do a guided walkthrough or acceptance session, or verify the app manually — with optional scope arguments.
---

# test-manual — Conduct the manual plan

**Goal**: Walk the user through `TESTS_MANUAL.md` (repository root) with
the **user executing every command and GUI action**. Claude conducts: one
step at a time, exact command/action + expected result up front, evaluate
what the user reports, log everything to
`<protocol dir>/<protocol prefix>-YYYYMMDD-HHMM.md` (UTC timestamp at
start; create the directory if missing).

## Pre-flight

1. Locate `TESTS_MANUAL.md` at the repo root (or nearest ancestor).
   **Missing** → say so and offer to run `test-init`. Do not improvise.
2. Read the plan: Meta, Scopes, Facts, Fixtures, Phases, Wrap-up.
3. Resolve arguments against `## Scopes`; unknown scope → ask. The user
   may also name phases directly ("just Phase 4 and 5").

## Critical rules (inverted from test-e2e)

1. **The user runs the commands and drives the GUI — never Claude.** Do
   not execute build, run, curl, kill, docker, or any stack-exercising
   command yourself, even if it would be faster. Present each shell
   command copy-paste-ready and suggest the `!` prefix (`! npm test …`)
   so its output lands directly in the conversation for evaluation.
   Present each GUI action as: what to click/drag/type, and exactly what
   should appear.
2. **One step at a time.** Present exactly one step: the command or
   action, what it does, and the expected result (exit code, key output
   lines, thresholds, visible UI state). Then stop and wait. Never dump a
   phase's worth of steps at once.
3. **Evaluate, don't assume.** When a report arrives, state PASS/FAIL
   against the `Expect:` explicitly and say why. Ambiguous or truncated
   report → ask for the missing piece (or a screenshot description)
   before judging. Check `## Facts` before judging — documented caveats
   are not failures.
4. **Propose fixes, apply only on instruction.** On failure: diagnose
   root cause, present the fix (file, before → after), and wait. The user
   decides — Claude applies it, the user applies it, or log-and-continue.
   Never edit code unasked.
5. **The user may skip.** Any step or phase can be skipped on request —
   log it `SKIPPED (user)` and move on. Missing prerequisites →
   `SKIPPED (prereq)`, recording which.
6. **Claude keeps the books.** Writing the protocol file, creating the
   protocol directory, and preparing inert Fixtures from the plan
   (scratch configs, broken-config samples, helper scripts) are Claude's
   job — offer each fixture before writing it, and never write into the
   repo except the protocol, plan-declared fixtures, and agreed fixes.
   Everything that *executes* is the user's.
7. **Retry guidance, not retry execution.** On timing-shaped failures
   (connection refused, still initializing) tell the user to wait 15–30 s
   and rerun once before treating it as a failure. Per-step `Retry:` and
   plan Facts (slow first compiles, known warm-up) override the default.
8. **Destructive steps are announced.** A step marked `Destructive:` is
   presented with its consequence stated plainly ("this wipes the app's
   cached state — binary selection will be gone") before the user runs it.

## Session flow

1. **Setup**: create the protocol file with the environment header — ask
   the user to run the plan's Environment commands and report, or accept
   "skip environment" and note it. Agree on a scratch directory (suggest
   `$(mktemp -d)`) — the user creates it.
2. Walk the phases in order (minus skips). Before each phase: one-line
   goal + step count. After each phase: one-line verdict, protocol
   updated.
3. **Wrap-up**: conduct the plan's `Re-run:` phases; summary table with
   totals (passed / failed / fixed / skipped); list fixes applied and by
   whom; surface the plan's `Remind:` bullets (uncommitted changes, spec
   checkboxes to tick — offer to tick them).

## Protocol file format

```markdown
# Manual Test Protocol — <project>

**Date**: YYYY-MM-DD HH:MM UTC
**Branch**: <current git branch>
**Commit**: <HEAD short hash>
**Plan**: TESTS_MANUAL.md (format v1, generated <date>) · Scope: <scopes or full>
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

**Who executed** is always the user for commands and GUI actions; quote
the user's pasted output or wording verbatim for anything FAIL, ambiguous,
or surprising. Issues & Fixes blocks per failure (root cause, fix
proposed, decision, who applied, state). Final summary table with totals.
Skips marked `SKIPPED (user)` / `SKIPPED (prereq)` / `SKIPPED (scope)`.

## Console style

Conductor voice, minimal — one step block at a time:

> **Step 4.2 — readiness probe.** Run: `curl -i http://127.0.0.1:9464/readyz`
> · Expect: `HTTP/1.1 200`, body `ready`. Paste the output (or run it with
> a leading `!`).

— then wait.
