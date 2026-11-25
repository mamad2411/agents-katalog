---
name: task-decomposition-tree
description: "Decompose a large user request into a tree of smaller, independently verifiable tasks so the work can be planned, parallelized, delegated, and reviewed leaf-by-leaf."
---

# Task decomposition tree

Most agent failure modes start with bad decomposition — either too coarse (a single mega-task that can't be reviewed) or too fine (a tree of trivial leaves that creates more coordination cost than work).

## The structure

A decomposition tree has three levels:

- **Root.** The user's outcome, in their words. Don't editorialize.
- **Branches.** 3–7 mid-level deliverables that together produce the root.
- **Leaves.** Concrete, verifiable actions (1–4 hours of agent time each).

Each leaf has:

- An owner (you, another agent template, or a human).
- A definition of done (a sentence that says exactly when it's complete).
- An `independent` / `dependent` flag for `parallel-agent-coordination`.
- A short list of tools or skills required.

## When to apply

- Any user request that requires more than 3 tool calls to satisfy.
- Any sprint or planning iteration.
- Any retrospective where you are figuring out why work missed.

## The loop

1. Restate the root in one sentence.
2. Draft 3–7 branches. If you have more than 7, you are mixing levels; collapse some.
3. For each branch, draft leaves at the granularity where one agent (or one engineer) can finish it in a single sitting.
4. For each leaf, mark dependencies on other leaves (use leaf ids).
5. Persist via `planning_tasks_bulk_create` so the tree lives in the planning system, not just in the chat.

## Anti-patterns

- One mega-leaf that hides 3 days of work behind a single status field.
- Leaves with no verifiable definition of done.
- Mixing levels — a "deploy to staging" leaf next to a "decide entire pricing model" leaf.
