---
name: plan-resume
description: >
  Recover current planning state read-only from the live graph, completion
  gates, checkpoints, and authored handoff. Use after an interruption or compact,
  when continuing a session, or when running /ultimate-sdd:resume.
license: MIT
metadata:
  author: andrewr303
  version: "1.0"
---

Recover what is true now, not what the last session expected.

**Read:** `references/recovery.md` for resume and failure contracts.

1. Resolve the target repo and plan root. Read its `HANDOFF.md` if present; preserve authored notes. A missing handoff is a reported gap, not a reason to invent one.
2. Run the read-only report:

   ```
   python <plugin>/scripts/sdd.py resume --repo <target> --root docs/plan --json
   ```

3. Report setup gaps, current graph-derived Next, fresh complete-gate results, latest checkpoints, and the HANDOFF path. Separate missing setup from malformed state; expose nonzero failures rather than presenting them as a successful resume.
4. Treat saved Next values and checkpoint git observations as historical. Use the live report to select the next action; do not infer task completion or commit ownership from them.
5. Surface conflicts between authored notes and live state without editing either. Route missing scaffolding to `plan-setup` only as an explicit follow-up; resume itself performs no repair.

## Guardrails

- No status updates, HANDOFF overwrites, new TASKs, test-command execution, or git mutations.
- Resume works without git; explain that explicit commit association and rollback preview require git.
- A failed completion gate remains visible even if a checkpoint exists. Completion and rollback safety are separate decisions.
