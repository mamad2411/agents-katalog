---
name: plan-revert
description: >
  Preview a conservative rollback plan from explicit, proven task-to-commit
  associations without executing it. Use when asked to undo a TASK, REQ, or
  CHANGE, inspect rollback safety, or run /ultimate-sdd:revert.
license: MIT
metadata:
  author: andrewr303
  version: "1.0"
---

Preview only. A request to undo work does not authorize git mutations.

**Read:** `references/recovery.md` for ownership proof and refusal conditions.

1. Resolve one selector from disk: a qualified task, a REQ, or a CHANGE. Do not guess ownership from HEAD, messages, timing, filenames, or a `done` status.
2. Run exactly one of:

   ```
   python <plugin>/scripts/sdd.py revert-plan --repo <target> --root docs/plan --task REQ-n/TASK-k --json
   python <plugin>/scripts/sdd.py revert-plan --repo <target> --root docs/plan --target REQ-n --json
   python <plugin>/scripts/sdd.py revert-plan --repo <target> --root docs/plan --target CHANGE-n --json
   ```

3. On success, present only the runtime's exact explicit commit associations and proposed commands, newest-first. Explain the verified scope and that nothing was executed. Do not extend the plan with guessed commits or a broad reset.
4. On refusal, show the reasons and missing evidence with **no rollback commands**. Dirty state, merges, missing/unreachable commits, mixed path scope, multiple task ownership, or unprovable associations block a safe preview. Do not weaken checks to produce a plan.

## Guardrails

- Never execute the proposed commands, create commits, reset/restore/clean files, or mutate git history through this skill.
- No application or planning artifact edits to reconcile a hypothetical rollback. Status, truth specs, context, and HANDOFF remain untouched; report any follow-up review needed separately.
- No git means no rollback preview. Completion evidence is necessary for ownership checks but does not alone prove rollback safety.
