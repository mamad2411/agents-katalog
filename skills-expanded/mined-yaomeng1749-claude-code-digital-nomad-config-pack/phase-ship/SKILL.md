---
name: phase-ship
description: Phase 6 of the software delivery workflow: perform final verification, prepare commits, write PR summaries, and hand off a completed change safely.
origin: ECC automation-pack
---

# Phase Ship

Use this skill when the user asks for `/phase-ship`, shipping, final verification, commit and PR preparation, or the final stage of a software delivery flow.

## Purpose

Move a verified change from local work to a clean commit or pull request.

## Workflow

1. Confirm the working tree scope and avoid staging unrelated user changes.
2. Run final verification or confirm recent verification is still valid.
3. Check for secrets, local files, debug code, and accidental artifacts.
4. Prepare a conventional commit message.
5. Create or update the commit only when requested or clearly part of the flow.
6. Prepare a PR summary:
   - what changed
   - why it changed
   - test plan
   - risks and rollout notes
7. If pushing or opening a PR, use the project’s GitHub workflow and keep branch names clear.

## Output

Include:

- final verification status
- commit hash if created
- PR URL if created
- test plan
- residual risks

End with `PHASE_SHIP_DONE` when shipped, or `PHASE_SHIP_BLOCKED`.
