---
name: plan-handoff
description: >
  Preserve and update the authored session distillate so the next turn or
  post-compact session can resume from disk. Use when the user says handoff,
  session notes, rasen-handoff, or /ultimate-sdd:handoff. Use plan-checkpoint
  for machine-readable task snapshots.
license: MIT
metadata:
  author: andrewr303
  version: "2.3"
---

Conversation memory is not the plan. Preserve the distillate, not just the latest snapshot.

**Read:** `references/recovery.md` for authored handoff, checkpoint, and resume contracts.

## Procedure

1. Resolve the target repo and plan root. Read the entire existing `HANDOFF.md` before editing; preserve authored decisions, constraints, questions, and next-session warnings.
2. Run from the target repo, substituting its resolved plan root. Obtain a read-only draft and live state:

   ```
   python <plugin>/scripts/plan.py handoff --root docs/plan
   python <plugin>/scripts/sdd.py resume --repo <target> --root docs/plan --json
   ```

   The base draft summarizes Next, open REQs, active CHANGEs, and the current run; it does not write the file. Do not run base `handoff --write` unconditionally: that replaces the authored handoff.
3. Append or make targeted edits to the existing file after reading it. If missing, create a concise `HANDOFF.md`. Include only useful recovery notes:
   - Decisions made this session (one line each)
   - Files touched in the target repo
   - Open questions / `[assumed]` still live and unresolved diagnostics
   - What the next agent must **not** redo
   - The observed Next, labeled as historical session state rather than a standing instruction
4. If an existing task is known, persist its machine state with `plan-checkpoint`:

   ```
   python <plugin>/scripts/sdd.py checkpoint --repo <target> --root docs/plan --task REQ-n/TASK-k --json
   ```

   Do not auto-associate a commit from HEAD. If there is no task, keep the resume report and narrative gap; do not fabricate TASKs. PreCompact machine snapshots are handled separately by the hook.
5. At the next session or after compact, **read HANDOFF.md and call resume again**. Derive fresh Next from the graph; do not reconstruct it from chat or blindly follow the saved value.

## Guardrails

- Do not dump the whole INDEX or discard human additions to regenerate a handoff.
- Keep missing setup distinct from malformed state. Surface resume failures; do not hide them behind successful prose.
- No status transitions, application code changes, automatic test execution, or git mutations. Completion and rollback safety remain separate checks.
- No secrets. Env key names only.
