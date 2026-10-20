# Blocked Promoter Owner Decision

Owns the post-integration owner interaction for one blocked-task decision.

- This workflow has no repository access. It asks, waits, consumes the outcome,
  and emits a stable result for a fresh blocked-promoter writer transaction.
- Never apply task markers or promotions here; the writer revalidates current
  canonical task state before applying the result.
