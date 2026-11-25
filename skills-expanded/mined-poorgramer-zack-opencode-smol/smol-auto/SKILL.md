---
name: smol-auto
description: Full pipeline non-stop — plan, build every atomic task, review. No mid-pipeline pauses. Use when you trust the agent to take a feature from idea to reviewed implementation in one shot.
---

# /smol-auto

Conductor enters Auto mode:
1. Invoke `planner` → produce `.smol/plans/<date>-<topic>.md` (via `smol_plan` tool).
2. For each atomic task in plan order:
   - Invoke `coder` to run RED → GREEN.
   - On test failure that the coder cannot resolve in one retry, halt the pipeline and report.
3. Invoke `reviewer` once across the full diff.
4. Emit a single final summary:
   - Tasks completed / skipped
   - Files changed
   - Reviewer verdict and issues
   - Wiki entries appended

Do not pause for user confirmation between tasks.
