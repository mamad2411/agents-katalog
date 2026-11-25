---
name: usage
description: >-
  Visualize the current Claude Code session's real usage: cost, model token usage, cache tokens, line-change estimate, and MCP/skill share. Use when the user asks for usage, cost, spend, tokens, model usage, session stats, or "/usage"-style data.
allowed-tools: [Bash, Read, Agent]
---

# Usage Lens

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" usage --latest --data .claude/artilens/usage.data.json`.
2. Relay the CLI's summary line to the user verbatim (total cost, estimate flag).
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to usage.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: total cost up front (flag if estimated); per-model token/cost breakdown; MCP-server and skill usage share; lines-added/removed summary; copy-as-prompt.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
5. If the user pastes back copy-as-prompt JSON, apply `changes` and republish to the same URL (include the prior artifact URL in the subagent prompt).

If the user's current message also contains raw `/usage` command output (session/week percentage bars and reset times), relay those numbers separately as "plan limits (from your /usage output)" — do not fabricate this section when no paste is present.

Never paste raw transcript content into chat.
