---
name: "mindforge-ship"
description: "Create PR, run review, and prepare for merge after verification passes"
---

<objective>
Bridge local completion → merged PR. After /mindforge-verify-work passes, ship the work: push branch, create PR with auto-generated body, optionally trigger review, and track the merge.

Closes the plan → execute → verify → ship loop.
</objective>

<execution_context>
@.agent/workflows/mindforge-ship.md
</execution_context>

Execute the ship workflow from @.agent/workflows/mindforge-ship.md end-to-end.
