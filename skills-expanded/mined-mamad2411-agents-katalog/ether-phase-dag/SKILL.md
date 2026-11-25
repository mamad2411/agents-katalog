---
name: ether-phase-dag
description: Use when working on any change tracked under .ether/changes/ — explains the mandatory phase order (init, explore, proposal, spec/design, tasks, apply, verify, archive) and how it is enforced by hooks.
---

# Ether Phase DAG

This project is under Ether Harness enforcement. A PreToolUse hook hard-blocks
writes that skip phases. This is not advisory — violations are denied by the
hook, not just discouraged.

## Phase order (stages)

1. `init` — `ether init <change-id>` creates `.ether/changes/<id>/` and state.
2. `explore` — research, read code, understand the problem. Mark complete with `ether phase done explore`.
3. `proposal` — write `.ether/changes/<id>/proposal.md`. Completing this file auto-marks the phase.
4. `spec` and `design` (parallel stage) — write `spec.md` then `design.md` (design.md requires spec.md to exist — see the ether-artifact-deps skill).
5. `tasks` — write `tasks.md`.
6. `apply` — write actual project code. BLOCKED until `tasks.md` and `ac.md` both exist. `tasks.md` must list every touched file under a `## Files` section — `ether phase done apply` fails closed if any listed file has no paired test (default `src/X.ts` → `tests/X.test.ts`, configurable via `.ether/config.json`) or if the test suite doesn't pass. Missing-test failures name the exact test file to write; consult spec.md/design.md/ac.md for expected behavior before writing it. There is no auto-fix — Ether has no LLM/network calls, so you write the missing test yourself.
7. `verify` — run tests, write `evidence.md` with proof (test output, logs). `ether phase done verify` re-runs the same TDD gate as `apply` (same `## Files` coverage + passing suite) as a regression check before completing.
8. `archive` — write `archive.md` summarizing the shipped change. Writing the file auto-marks the phase via the PostToolUse hook. **Run `ether phase done archive` explicitly afterward** to complete the phase and record the change in the session summary.

## Commands

- `ether init <change-id>` — start a new change.
- `ether phase done <phase>` — mark a no-artifact phase (init/explore/apply/verify) complete. Fails if the previous stage isn't complete.
- `ether status [change-id]` — show current phase and completed phases.

## What happens on violation

A PreToolUse hook denies the tool call (exit code 2) with a message stating
exactly which file or phase is missing. Read the message and write the
missing artifact/run the missing command before retrying — do not attempt
to work around the block.
