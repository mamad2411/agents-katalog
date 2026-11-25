---
name: what-next

description: Determine the next useful action from the current state of the work. Use when you have reached a stopping point, are unsure what to do next, or want to continue from where you currently are.

metadata:

  disable-model-invocation: true

---

# What Next

You are here. Now what?

This skill identifies the **next useful action** from the current state of the work.

It is not a general planner, task manager, or brainstorming tool. It looks at what has already been done, what is currently in progress, and what remains unresolved, then recommends the most appropriate next step.

## What to consider

Before answering, inspect the available context:

- What the user is currently working on
- What has already been completed
- What is currently in progress
- What is blocked, missing, or unresolved
- Any explicit goal, requirement, or constraint
- The most recent meaningful change or result

Use the latest state as the primary source of truth.

Do not assume work was completed when the context does not show it.

Do not invent missing requirements, tasks, or project state.

## Determine the next step

Choose the **single most useful next action**.

Prefer actions that:

1. Directly move the current work toward its goal.
2. Resolve an existing blocker or uncertainty.
3. Complete an obvious unfinished step.
4. Validate or verify the most recent change when validation is the natural next step.
5. Preserve momentum without introducing unnecessary work.

Do not recommend multiple alternatives unless the next step genuinely depends on an unresolved choice.

When several actions are possible, prefer the one with the clearest immediate value.

## When the next step is unclear

If the available context is insufficient to determine a meaningful next action, ask for the **smallest missing piece of information** needed to continue.

Do not fill missing context with assumptions.

## When nothing needs to happen yet

If the work is already complete or no meaningful next action exists:

> No immediate next step. The current state is sufficient for now.

## How to answer

Format every reply as:

1. **Current state** — one short sentence describing where the work currently stands.
2. **Next step** — the single most useful action to take now.
3. **Why** — one short explanation of why this should happen next.

Stop after that.

## Principles

- Optimize for the next action, not the entire plan.
- Prefer concrete actions over vague advice.
- Use the current context as the source of truth.
- Do not repeat completed work.
- Do not invent progress that is not present.
- Do not turn a simple next step into a large workflow.

## Maintenance

This skill should remain focused on identifying the next actionable step from the current state.

Only update this file when its decision rules or output format need to change.