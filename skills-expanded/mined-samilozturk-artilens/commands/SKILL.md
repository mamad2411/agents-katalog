---
name: commands
description: >-
  Catalog available slash commands, ArtiLens skills, plugins, and contextual recommendations. Use when the user asks what commands/tools/skills are available, what ArtiLens can do, or what to run next.
allowed-tools: [Bash, Read, Agent]
---

# Commands Catalog

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" session commands --data .claude/artilens/commands.data.json`.
2. Relay the CLI's summary line to the user verbatim.
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to commands.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: catalog of available commands/skills; contextual recommendations with reasons.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, mention the top contextual recommendations (with reason) and relay the artifact URL.
