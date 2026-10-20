# Inbox Sorter Workflow

This workflow exists to keep `data/inbox/` lightweight and durable.

- This workflow owns triage of rough captures, owner notes, and raw idea dumps.
- Prefer the lightest durable outcome that preserves the idea honestly.
- Keep this workflow focused on sorting and normalization, not roadmap invention for its own sake.
- Its unbounded repair loop contributes the inspected inbox to the shared
  continuation authority. Because inbox sorting has no task-decomposition
  consumer, a split or deferral preserves and yields the same run lineage.
- Triage covers the whole inbox, so one scope-local logical resource owns it
  through yield, recovery and publication. A queued successor observes the
  inbox only after that owner releases it; cooldown does not establish ownership.
