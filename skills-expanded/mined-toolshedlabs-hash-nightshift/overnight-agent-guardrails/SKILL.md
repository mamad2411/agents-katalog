---
name: overnight-agent-guardrails
description: >-
  Run a coding agent unattended overnight, long running agent safety, stop a
  runaway loop, cap agent token spend. Sets up four guardrails around an agent
  loop you already have: a resumable handoff file so an interrupted run
  continues, a verification gate that fails closed so unchecked work is never
  accepted, a runaway guard with an iteration cap and a wall clock deadline and
  a stop file, and a morning brief that puts the verdict on the first line.
  Use when a user asks to leave an agent running overnight, wants to bound what
  an unattended run can cost, or has had a run keep going and produce hours of
  unverified output. Pure bash, no dependencies, no loop of its own.
version: 1.0.0
---

# Overnight agent guardrails

Use this when a user wants to leave a coding agent running unattended and needs
the run to be bounded, resumable and checkable afterwards.

## When this applies

- "leave it running overnight", "run this unattended", "let it work while I sleep"
- a run that kept going and produced hours of output nobody verified
- wanting a hard ceiling on what one unattended run can cost

## What to do

The four scripts ship inside this skill directory, so there is nothing to fetch.
Refer to them as `$SKILL_DIR` below, meaning the folder this file is in.

1. Wrap the existing loop in the runaway guard. It exits nonzero when the run
   should stop, so it belongs in the `while` condition:
   ```bash
   while "$SKILL_DIR/runaway-guard" --max-iters 40 --max-minutes 480; do
     ... one bounded unit of work ...
   done
   ```
   At least one cap is required. It refuses to start with none, because an
   unbounded loop is the thing it exists to prevent.

2. Put the project's real checks behind the gate, so unchecked work is never
   accepted:
   ```bash
   "$SKILL_DIR/verify-gate" "npm test" "npm run lint"
   ```
   Nonzero means stop or escalate, rather than piling more work on a broken base.

3. Write the handoff file at the end of every unit of work, rewritten and not
   appended. `HANDOFF.md` in this directory is the template. A fresh run reads
   that one file and continues.

4. Record events as you go with `"$SKILL_DIR/nightlog"`, then produce the summary
   with `"$SKILL_DIR/morning-brief"`. The verdict lands on the first line.

## Notes

- `touch $NIGHTSHIFT_DIR/STOP` halts a running loop by hand. That is the whole kill switch.
- There is no daemon. State is one counter directory you can delete to reset.
- Everything is MIT and about 300 lines of bash. Reading it takes ten minutes.
