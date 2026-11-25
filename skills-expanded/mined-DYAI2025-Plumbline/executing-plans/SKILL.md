---
name: executing-plans
description: Use while carrying out an approved implementation plan, keeping task state, evidence, and deviations explicit.
---

# Executing Plans

## Per-task loop
1. Read the current plan item and its acceptance signal.
2. Claim only one task at a time.
3. Execute using TDD where code changes are required.
4. Update evidence: commands, files changed, decisions, and blockers.
5. Mark complete only when the stated acceptance signal passes.

If reality diverges from the plan, stop and update the plan rather than silently improvising.

