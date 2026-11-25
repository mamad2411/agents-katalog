---
name: context-files
description: >-
  Inventory project context files — CLAUDE.md, AGENTS.md, rules, SKILL.md files, plans, and docs — with read-frequency from the current transcript. Use when the user asks what context is loaded, which files shaped the session, or before auditing stale or unused context files.
allowed-tools: [Bash, Read, Agent]
---

# Context Files Inventory

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" session context-files --data .claude/artilens/context-files.data.json`.
2. Relay the CLI's summary line to the user verbatim.
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to context-files.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: inventory of loaded context files; read-frequency per file; highlight stale-looking candidates.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.

This is an inventory (what's loaded and how often it's read), not a staleness judgment — for stale or contradictory content, use `artilens:docs-health` instead.
