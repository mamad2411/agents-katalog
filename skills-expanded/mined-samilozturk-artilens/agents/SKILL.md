---
name: agents
description: >-
  Visualize subagent, Agent tool, and delegated task activity from the current Claude Code session. Use when work was delegated or the user asks what agents/subagents did, what ran in the background, or how tasks were coordinated.
allowed-tools: [Bash, Read, Agent]
---

# Agent View

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" session agents --data .claude/artilens/agents.data.json`.
2. Relay the CLI's summary line to the user verbatim.
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to agents.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: timeline of which subagent did what and when; a task/result summary table. Copy-as-prompt is optional — only include it if the JSON has editable state worth capturing.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.

If hook event logging is enabled, the data JSON includes richer SubagentStart/SubagentStop and Task events.
