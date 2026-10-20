---
name: plan-orchestrating
description: Authors, maintains, and orchestrates implementation of plans stored under .plans/. Covers writing new plans (contracts, touchpoints, concept boundaries), updating checklists during implementation, moving completed sub-plans from pending/ to implemented/ and updating .plans/plan.md's tables, and executing "Ready to Implement" plans (single plan directly, multiple plans via sequential subagent delegation with commit-on-success/stop-on-failure). Use when a user asks to "create a plan", "write a plan", "run plans", "implement plans", "execute pending plans", or "orchestrate plan execution".
---

`.plans/plan.md` is the master index for a project's plans. Use this exact casing when creating it; do not rename an existing master index file just to match this casing. It contains a checklist of all sub-plans, organized into "Ready to Implement", "Not Ready", and "Completed" tables.

Each sub-plan lives in `.plans/pending/` or `.plans/implemented/` and has a checklist at the top listing its implementation steps.

## Writing Plans

Plans describe **what** needs to exist at boundaries, not **how** to build it. A task agent reads the plan alongside the codebase and uses its own judgment on implementation. A plan is ready when it answers:

- **Existing touchpoints** — which files (with paths) are modified or extended, and what role each plays.
- **Contracts** — the precise interface at every boundary the task crosses: function signatures, HTTP endpoint shapes, message/event names and payloads, file formats. Be exact; a cold agent cannot guess a name or shape.
- **Concept boundaries** — names or patterns in the codebase that could be confused with new ones introduced by this plan. Call these out explicitly.
- **.gitignore** — if the plan produces build artifacts, generated files, or local data, note what should be added to `.gitignore`.

Avoid over-specifying internal details — variable names, loop structure, algorithmic approach — unless a specific approach is required by a constraint the agent wouldn't otherwise know about. If two valid implementations satisfy the contracts, either is acceptable.

## Orchestrating Implementation

Read `.plans/plan.md` to understand available plans. The user's prompt will specify which plans to orchestrate.

Send notifications via ntfy.sh (topic: `emerald42create_`) when starting and completing each plan. Keep messages terse.

### Per-Plan Instructions

For each plan:

1. Implement the plan following its checklist and validation steps, updating checklist items as each step completes — do not batch updates at the end.
2. If successful, commit the implementation to the repository.
3. Report whether the implementation succeeded, and if not, what the error was.
4. When the sub-plan is fully complete, do all three of the following steps in order:
   1. Move the file from `.plans/pending/` to `.plans/implemented/`.
   2. Remove the row from whichever "Ready to Implement" or "Not Ready" table it is in.
   3. Add the row to the **Completed** table with status `✅ Done`, updating the plan doc link to point to `implemented/`.

### Single Plan vs. Multiple Plans

**Single plan** — implement it directly yourself. Do not delegate to a subagent.

**Multiple plans** — delegate each plan to a new foreground subagent in sequence. Instruct each subagent to follow the Per-Plan Instructions above. Wait for each subagent to complete before starting the next. If any subagent fails, stop immediately and report the failure.
