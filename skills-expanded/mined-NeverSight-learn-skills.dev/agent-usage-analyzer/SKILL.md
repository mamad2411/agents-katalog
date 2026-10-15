---
name: agent-usage-analyzer
description: Analyze local AI-agent session histories and report usage counts for agent skills, tools, commands, or MCP actions across sessions. Use for requests about skill rankings, top skills used last week, tool usage, recent-session comparisons, agent-specific usage, or exports from Codex, Claude Code, and other compatible JSON or JSONL agent-history exports. Read-only.
---

# Agent Usage Analyzer

## Goal
Produce an accurate, local, read-only report of structured skill, tool, command, and MCP usage across agent sessions.

## Inputs to infer from the user's request
- agent or source filters
- since and until date filters
- repo or cwd filters
- raw versus canonical mode
- kind filter
- output format
- whether the user supplied an export directory
- whether samples, partial sessions, or heuristic parsing are allowed

## Resources
- Analyzer script: `scripts/analyze.mjs`
- Install helper: `scripts/install.mjs`
- Output contract: `references/OUTPUT.md`
- Alias example: `references/ALIASES.example.yaml`

## Workflow
1. Do not count usage manually from transcript prose.
2. Prefer running `scripts/analyze.mjs`.
3. Use `--provider auto` unless the user supplied an explicit export directory.
4. If the user asks for "skill usage", "agent skills", or named skill counts, prefer `--kind skill`.
5. For Codex and Claude Code event-log exports, count skill usage from structured `.../skills/<name>/SKILL.md` load signals rather than generic transport tools.
6. If the source only exposes tool or MCP events and does not expose any structured skill-load signal, say so explicitly instead of presenting tool counts as skill counts.
7. If the analyzer reports missing prerequisites, explain what is missing instead of guessing.
8. Present the result as a markdown table unless the user asked for JSON or CSV.
9. Always state coverage and caveats.

## Output rules
- Treat `skill`, `tool`, `command`, and `mcp` as separate categories unless the user asks for a broader combined report.
- Default to canonical mode.
- Use raw mode only when the user asks for raw names.
- Keep samples off unless the user asks for them.
- Sort rows by invocation count descending.
- Never imply skipped sessions were counted.
- When reporting skill usage from Codex or Claude Code archives, note that counts come from structured skill-load records, typically reads or prompts that reference `SKILL.md`.
