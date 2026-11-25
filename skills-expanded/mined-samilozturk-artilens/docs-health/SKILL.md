---
name: docs-health
description: >-
  Analyze CLAUDE.md, AGENTS.md, rules, skills, plans, and docs for stale, broken, or conflicting context guidance. Use when docs may be outdated, contradictory, stale, misleading, or need a health check.
allowed-tools: [Bash, Read, Agent]
---

# Docs Health

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/run-artilens.mjs" docs-health --no-llm --data .claude/artilens/docs-health.data.json`.
2. Relay the CLI's summary line to the user verbatim (score, finding count).
3. Start a background subagent with the Agent tool: `subagent_type: general-purpose`, `model: sonnet`, `run_in_background: true`. Prompt template:
   "Read `<absolute path to docs-health.data.json>` and `${CLAUDE_PLUGIN_ROOT}/references/artifact-authoring.md`. Load the artifact-design skill, then author and publish an artifact with the Artifact tool.
   Page plan: score up front; findings table (file, kind, evidence); suggested fix list.
   All visual design decisions are yours."
4. Continue your own task. When the subagent finishes, relay the artifact URL to the user.

If contradiction candidates appear in the data JSON, inspect only the candidate lines before suggesting edits.
