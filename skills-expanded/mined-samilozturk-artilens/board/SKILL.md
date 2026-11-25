---
name: board
description: >-
  Create a draggable planning, kanban, roadmap, or backlog board artifact with copy-as-prompt feedback. Use for task ordering, project boards, sprint planning, prioritization, or moving cards between columns.
allowed-tools: [Bash, Read, Agent]
---

# Board Recipe

1. Gather the column/card data: ask the user for columns and cards, or infer them from the conversation context (backlog items, task list, etc.). There is no CLI command for this skill.
2. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Data: <columns and cards gathered above, inline>.
   Page plan: columns (Now/Next/Later, or the user's given columns) with cards; drag-and-drop affordance; copy-as-prompt using the `data-card`/`data-column` move contract.
   All visual design decisions are yours."
3. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
4. If the user pastes back copy-as-prompt JSON, apply `changes` and republish to the same URL (include the prior artifact URL in the subagent prompt).
