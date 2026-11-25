---
name: todos
description: >-
  Visualize todos, plan checklists, progress, blockers, and next actions from the current transcript and project plan files. Use when the user asks for progress, task status, blockers, roadmap state, or the next safe task.
allowed-tools: [Bash, Read, Agent]
---

# Todo View

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" session todos --data .claude/artilens/todos.data.json`.
2. Relay the CLI's summary line to the user verbatim.
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to todos.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: status counters; task list marked with status/blockers; suggested next safe step; copy-as-prompt with `data-change-op` checkboxes on tasks.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
5. If the user pastes back copy-as-prompt JSON, apply `changes` and republish to the same URL (include the prior artifact URL in the subagent prompt).
