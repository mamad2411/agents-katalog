---
name: semwright-workflow-distillation
description: Use when repeated successful Semwright executions should be recorded, compiled into a deterministic Recipe candidate, verified, replayed, and promoted into a reusable capability.
---

# Workflow Distillation

Distill observed successful Semwright execution traces, never promises written in Markdown.

## Procedure

1. Start recording only with explicit intent. Choose `capture_values` deliberately; do not capture private values merely because they might help later.
2. Perform the workflow through ordinary Semwright capabilities and Broker policy.
3. Stop recording as successful only when the result has actually been verified.
4. Inspect patterns/suggestions. Repetition is evidence for a candidate, not permission to automate.
5. Compile a candidate Recipe. Parameterize genuine variation; do not bind opaque session refs as durable constants.
6. Run `workflow.verify` to validate the candidate against current descriptors and Recipe rules.
7. Replay successfully at least once under normal policy.
8. Promote only after static verification and a successful replay. Promotion becomes a normal `recipe.<slug>.run` capability.

After promotion, future Skills should reason about **when** the workflow applies and delegate the **how** to the verified capability.

See [capture](references/capture.md), [compile-and-verify](references/compile-and-verify.md), and [promotion](references/promotion.md).
