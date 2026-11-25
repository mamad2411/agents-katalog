---
name: rll
description: Alias for ralph-loop-loop. Run repeated ralph-loop unblock cycles, review PRs, merge safe PRs, and flag potentially destructive merges for user approval.
disable-model-invocation: true
---

# rll

This is a short alias for `ralph-loop-loop`.

Follow the same workflow and safety rules as `ralph-loop-loop`:
- iterate unblock issues with `ralph-loop`,
- review every PR,
- merge only safe PRs,
- flag potentially destructive merges to the user,
- repeat until all issues are closed and all PRs are merged or flagged.
