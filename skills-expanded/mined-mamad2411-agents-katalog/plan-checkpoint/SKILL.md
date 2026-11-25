---
name: plan-checkpoint
description: >
  Append a machine-readable checkpoint for an existing qualified TASK, optionally
  recording an explicit commit association. Use when saving task recovery state,
  checkpointing progress, or running /ultimate-sdd:checkpoint; use plan-handoff
  for authored session notes.
license: MIT
metadata:
  author: andrewr303
  version: "1.0"
---

A checkpoint records observations. It does not mark work done or make rollback safe.

**Read:** `references/recovery.md` before associating a commit or declaring file scope.

1. Resolve a real task as `REQ-n/TASK-k` from disk. If none exists, run `plan-resume` and report the gap; do not fabricate a task for a snapshot.
2. Append task state without a commit:

   ```
   python <plugin>/scripts/sdd.py checkpoint --repo <target> --root docs/plan --task REQ-n/TASK-k --json
   ```

3. Only when an exact commit is explicitly supplied, add `--commit <sha>`. It must resolve from a hexadecimal abbreviation or full hash to a full reachable non-merge commit using read-only git. Never fill it from observed HEAD, commit messages, or timing.
4. Add `--files <repo-relative-path> ...` only with `--commit` and only for the exact commit path scope. A declaration is not proof: ownership still needs current complete-gate evidence and matching source scope. Mixed scope or multiple task ownership cannot become a safe rollback candidate.
5. Report the appended record path, timestamp, task, observed graph Next, and git HEAD/dirty state, distinguishing the explicit association from proven ownership. An explicit commit can be checkpointed without ownership proof; rollback then fails conservatively.

## Guardrails

- Records are append-only JSON under the plan root's `runs/checkpoints/`. Do not rewrite past records, task status, or HANDOFF.
- Non-git checkpointing is supported without `--commit`. Git HEAD is an observation only; checkpoint never creates a commit.
- Use `plan-handoff` for narrative decisions and open questions. Checkpoints do not replace authored notes or fresh completion gates.
