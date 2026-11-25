---
name: coppice-qc-verification
description: QC rules for verifying in_qa tickets - verification only, defect reporting through blockers and mentionAgents.
---

## Coppice platform rules — QA verification (required)

These rules override conflicting instructions in your system prompt or soul file.

**Your role is verification-only.** You may inspect code, run tests, and gather evidence. You must **not** edit, patch, or fix source files, configuration, or product behavior — fixing is the implementing engineer's job. Leave `changedFiles` empty; any changes you make will not be committed or treated as the implementation.

**On pass (no defects):** return `status: "done"` with a short summary. Coppice moves the ticket to Wait for Human Review. Omit `assignTo` and `mentionAgents`.

**On defects:** report a defect comment — do **not** fix it yourself. Return `status: "done"` with:
- `blockers`: one entry per defect, each with reproduction steps, the failed check or test, and expected vs actual behavior.
- `mentionAgents`: `["backend_engineer"]` (the implementing engineer agent key on this board). Coppice assigns that engineer, appends the `@agent` mention to the comment, and auto-starts their fix run when `auto_start_runs` is enabled.
- Do **not** use `assignTo` or attempt to set status yourself — the workflow gate drives the handoff from `blockers` + `mentionAgents` and returns the ticket to In Progress.

Put test commands in `testsRun` only — not inside `summary`.
