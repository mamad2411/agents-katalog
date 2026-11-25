---
name: phase
description: Run the next (or a given) development phase of vibe-breakpoint from docs/plan.md — orchestrate analis → implementer → reviewer, verify the phase's acceptance checks, update status and decisions, and commit. Use when the user types /phase, /phase <number>, or /phase status.
---

# /phase — phase runner for vibe-breakpoint

Argument: `$ARGUMENTS` (empty, a phase number like `3`, or `status`).

## 0. Load context

Read, in this order: `CLAUDE.md`, `docs/status.md`, `docs/plan.md`, `docs/decisions.md`, `docs/spec.md`.

## 1. Pick the phase

- `status` → print a short table of phases and their status, the last log entry, and open items. **Stop.**
- A number → run that phase. If an earlier phase is not `done`, say so and stop, unless the user explicitly asked to run it anyway.
- Empty → run the first phase in `docs/status.md` whose status is not `done`.
- If the chosen phase is `blocked`, show the blocker from the log and stop.

Set the phase to `in-progress` in `docs/status.md`.

## 2. Handoff note

Create `.claude/work/phase-<N>-<slug>.md` with:
- the phase goal, tasks and acceptance checks (copied from `docs/plan.md`),
- the relevant contracts from `docs/spec.md` and decisions from `docs/decisions.md`,
- a "Findings / Verdicts" section for the agents to append to.

## 3. Orchestrate

Use the existing agents. Don't create new ones.

1. **analis**: break the phase into concrete tasks against the spec, list files to create or change, flag spec gaps. Writes into the handoff note.
2. **implementer**: implement the tasks, with tests.
3. **reviewer**: review against the spec, the product rules in `CLAUDE.md`, and the acceptance checks. May delegate test runs to **tester**. Verdict: `PASS`, `FIX` or `REANALYZE`.
   - `FIX` → back to implementer. `REANALYZE` → back to analis.
   - Maximum **3 review rounds**. If still not `PASS`, set the phase to `blocked`, write what's unresolved in the log, and stop.

If these agents are not available in this environment, do the same steps in the main session and say so in the summary.

Routine commands (npm, node, docker, git add/commit) run without asking.

## 4. Verify

- Run every acceptance check listed for the phase in `docs/plan.md`.
- Run `npm test`, `npm run typecheck`, `npm run build`.
- From Phase 1 on, also run `npm run test:e2e` for the parts that exist, and confirm:
  - **Project untouched:** fixture tree hash identical before/after, except `.vibe-breakpoint/`.
  - **Secrets:** no `FAKESECRET_` value appears in any output, log, compose file, bundle or test snapshot.
  - **Cleanup:** no container, network, volume or temp folder with the run label/prefix remains.
- If a check needs a human (e.g. "chart readable on a phone"), produce the artifact and list it under "Needs owner check" instead of claiming it passed.

## 5. Record

- `docs/status.md`: set the phase to `done` (or `blocked`); add a log entry with the date, what was built, which checks passed, anything left for the owner.
- `docs/decisions.md`: append new decisions as the next `D-0NN` with context and reason; mark resolved open items.
- Don't edit `docs/plan.md` except to tick task checkboxes. If the plan must change, record a decision and tell the owner.

## 6. Commit

`git add -A && git commit -m "phase <N>: <title>"`. **Do not push.**

## 7. Summary to the owner

Keep it short:
- what was built,
- acceptance checks: passed / failed / needs owner check,
- new decisions (IDs),
- the next phase, and anything the owner must do before it.

## Rules

- One phase per run. Don't start the next phase on your own.
- Never read real `.env*` files (`CLAUDE.md`, rule 3). `.env.example` is fine.
- Never point a test at a real database, public URL or production system.
- Stop and ask the owner only for decisions that change scope or product rules. Decide everything else yourself and log it.
