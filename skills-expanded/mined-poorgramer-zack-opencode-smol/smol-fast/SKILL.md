---
name: smol-fast
description: Skip planning. Apply TDD directly to a small change described in the prompt. Use for bug fixes, single-file edits, or trivial features.
---

# /smol-fast

Steps:
1. Take the user's free-text description as the task.
2. Delegate to the `coder` agent.
3. Coder runs the standard RED → GREEN cycle.
4. Report files changed and test result.

Do not write a plan file. Do not invoke `planner`.
