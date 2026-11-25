---
name: smol-build
description: Execute the next pending atomic task from the latest plan in .smol/plans/, using strict TDD. Use after /smol-plan when stepping through tasks one at a time.
---

# /smol-build

Steps:
1. Locate the latest plan file under `.smol/plans/` (most recent date wins).
2. Pick the first `- [ ]` atomic task.
3. Delegate to the `coder` agent with that task description.
4. Coder runs RED → GREEN; reports tests passing.
5. Mark the task `- [x]` in the plan file.
6. Report which task ran, files changed, test result.

If no plan exists, tell the user to run `/smol-plan` first or use `/smol-fast`.
