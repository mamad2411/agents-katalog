---
name: lens
description: >-
  Visualize the current Claude Code session's context health, token pressure, hot files, and compact/clear/handoff recommendation. Use when the user asks to see session context, context window, context usage, session health, handoff readiness, or whether to compact.
allowed-tools: [Bash, Read, Agent]
---

# Context Lens

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" lens --latest --data .claude/artilens/lens.data.json`.
2. Relay the CLI's summary line to the user verbatim (health score, context %, recommendation).
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to lens.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: health score + context % + one-line recommendation (compact/clear/continue) up top; the 10x10 context-window grid with a category legend; token-breakdown; tool-usage and hot-files tables; the handoff block; copy-as-prompt.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.
5. If the user pastes back copy-as-prompt JSON, apply `changes` and republish to the same URL (include the prior artifact URL in the subagent prompt).

If the recommendation is `compact` or `handoff`, read `.claude/artilens/lens.data.json` yourself and use `decision.preservationPrompt` in the next `/compact`, or the `handoff` block for a fresh session.

Never paste raw transcript content into chat.
